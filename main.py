import credentials
from defs import Client
import time

client = Client(credentials.twilio_get_number(), credentials.twilio_get_sid(), credentials.twilio_get_auth())


while True:

    # get list of unread messages

    messages = client.get_unread_messages()

    # for each message in messages

    for message in messages:

        # prints sms or mms
        message.send_sms("hello world!")

    # change this number for more frequent checks
    time.sleep(.5)
