from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import credentials
import requests
import json
import mimetypes

# create base twilio client

twilio_client = Client(credentials.twilio_get_sid(), credentials.twilio_get_auth())


# main message class


class Message:

    message_type = ""  # sms or mms
    content = ""  # message body
    sid = ""  # ID of message
    number = ""  # number of who sent message

    # this is for internal use only
    beta_uri = ""

    # respond with sms

    def send_sms(self, content):

        twilio_client.messages \
            .create(
                body=content,
                from_=credentials.twilio_get_number(),
                to=self.number

            )

    # respond with mms

    def send_mms(self, content, url):
        twilio_client.messages \
            .create(
                body=content,
                from_=credentials.twilio_get_number(),
                media_url=[url],
                to=self.number
            )

    # delete message

    def mark_as_read(self):
        try:
            twilio_client.messages(self.sid).delete()
        except TwilioRestException:
            twilio_client.messages(self.sid) \
                .update(body="***")

    # download message

    def mv(self, file_path):

        string1 = f"https://api.twilio.com{self.beta_uri}"
        string1 = f"{string1[:-5]}/Media{string1[-5:]}"
        r = requests.get(string1, auth=(credentials.twilio_get_sid(), credentials.twilio_get_auth()))
        r = json.loads(r.text)
        r = r["media_list"][0]
        sid = r["sid"]
        mime_type = r["content_type"]
        print(r["content_type"])
        media_url = f"{string1[:-5]}/{sid}"
        r2 = requests.get(media_url)

        with open(f'{file_path}{mimetypes.guess_extension(mime_type, strict=True)}', 'wb') as handler:
            handler.write(r2.content)


# get all unread messages

def get_unread_messages():
    response = []
    messages = twilio_client.messages.list(
        to=credentials.twilio_get_number(),
        limit=20
    )
    for message in messages:
        if message.body != "***":
            msg = Message()
            msg.content = message.body
            msg.number = message.from_
            msg.sid = message.sid

            msg.beta_uri = message.uri
            if message.num_media != "0":
                msg.message_type = "mms"
            else:
                msg.message_type = "sms"

            response.append(msg)
        else:
            mark_as_read(message.sid)
    return response


def send_sms(content, to):
    twilio_client.messages \
        .create(
            body=content,
            from_=credentials.twilio_get_number(),
            to=to
        )


def send_mms(content, to, url):
    twilio_client.messages \
        .create(
            body=content,
            from_=credentials.twilio_get_number(),
            media_url=[url],
            to=to
        )


def mark_as_read(sid):
    try:
        twilio_client.messages(sid).delete()
    except TwilioRestException:
        twilio_client.messages(sid) \
            .update(body="***")
