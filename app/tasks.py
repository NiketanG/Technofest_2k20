from flask_mail import Mail, Message
from flask import Flask,render_template
from app import mail as mail
from flask import current_app as app
import requests
import json
import app.Checksum as Checksum

def send_mail(registration_dict):
        msg = Message('Registration Successful', recipients = [registration_dict['email']])
        msg.html = render_template('/mail_format.html', registration=registration_dict)
        mail.send(msg)
        print("Mail sent")

def check_txn_status(paytmParams):
    # for Staging
    url = "https://securegw.paytm.in/order/status"

    # for Production
    # url = "https://securegw.paytm.in/order/status"

    # Generate checksum by parameters we have
    checksum = Checksum.generate_checksum(paytmParams, app.config['MERCHANT_KEY'])

    # put generated checksum value here
    paytmParams["CHECKSUMHASH"] = checksum

    # prepare JSON string for request
    post_data = json.dumps(paytmParams)

    response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()

    if response['STATUS'] == 'TXN_SUCCESS':
        return True
    else:
        #check_pending_transaction(paytmParams)
        return False

def check_pending_transaction(paytmParams):
    q.enqueue(check_txn_status, paytmParams)