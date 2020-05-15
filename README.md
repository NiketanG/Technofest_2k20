# COMeIT_RegistrationApp
Web App for the registration of COMeIT's events in Government Polytechnic, Pune.

Demo at : https://bit.ly/technofest2k20



# How to run:
Requires Python v3. Replace python3 and pip3 with py or python and pip, if necessary.

pip3 install --user -r requirements.txt

python3 Config.py

python3 manage.py create_db

python3 manage.py create_user

python3 manage.py create_events

python3 manage.py run_redis (Run this in a new terminal window)

python3 manage.py run_worker (Run this in a new window)

flask run (Run this in a new terminal window)

