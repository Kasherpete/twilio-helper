from defs import Client
import time

client = Client()

while True:

    # get list of unread messages

    messages = client.get_unread_messages()
    print("check")

    # for each message in messages

    for message in messages:

        # prints sms or mms
        print(message.message_type)

    # change this number for more frequent checks
    time.sleep(.3)
