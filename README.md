# Setup:
### How to create client:

```python
from defs import Client

# replace with credentials. I recommend doing Credentials.twilio_get_sid, etc.
client = Client("your_number", "account_sid", "auth_token")

```
**_You also need to update the client used in defs.py_**:
```python
import twilio.rest

# twilio.rest.Client() is different that Client()
twilio_client = twilio.rest.Client("twilio_sid", "twilio_auth")
```
After these two things are done, you are pretty much ready to start using and modifying the code.
# Usage
### Client methods, Properties, and Usages:

```python
from defs import Client


# Methods


client = Client("number", "sid", "auth")  # details above


# E.164 formatted number. (123)-456-7890 would be +11234567890
client.send_sms("Hello World!", "+11234567890")  # send sms


client.send_mms("Hello World!", "+11234567890", "media_url")  # send mms


# returns list of class Messages, details below
client.get_unread_messages("optional number")


# marks all unread messages as read
client.mark_all_read()


# marks a message as read. message_sid explained below
client.mark_as_read("message_sid")


# properties


print(client.number)  # client assigned phone number

print(client.sid)  # client assigned account sid

print(client.auth)  # client assigned auth token
```

### Message Class, Properties, and Usages:
```python
from defs import Client

client = Client("your_number", "account_sid", "auth_token")

messages = client.get_unread_messages()

for msg in messages:

    
# properties

    
    print(msg.content)  # body of message
    print(msg.number)  # number of who sent the message
    print(msg.message_type)  # returns either "sms" or "mms"
    print(msg.sid)  # returns the SID of that specific message
    print(msg.message_to)  # returns number of the one who received message
    print(msg.account_auth)  # returns account auth of client that handled message
    print(msg.account_sid)  # returns account sid of client that handled message


 # methods

    
    # sends a sms or mms message to the number that sent the message
    msg.send_sms("Hello World!")
    msg.send_mms("hello World!", "url_of_media")

    msg.mark_as_read()  # mark message as read



    # these are only for MMS messages

    # downloads the media. DO NOT include extension, like .png or .jpg
    msg.MMS_mv("file_name")
    
    # a list - first element is raw data, second element is mime-type
    msg.MMS_raw_data()
```

# Setting Up Credentials:

You can either have the credentials hardcoded in, rely on environment variables, or use the following method. This
method involves you putting your credentials in functions that are contained in credentials.py. For example, your
twilio sid will go in twilio_get_sid.

```python
def twilio_get_number():
    my_number = ""  # number goes here
    return my_number


def twilio_get_sid():
    account_sid = ""  # sid
    return account_sid


def twilio_get_auth():
    auth_token = ""  #auth
    return auth_token
```

# Running Program:
A sample program is supplied in main.py. You can also use this code to help you get started:
```python
from defs import Client

client = Client("number", "sid", "auth")

messages = client.get_unread_messages()
for msg in messages:
    # if messages starts with !
    if msg.content[0] == "!":
        
        # if message is !help
        
        if msg.content == "!help":
            msg.send_sms("Help command activated.")
            
        # if message is !test
        
        elif msg.content == "!test":
            msg.send_sms("Program is running.")
        
```