from twilio.rest import TwilioRestClient

account_sid = "ACb57be35ea472d5288dfdc25aa8da9b27"
auth_token  = ""
client = TwilioRestClient(account_sid, auth_token)

 
def send_message(message="hardcoded",number=9174350162):
    message = client.messages.create(body=message,
    to="+1" + str(number),
    from_="+14694782929")
    print message.sid

