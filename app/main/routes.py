from flask import render_template, Blueprint, flash, redirect, render_template, url_for, request, session, jsonify
from app.models import events, registrations, payments
from app.main.forms import RegistrationForm, set_evlist
from flask_login import current_user
import uuid
import hashlib
from flask_sqlalchemy import SQLAlchemy
# import checksum generation utility from PayTM
import requests
import paytmchecksum
import json
from app import db
from app.tasks import send_mail, check_pending_transaction, check_txn_status
from flask import current_app as app
import redis
from rq import Queue, Connection
import traceback
import os

main = Blueprint('main', __name__)


class event_list:
    evlist = list()

    def __init__(self):
        eventList = events.query.all()
        self.evlist = [item.as_dict() for item in eventList]

    def __repr__(self):
        return f"{self.evlist}"


def send_email(registration_dict, evlist):
    try:
        reg_info = registration_dict.__dict__
        event_selected = int(reg_info['event_id']) - 1
        reg_info['event_name'] = evlist[event_selected]["event_name"]
        send_mail(reg_info)
    except Exception as e:
        print(e)
        traceback.print_exc()


@main.route('/register/', methods=['POST', 'GET'])
@main.route('/register', methods=['POST', 'GET'])
def register():

    evlist = event_list().evlist
    list = [(str(event["event_id"]), event["event_name"]) for event in evlist]
    set_evlist(list)
    session['evlist'] = evlist
    form = RegistrationForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            user = current_user.username
        else:
            user = "NULL"
        salt = '8f1e39a21c9d4661b24a06356e5fe4d1'
        ORDER_ID = str(uuid.uuid4())
        CUST_ID = str(hashlib.md5(salt.encode() +
                                  form.phno.data.encode()).hexdigest())

        ev_selected = int(form.event.data)
        selectedEvent = next((item for item in evlist if item["event_id"] == ev_selected), None)

        if (selectedEvent is None):
            flash("An error occured")
            return redirect(url_for('.register'))
        TXN_AMOUNT = int(selectedEvent["amt"])

        registration = registrations(name=form.name.data,
                                     phno=form.phno.data,
                                     email=form.email.data,
                                     clgname=form.clgname.data,
                                     grpname=form.GrpName.data,
                                     team=form.radio_team.data,
                                     event_id=ev_selected,
                                     user=user,
                                     order_id=ORDER_ID,
                                     cust_id=CUST_ID,
                                     amt=str(TXN_AMOUNT),
                                     paymentmode='ONLINE'
                                     )
        registration_dict = vars(registration)
        registration_dict.pop('_sa_instance_state', None)
        session['reg_info'] = registration_dict
        registration = registrations(**registration_dict)

        try:
            if request.form.get('submit_ofc', False) == "REGISTER ( Pay via Cash )":
                try:
                    registration.paid = True
                    registration.paymentmode = 'Cash'

                    db.session.add(registration)
                    db.session.commit()

                    flash('Registration Successful')
                    print('Offline Registration Done')
                    try:
                        # send_email(registration_dict,evlist)
                        flash('An Email consisting of Registration Details has been sent to the specified email address')
                    except Exception as error:
                        print(error)
                        traceback.print_exc()
                except Exception as error:
                    db.session.rollback()
                    flash('Registration Failed')
                    print(error)
                    traceback.print_exc()

                return redirect(url_for('.success', order_id=registration_dict['order_id'], user_id=registration_dict['cust_id']))

            else:
                environment = os.getenv('FLASK_ENV')
                # initialize a dictionary
                paytmParams = dict()
                paytmParams["body"] = {
                    "requestType": "Payment",

                    "mid": app.config['MID'],
                    "websiteName": app.config['WEBSITE'] if environment == "production" else "WEBSTAGING",
                    "orderId": ORDER_ID,
                    "callbackUrl": request.host_url + "payment",
                    "txnAmount": {
                        "value": str(TXN_AMOUNT),
                        "currency": "INR",
                    },
                    "userInfo": {
                        "custId": CUST_ID,
                        "mobile": str(form.phno.data),
                        "email": form.email.data,
                    },
                }

                # Generate checksum by parameters we have
                # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys

                checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), app.config['MERCHANT_KEY'])

                paytmParams["head"] = {
                    "signature": checksum,
                    "channelId": app.config['CHANNEL_ID']
                }

                postData = json.dumps(paytmParams)

                initiateTxnUrl = app.config["PAYMENT_URL" if environment == "production" else "PAYMENT_URL_STAGING"] + "initiateTransaction?mid=" + \
                    app.config["MID"] + "&orderId=" + ORDER_ID

                paytmResponse = requests.post(initiateTxnUrl, data=postData, headers={
                                              "Content-type": "application/json"}).json()

                paymentPageUrl = app.config["PAYMENT_URL" if environment == "production" else "PAYMENT_URL_STAGING"] + "showPaymentPage?mid=" + \
                    app.config["MID"] + "&orderId=" + ORDER_ID

                return render_template('/paymentform.html',
                                       mid=paytmParams.get("body").get("mid"),
                                       orderId=paytmParams.get("body").get("orderId"),
                                       url=paymentPageUrl,
                                       txnToken=paytmResponse.get("body").get("txnToken"))
        except Exception as error:
            print(error)
            traceback.print_exc()

    return render_template('/Main.HTML', form=form, evlist=evlist)


@main.route('/success')
def success():
    Order_ID = request.args.get('order_id', False)
    User_ID = request.args.get('user_id', False)
    evlist = event_list().evlist

    if (not(Order_ID == False or User_ID == False)):
        registration_dict = db.session.query(registrations).filter_by(order_id=Order_ID, cust_id=User_ID).first()

        send_email(registration_dict, evlist)
    else:
        flash('No Order_ID or User_ID was provided')
        registration_dict = {'order_id': 'Null', 'user_id': 'Null'}
        return render_template('RegistrationSuccess.html', registration=registration_dict, evlist=evlist)

    Transaction_ID = request.args.get('txn_id', False)

    if (Transaction_ID == False):
        return render_template('RegistrationSuccess.html', registration=registration_dict, evlist=evlist)
    else:
        payment_dict = payments.query.filter_by(txn_id=Transaction_ID, order_id=Order_ID).first()
        if payment_dict == None:
            Payment_Status = "FAILED"
            Response_code = "810"
            Response_msg = "Seems like the Payment wasn't completed. You can reach us with the given Order_ID and Transaction_ID if the money has been deducted from your account."
        else:
            payment_dict = vars(payment_dict)
            Response_code = str(payment_dict['resp_code'])
            Response_msg = payment_dict['resp_msg']
            Payment_Status = payment_dict.get('status', False)

            if Payment_Status != False:
                Payment_Status = Payment_Status.replace("TXN_", "")
            if Payment_Status == 'SUCCESS':
                send_email(registration_dict, evlist)

        return render_template('PaymentStatus.html', resp_code=Response_code, resp_msg=Response_msg, txn_id=Transaction_ID, status=Payment_Status, registration=registration_dict, evlist=evlist)


@main.route('/payment', methods=['POST', 'GET'])
def payment():
    evlist = event_list()

    received_data = {
        "MID": request.form.get("MID", 'Null'),
        "TXNID": request.form.get("TXNID", 'Null'),
        "ORDER_ID": request.form.get("ORDERID", 'Null'),
        "BANKTXNID": request.form.get("BANKTXNID", 'Null'),
        "TXNAMOUNT": request.form.get("TXNAMOUNT", 'Null'),
        "CURRENCY": request.form.get("CURRENCY", 'Null'),
        "STATUS": request.form.get("STATUS", 'Null'),
        "RESPCODE": request.form.get("RESPCODE", 'Null'),
        "RESPMSG": request.form.get("RESPMSG", 'Null'),
        "TXNDATE": request.form.get("TXNDATE", 'Null'),
        "GATEWAYNAME": request.form.get("GATEWAYNAME", 'Null'),
        "BANKNAME": request.form.get("BANKNAME", 'Null'),
        "PAYMENTMODE": request.form.get("PAYMENTMODE", 'Null'),
        "CHECKSUMHASH": request.form.get("CHECKSUMHASH", 'Null'),
    }
    checksumhash = ""

    # Create a Dictionary from the parameters received in POST
    paytmParams = {}
    for key, value in received_data.items():
        if key == 'CHECKSUMHASH':
            checksumhash = value
        else:
            paytmParams[key] = value

    isValidChecksum = paytmchecksum.verifySignature(
        paytmParams, app.config['MERCHANT_KEY'], checksumhash)

    if isValidChecksum:
        print("Checksum Matched")
    else:
        print("Checksum doesnt match")

    payment = payments(txn_id=paytmParams['TXNID'],
                       order_id=paytmParams['ORDER_ID'],
                       txn_amount=paytmParams['TXNAMOUNT'],
                       status=paytmParams['STATUS'],
                       resp_code=paytmParams['RESPCODE'],
                       resp_msg=paytmParams['RESPMSG'])

    try:
        db.session.add(payment)
        db.session.commit()
    except Exception as error:
        print(error)
        traceback.print_exc()

    registration_dict = session.get('reg_info')

    if (registration_dict is None):
        flash("Registration Failed")
        return redirect(url_for('.register'))

    registration = registrations(
        name=registration_dict.get("name"),
        email=registration_dict.get("email"),
        clgname=registration_dict.get("clgname"),
        phno=registration_dict.get("phno"),
        grpname=registration_dict.get("grpname"),
        event_id=registration_dict.get("event_id"),
        team=registration_dict.get("team"),
        user=registration_dict.get("user"),
        paid=True,
        amt=registration_dict.get("amt"),
        paymentmode=registration_dict.get("paymentmode"),
        order_id=registration_dict.get("order_id"),
        cust_id=registration_dict.get("cust_id"),
    )

    environment = os.getenv('FLASK_ENV')
    txnParams = dict()
    txnParams["body"] = {
        "requestType": "Payment",

        "mid": app.config['MID'],
        "websiteName": app.config['WEBSITE'] if environment == "production" else "WEBSTAGING",
        "orderId": paytmParams['ORDER_ID'],
        "callbackUrl": request.host_url + "payment",
        "txnAmount": {
            "value": str(registration_dict.get("amt")),
            "currency": "INR",
        },
        "userInfo": {
            "custId": registration_dict.get("cust_id"),
            "mobile": registration_dict.get("phno"),
            "email": registration_dict.get("email"),
        },
    }

    txnSuccess = check_txn_status(txnParams)

    if (paytmParams["STATUS"] == "TXN_SUCCESS") and txnSuccess:
        paid = True
        registration.paid = True
    elif paytmParams["STATUS"] == "PENDING":
        if check_pending_transaction(paytmParams):
            paid = True
            registration.paid = True
    else:
        paid = False
        registration.paid = False

    if isValidChecksum and paid:
        try:
            db.session.add(registration)
            db.session.commit()

            flash('Registration Successful')
            try:
                # send_email(registration_dict,evlist)
                flash('An Email consisting of Registration Details has been sent to the specified email address')
            except Exception as error:
                print(error)
                traceback.print_exc()
        except Exception as error:
            db.session.rollback()
            flash('Registration Failed')
            print(error)
            traceback.print_exc()
    else:
        flash('Registration Failed')

    return redirect(url_for('.success', order_id=registration_dict['order_id'], user_id=registration_dict['cust_id'], txn_id=paytmParams['TXNID']))
