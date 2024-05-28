from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
to_phone_number = os.getenv('TO_PHONE_NUMBER')

twilio_client = Client(twilio_sid, twilio_auth_token)