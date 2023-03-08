import defs as client
import time
import random

while True:

    messages = client.get_unread_messages()
    print("check")
    for message in messages:
        print(message.message_type)



    time.sleep(.3)




