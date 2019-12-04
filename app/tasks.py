from flask_mail import Mail, Message
from flask import Flask,render_template
import requests
import app.Checksum as Checksum
import json
from app import mail as mail

def send_mail(registration_dict):
        msg = Message('Registration Successful', recipients = [registration_dict['email']])
        msg.html = render_template('/mail_format.html', registration=registration_dict)
        mail.send(msg)
        print("Mail sent")

def check_txn_status(paytmParams):
    # Generate checksum by parameters we have
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = Checksum.generate_checksum(paytmParams, app.config['MERCHANT_KEY'])
    # put generated checksum value here
    paytmParams["CHECKSUMHASH"] = checksum
    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/order/status"

    # for Production
    # url = "https://securegw.paytm.in/order/status"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    
    if response['STATUS'] == 'PENDING':
        q.enqueue(check_txn_status, paytmParams)

def check_pending_transaction(paytmParams):
    q.enqueue(check_txn_status, paytmParams)