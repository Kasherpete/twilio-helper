# Usage:

How to create client:

    from defs import Client

    client = Client(your_number, account_sid, auth_token)

Client methods:

    # note that message sid is different from account sid
    client.mark_as_read(message_sid)

    client.send_sms("Hello World!", number)

    client.send_mms("Hellow World!", number, url_of_media)

    # returns a list of class Messages (see below)
    client.get_unread_messages()

Message Class, properties, usages:

    messages = client.get_unread_messages()

    for msg in messages:

        # properties

        print(msg.content)  # body of message
        print(msg.number)  # number of who sent the message
        print(msg.message_type)  # returns either "sms" or "mms"
        print(msg.sid)  # returns the SID of that specific message



        # methods

        # sends a sms message to the number that sent the message
        msg.send_sms("Hello World!")
        msg.send_mms("hello World!", url_of_media)

        msg.mark_as_read()



        # these are only for MMS messages

        # downloads the media. DO NOT include extension, like .png or .jpg
        MMS_mv(file_name)
        
        # a list - first element is raw data, second element is mime-type
        MMS_raw_data()

Setting up credentials:

You will need to have a separate file called credentials.py that contains the keys and your number. The client does not
depend on them, but the Message class does. This is being worked on but for now, just include the following
code in credentials.py:

    def twilio_get_number():
    my_number = ""
    return my_number


    def twilio_get_sid():
    account_sid = ""
    return account_sid


    def twilio_get_auth():
    auth_token = ""
    return auth_token
