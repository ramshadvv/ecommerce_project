from django.conf import settings
from twilio.rest import Client
import random

class MessageHandler:
    phone_number=None
    otp=None
    def __init__(self, phone_number, otp):
        self.phone_number = phone_number
        self.otp = otp
    
    def send_otp_phone(self):
        # account_sid = os.environ['TWILIO_ACCOUNT_SID']
        # auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

        message = client.messages.create(
                                    body=f'Your otp is {self.otp}',
                                    from_='+8586306903',
                                    to=self.phone_number
                                )

        print(message.sid)