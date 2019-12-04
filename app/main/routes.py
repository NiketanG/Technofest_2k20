from flask import render_template, Blueprint, flash, redirect, render_template, url_for,request, session
from app.models import events, registrations
from app.main.forms import RegistrationForm, set_evlist
from flask_login import current_user
import uuid
import hashlib
# import checksum generation utility from PayTM
import app.Checksum as Checksum
from app import db
from app.tasks import send_mail, check_pending_transaction
from flask import current_app as app
import redis
from rq import Queue, Connection

main = Blueprint('main', __name__)

class event_list:
    def __init__(self):
        self.evlist = db.session.query(events.event_id, events.event_name, events.amt_per_head, events.solo, events.duo, events.squad).all()
    def __repr__(self):
        return f"{self.evlist}"

def send_email(registration_dict, evlist):
    reg_info = registration_dict
    event_selected = int(reg_info['event_id']) - 1
    reg_info['event_name'] = evlist[event_selected][1]
    redis_url = app.config['REDIS_URL']
    with Connection(redis.from_url(redis_url)):
                    q = Queue()
                    q.enqueue(send_mail, reg_info)

@main.route('/register/', methods=['POST', 'GET'])
@main.route('/register', methods=['POST', 'GET'])
def register():
    ev_list = event_list()
    evlist = vars(ev_list)
    evlist = [val for evlist in evlist.values() for val in evlist]
    list = [(str(ev_id), ev_name) for ev_id, ev_name, ev_amt, ev_solo, ev_duo, ev_squad in evlist]
    set_evlist(list)

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
                           squad in evlist][ev_selected]))*int(form.radio_team.data)
        # initialize a dictionary
        paytmParams = dict()
        paytmParams = {
            "MID": app.config['MID'],
            "WEBSITE": "WEBSTAGING",
            "INDUSTRY_TYPE_ID": "Retail",
            "CHANNEL_ID": "WEB",
            "ORDER_ID": ORDER_ID,
            "CUST_ID": CUST_ID,
            "MOBILE_NO": str(form.phno.data),
            "EMAIL": form.email.data,
            "TXN_AMOUNT": str(TXN_AMOUNT),
            "CALLBACK_URL": "http://127.0.0.1:5000/payment",
        }
        # Generate checksum by parameters we have
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        checksum = Checksum.generate_checksum(
            paytmParams, app.config['MERCHANT_KEY'])
        # for Staging
        url = "https://securegw-stage.paytm.in/order/process"

        # for Production
        # url = "https://securegw.paytm.in/order/process"

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
                                     amt=str(TXN_AMOUNT)
                                     )
        registration_dict = vars(registration)
        registration_dict.pop('_sa_instance_state', None)
        session['reg_info'] = registration_dict
        registration_dict = session['reg_info']
        registration = registrations(**registration_dict)
        try:
            if request.form['submit_ofc'] == "REGISTER ( Pay via Cash )":
                try:
                    registration.paid = True
                    db.session.add(registration)
                    db.session.commit()
                    flash('Registration Successful')

                    send_email(registration_dict,evlist)

                except Exception as error:
                    db.session.rollback()
                    flash('Registration Failed')
                    print(error)

                return render_template('RegistrationSuccess.html', registration=registration_dict, evlist=evlist, paytmParams=paytmParams)
        except:
            return render_template('/paymentform.html', paytmParams=paytmParams, url=url, checksum=checksum)
    return render_template('/Main.HTML', title='Registrations', form=form, evlist=evlist)


@main.route('/payment', methods=['POST', 'GET'])
def payment():
    ev_list = event_list()
    evlist = vars(ev_list)
    evlist = [val for evlist in evlist.values() for val in evlist]

    registration_dict = session['reg_info']
    registration = registrations(**registration_dict)
    received_data = {
        "MID": request.form["MID"],
        "TXNID": request.form["TXNID"],
        "ORDER_ID": request.form["ORDERID"],
        "BANKTXNID": request.form["BANKTXNID"],
        "TXNAMOUNT": request.form["TXNAMOUNT"],
        "CURRENCY": request.form["CURRENCY"],
        "STATUS": request.form["STATUS"],
        "RESPCODE": request.form["RESPCODE"],
        "RESPMSG": request.form["RESPMSG"],
        "TXNDATE": request.form["TXNDATE"],
        "GATEWAYNAME": request.form["GATEWAYNAME"],
        "BANKNAME": request.form["BANKNAME"],
        "PAYMENTMODE": request.form["PAYMENTMODE"],
        "CHECKSUMHASH": request.form["CHECKSUMHASH"],
    }

    paytmChecksum = ""
    # Create a Dictionary from the parameters received in POST
    # received_data should contains all data received in POST
    paytmParams = {}
    for key, value in received_data.items():
        if key == 'CHECKSUMHASH':
            paytmChecksum = value
        else:
            paytmParams[key] = value

    isValidChecksum = Checksum.verify_checksum(
        paytmParams, app.config['MERCHANT_KEY'], paytmChecksum)

    if paytmParams["STATUS"] == "TXN_SUCCESS":
        paid = True
        registration.paid = True
    else:
        paid = False
        registration.paid = False

    paymentstatus = paytmParams["STATUS"].replace("TXN_", "")

    if isValidChecksum and paid:
        try:
            db.session.add(registration)
            db.session.commit()
            flash('Registration Successful')
            send_email(registration_dict,evlist)

        except Exception as error:
            db.session.rollback()
            flash('Registration Failed')
            print(error)
    else:
        flash('Registration Failed')
    return render_template('PaymentStatus.html', paytmParams=paytmParams, status=paymentstatus, registration=registration_dict, evlist=evlist)

