import defs as client
import time


while True:
    messages = client.get_unread_messages()
    for message in messages:
        print(message.content)
    time.sleep(.3)
