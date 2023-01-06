from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)


def _send_otp(phone_number):
    verify.verifications.create(to=str('+91') + phone_number, channel='sms')


def _verify_otp(phone_number, code):
    try:
        result = verify.verification_checks.create(to=str('+91')+phone_number, code=code)
    except TwilioRestException:
        return False
    return result.status == 'approved'
