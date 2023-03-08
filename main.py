import defs as client
import time


while True:
    messages = client.get_unread_messages()
    for message in messages:
        print(message.message_type)
    time.sleep(.3)
