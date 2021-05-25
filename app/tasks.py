from flask_mail import Mail, Message
from flask import Flask, render_template
from app import mail as mail
from flask import current_app as app
import requests
import json
import paytmchecksum
import os


def send_mail(registration_dict):
    msg = Message('Registration Successful', recipients=[registration_dict['email']])
    msg.html = render_template('/mail_format.html', registration=registration_dict)
    mail.send(msg)
    print("Mail sent")


def check_txn_status(paytmParams):
    environment = os.getenv('FLASK_ENV')
    url = "https://securegw.paytm.in/v3/order/status" if environment == "production" else "https://securegw-stage.paytm.in/v3/order/status"

    # Generate checksum by parameters we have
    checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), app.config['MERCHANT_KEY'])

    paytmParams["head"] = {
        "signature"	: checksum
    }

    # prepare JSON string for request
    post_data = json.dumps(paytmParams)

    response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()

    if response.get("body").get("resultInfo").get("resultStatus") == 'TXN_SUCCESS':
        return True
    else:
        # check_pending_transaction(paytmParams)
        return False


def check_pending_transaction(paytmParams):
    q.enqueue(check_txn_status, paytmParams)
