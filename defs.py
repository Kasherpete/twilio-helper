import twilio.rest
from twilio.base.exceptions import TwilioRestException
import credentials
import requests
import json
import mimetypes

# create base twilio client. Put in your own credentials

twilio_client = twilio.rest.Client(credentials.twilio_get_sid(), credentials.twilio_get_auth())


dummy_list = []  # DO NOT REMOVE

# main message class


class Message:

    message_type = ""  # sms or mms
    content = ""  # message body
    sid = ""  # ID of message
    number = ""  # number of who sent message
    message_to = ""  # number of whom the msg was sent to
    account_auth = ""  # auth key of account
    account_sid = ""  # sid key of account


    # this is for internal use only
    beta_uri = ""

    # respond with sms

    def send_sms(self, content):
        twilio_client.messages \
            .create(
                body=content,
                from_=self.message_to,
                to=self.number

            )

    # respond with mms

    def send_mms(self, content, url):
        twilio_client.messages \
            .create(
                body=content,
                from_=self.message_to,
                media_url=[url],
                to=self.number
            )

    # delete message

    def mark_as_read(self):

        try:
            twilio_client.messages(self.sid).delete()
        except TwilioRestException:

            if self.sid not in dummy_list:
                dummy_list.append(self.sid)

            # twilio_client.messages(self.sid).update(body="")

    # download message

    def MMS_mv(self, file_name):

        string1 = f"https://api.twilio.com{self.beta_uri}"
        string1 = f"{string1[:-5]}/Media{string1[-5:]}"
        r = requests.get(string1, auth=(self.account_sid, self.account_auth))
        r = json.loads(r.text)
        r = r["media_list"][0]
        sid = r["sid"]
        mime_type = r["content_type"]
        # print(r["content_type"])
        media_url = f"{string1[:-5]}/{sid}"
        r2 = requests.get(media_url)

        with open(f'{file_name}{mimetypes.guess_extension(mime_type, strict=True)}', 'wb') as handler:
            handler.write(r2.content)

    def MMS_raw_data(self):
        string1 = f"https://api.twilio.com{self.beta_uri}"
        string1 = f"{string1[:-5]}/Media{string1[-5:]}"
        r = requests.get(string1, auth=(self.account_sid, self.account_auth))
        r = json.loads(r.text)
        r = r["media_list"][0]
        sid = r["sid"]
        mime_type = r["content_type"]

        media_url = f"{string1[:-5]}/{sid}"
        r2 = requests.get(media_url)

        return r2.content, mime_type



class Client:
    number = ""
    sid = ""
    auth = ""

    def __init__(self, number, sid, auth):
        self.number = number
        self.sid = sid
        self.auth = auth

    def get_unread_messages(self, list_count=20):
        response = []
        messages = twilio_client.messages.list(
            to=self.number,
            limit=list_count
        )
        for message in messages:
            if message.sid not in dummy_list:
                msg = Message()
                msg.content = message.body
                msg.number = message.from_
                msg.sid = message.sid
                msg.message_to = message.to
                msg.account_auth = self.auth
                msg.account_sid = self.sid

                msg.beta_uri = message.uri
                if message.num_media != "0":
                    msg.message_type = "mms"
                else:
                    msg.message_type = "sms"

                response.append(msg)
            else:
                dummy_list.remove(message.sid)
                self.mark_as_read(message.sid)
        return response


    def send_sms(self, content, to):
        twilio_client.messages \
            .create(
                body=content,
                from_=self.number,
                to=to
            )


    def send_mms(self, content, to, url):
        twilio_client.messages \
            .create(
                body=content,
                from_=self.number,
                media_url=[url],
                to=to
            )


    def mark_as_read(self, sid):
        try:
            twilio_client.messages(sid).delete()
        except TwilioRestException:

            if sid not in dummy_list:
                dummy_list.append(sid)

    def mark_all_read(self):
        messages = self.get_unread_messages()
        for message in messages:
            message.mark_as_read()
