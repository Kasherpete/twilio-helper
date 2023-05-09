import credentials
from defs import Client
import time

client = Client(credentials.twilio_get_number(), credentials.twilio_get_sid(), credentials.twilio_get_auth())


while True:

    # get list of unread messages

    messages = client.get_unread_messages()

    # for each message in messages

    for msg in messages:

        # all properties of Message class

        msg.send_sms(f"Hi, '{msg.number}'!")
        print(msg.sid)
        print(msg.account_sid)
        print(msg.account_auth)
        print(msg.message_to)
        print(msg.content)
        print(msg.number)
        print(msg.message_type)

        # mark as read

        msg.mark_as_read()  # pls remember this ;)


    # change this number for more frequent checks. I recommend this value for stability
    time.sleep(.5)
