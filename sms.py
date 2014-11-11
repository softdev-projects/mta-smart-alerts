from twilio.rest import TwilioRestClient

account_sid = "PNc7a6199f75736a4291760f00695b233c"
auth_token  = ""
client = TwilioRestClient(account_sid, auth_token)
 
def send_message(message="hardcoded",number=9174350162):
    message = client.messages.create(body=message,
    to="+" + str(number),
    from_="+4694782929")
    print message.sid
