# Technofest 2k20  Registration Web Site
An Event Registration Web Site for Technofest 2k20, Built for COMeIT - Government Polytechnic, Pune
Developed using Flask Micro Framework for Python.
#### Demo : [Technofest 2k20](https://bit.ly/technofest2k20)

##### Features
- Login and Signup for Volunteers/Management
- Paytm Payment Gateway
- Dynamic Events, Prices and Participants from Database
- Mail sending on Registration
- Registrations and Payments can be viewed by Volunteers/Management after Logging in

### Installation

###### Clone the repo and cd into it.
###### Install the requirements. 
#
```
pip install -r requirements.txt
```
###### Configure the Environment Variables
#
> SECRET_KEY
```
SQLALCHEMY_DATABASE_URI
MAIL_SERVER
MAIL_PORT
MAIL_USERNAME
MAIL_PASSWORD
MAIL_USE_TLS
MAIL_USE_SSL
MAIL_DEFAULT_SENDER
MID
MERCHANT_KEY
CHANNEL_ID
WEBSITE
PAYMENT_URL
BCRYPT_LOG_ROUNDS
REDIS_URL
QUEUES
AUTH_CODE
```
###### Create the database and events.
#
```
python3 manage.py create_db
python3 manage.py create_events
```
###### Run
#
```
flask run
```


###### License
#
---

MIT

