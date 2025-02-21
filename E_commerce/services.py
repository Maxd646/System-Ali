from twilio.rest import Client
from django.conf import settings

def send_sms(to_phone_number, message):
    """ Sends an SMS using Twilio """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone_number
        )
        return sms.sid
    except Exception as e:
        return str(e)
