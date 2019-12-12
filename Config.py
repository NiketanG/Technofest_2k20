import os
import uuid

def set_envvars():
        print("Configure Project Settings : \n")

        print('SECRET_KEY configuration : \n Press 1 to automatically generate one (Recommended), or Press 2 for manually entering.')
        ch_1 = int(input())
        if (ch_1 == 1):
            SECRET_KEY = str(uuid.uuid4())
            print("Key Generated : " + SECRET_KEY)
        else:
            SECRET_KEY = str(input('Enter Secret Key : '))
            
        print('SQLALCHEMY_DATABASE_URI configuration : \n')
        SQLALCHEMY_DATABASE_URI = str(input('Enter SQLALCHEMY_DATABASE_URI : '))

        print('MAIL configuration : \n')
        ch_3 = int(input())
        if (ch_3 == 1):
            MAIL_USERNAME = 'nikegulekar@gmail.com'
            MAIL_PASSWORD='xyofglsluyzlacbi'
            MAIL_SERVER='smtp.gmail.com'
            MAIL_PORT=465
            MAIL_USE_TLS=False
            MAIL_USE_SSL=True
        else:
            MAIL_USERNAME = str(input('MAIL_USERNAME : '))
            MAIL_PASSWORD=str(input('MAIL_PASSWORD : '))
            MAIL_SERVER=str(input("MAIL_SERVER : "))
            MAIL_PORT=int(input("MAIL_PORT : "))
            MAIL_USE_TLS=bool(input("MAIL_USE_TLS : "))
            MAIL_USE_SSL=bool(input("MAIL_USE_SSL : "))

        MAIL_DEFAULT_SENDER = MAIL_USERNAME
        
        print('Payement Gateway configuration : \n Press 1 for default (Recommended), or Press 2 for manually entering.')
        ch_4 = int(input())
        if (ch_4 == 1):
            MID='HWigbx14300533652986'
            MERCHANT_KEY='9kj1&dB@2zWjbnFO'
            CHANNEL_ID='WEB'
            WEBSITE='WEBSTAGING'
        else:
            MID=str(input("Enter MID : "))
            MERCHANT_KEY=str(input("Enter MERCHANT_KEY : "))
            CHANNEL_ID=str(input("Enter CHANNEL_ID : "))
            WEBSITE=str(input("Enter WEBSITE : "))

        print('REDIS configuration : \n Press 1 for default (Recommended), or Press 2 for manually entering.')
        ch_5 = int(input())
        if (ch_5 == 1):
            REDIS_URL='redis://localhost:6379/0'
            print("REDIS_URL : " + REDIS_URL)
        else:
            REDIS_URL=str(input("Enter REDIS_URL : "))
            
        QUEUES=['default']
        BCRYPT_LOG_ROUNDS=5

        print("Configuration Done")

        print("Writing Environment Variables to .env")

        file = open(".env", "w")
        file.write(f"SECRET_KEY='{SECRET_KEY}'\n")
        file.write(f"SQLALCHEMY_DATABASE_URI='{SQLALCHEMY_DATABASE_URI}'\n")
        file.write(f"MAIL_USERNAME='{MAIL_USERNAME}'\n")
        file.write(f"MAIL_PASSWORD='{MAIL_PASSWORD}'\n")
        file.write(f"MAIL_SERVER='{MAIL_SERVER}'\n")
        file.write(f"MAIL_PORT={MAIL_PORT}\n")
        file.write(f"MAIL_USE_SSL={MAIL_USE_SSL}\n")
        file.write(f"MAIL_USE_TLS={MAIL_USE_TLS}\n")
        file.write(f"MAIL_DEFAULT_SENDER='{MAIL_DEFAULT_SENDER}'\n")
        file.write(f"MID='{MID}'\n")
        file.write(f"MERCHANT_KEY='{MERCHANT_KEY}'\n")
        file.write(f"CHANNEL_ID='{CHANNEL_ID}'\n")
        file.write(f"WEBSITE='{WEBSITE}'\n")
        file.write(f"REDIS_URL='{REDIS_URL}'\n")
        file.write(f"QUEUES={QUEUES}\n")
        file.write(f"BCRYPT_LOG_ROUNDS={BCRYPT_LOG_ROUNDS}\n")

        file.close()

        print("Environment Variables Sucessfully Written")

if __name__ == '__main__':
    set_envvars()