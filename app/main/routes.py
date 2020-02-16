from flask import render_template, Blueprint, flash, redirect, render_template, url_for, request, session
from app.models import events, registrations, payments
from app.main.forms import RegistrationForm, set_evlist
from flask_login import current_user
import uuid
import hashlib
from flask_sqlalchemy import SQLAlchemy
# import checksum generation utility from PayTM
import requests
import app.Checksum as Checksum
import json
from app import db
from app.tasks import send_mail, check_pending_transaction, check_txn_status
from flask import current_app as app
import redis
from rq import Queue, Connection
import traceback

main = Blueprint('main', __name__)

class event_list:
    def __init__(self):
        self.evlist = db.session.query(events.event_id, events.event_name, events.amt, events.solo, events.duo, events.squad, events.team_5).order_by(events.event_id).all()
    def __repr__(self):
        return f"{self.evlist}"

def send_email(registration_dict, evlist):
    try:
        reg_info = registration_dict.__dict__
        event_selected = int(reg_info['event_id']) - 1
        reg_info['event_name'] = evlist[event_selected][1]
        #send_mail(reg_info)
    except Exception as e:
        print(e)
        traceback.print_exc()
    
@main.route('/register/', methods=['POST', 'GET'])
@main.route('/register', methods=['POST', 'GET'])
def register():
    ev_list = event_list()
    evlist = vars(ev_list)
    evlist = [val for evlist in evlist.values() for val in evlist]
    list = [(str(ev_id), ev_name) for ev_id, ev_name, ev_amt, ev_solo, ev_duo, ev_squad, ev_team_5 in evlist]
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
        ev_selected = int(form.event.data) - 1
        TXN_AMOUNT = (int([amt for ev_id, ev_name, amt, solo, duo,
                           squad, team_5 in evlist][ev_selected]))
        # initialize a dictionary
        paytmParams = dict()
        paytmParams = {
            "MID": app.config['MID'],
            "WEBSITE": app.config['WEBSITE'],
            "INDUSTRY_TYPE_ID": "Retail",
            "CHANNEL_ID": app.config['CHANNEL_ID'],
            "ORDER_ID": ORDER_ID,
            "CUST_ID": CUST_ID,
            "MOBILE_NO": str(form.phno.data),
            "EMAIL": form.email.data,
            "TXN_AMOUNT": str(TXN_AMOUNT),
            "CALLBACK_URL": request.host_url + "payment",
        }
        # Generate checksum by parameters we have
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        checksum = Checksum.generate_checksum(
            paytmParams, app.config['MERCHANT_KEY'])

        url = app.config['PAYMENT_URL'] + str("process")

        registration = registrations(name=form.name.data,
                                     phno=form.phno.data,
                                     email=form.email.data,
                                     clgname=form.clgname.data,
                                     grpname=form.GrpName.data,
                                     team=form.radio_team.data,
                                     event_id=form.event.data,
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
                        #send_email(registration_dict,evlist)
                        flash('An Email consisting of Registration Details has been sent to the specified email address')
                    except Exception as error:
                        print(error)
                        traceback.print_exc()
                except Exception as error:
                    db.session.rollback()
                    flash('Registration Failed')
                    print(error)
                    traceback.print_exc()
                
                return redirect(url_for('.success', order_id = registration_dict['order_id'], user_id = registration_dict['cust_id'] ))
                
            else:
                return render_template('/paymentform.html', registration=registration_dict, paytmParams=paytmParams, url=url, checksum=checksum)
        except Exception as error:
            print(error)
            traceback.print_exc()
            
    return render_template('/Main.HTML', title='Registrations', form=form, evlist=evlist)

@main.route('/success')
def success():
    Order_ID = request.args.get('order_id', False)
    User_ID = request.args.get('user_id', False)
    evlist = session['evlist']
    print(evlist)


    if (not(Order_ID == False or User_ID == False)):
        registration_dict = db.session.query(registrations).filter_by(order_id=Order_ID, cust_id=User_ID).first()

        send_email(registration_dict, evlist)
    else:
        flash('No Order_ID or User_ID was provided')
        registration_dict = {'order_id':'Null', 'user_id':'Null'}
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

        return render_template('PaymentStatus.html', resp_code=Response_code, resp_msg = Response_msg ,txn_id=Transaction_ID, status=Payment_Status, registration=registration_dict, evlist=evlist)

@main.route('/payment', methods=['POST', 'GET'])
def payment():
    ev_list = event_list()
    evlist = vars(ev_list)
    evlist = [val for evlist in evlist.values() for val in evlist]
    
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
    paytmChecksum = ""

    # Create a Dictionary from the parameters received in POST
    paytmParams = {}
    for key, value in received_data.items():
        if key == 'CHECKSUMHASH':
            paytmChecksum = value
        else:
            paytmParams[key] = value
    
    #possible error
    registration_dict = session.get('reg_info')
    registration = registrations(**registration_dict)

    isValidChecksum = Checksum.verify_checksum(
        paytmParams, app.config['MERCHANT_KEY'], paytmChecksum)
    
    print("Checksum : " + str(isValidChecksum))

    payment = payments(txn_id=paytmParams['TXNID'],
                       order_id=paytmParams['ORDER_ID'], 
                       txn_amount=paytmParams['TXNAMOUNT'], 
                       status=paytmParams['STATUS'], 
                       resp_code=paytmParams['RESPCODE'], 
                       resp_msg=paytmParams['RESPMSG'])
    
    try:
        db.session.add(payment)
        db.session.commit()
        print('Payment Details Added')
    except Exception as error:
        print(error)
        traceback.print_exc()

    TxnCheck = check_txn_status(paytmParams)
    print("TxnCheck" + str(TxnCheck))

    if (paytmParams["STATUS"] == "TXN_SUCCESS") and (TxnCheck):
        paid = True
        registration.paid = True
        print('Paid')
    elif paytmParams["STATUS"] == "PENDING":
        if check_pending_transaction(paytmParams):
            paid = True
            registration.paid = True
    else:
        paid = False
        registration.paid = False

    #if isValidChecksum and paid:
    if paid:
        try:
            db.session.add(registration)
            db.session.commit()

            print('Registration Done')
            flash('Registration Successful')
            try:
                #send_email(registration_dict,evlist)
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

    return redirect(url_for('.success', order_id = registration_dict['order_id'], user_id = registration_dict['cust_id'],txn_id = paytmParams['TXNID']))