from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import cred

account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)


# main message class


class Message:
    message_type = "sms"
    content = ""
    sid = ""
    number = ""

    MMS_num_media = 0
    MMS_content_type = ""

    # respond with sms

    def send_sms(self, content):

        client.messages \
            .create(
            body=content,
            from_=cred.get_number(),
            to=self.number

        )

    # respond with mms

    def send_mms(self, content, URL):
        client.messages \
            .create(
            body=content,
            from_=cred.get_number(),
            media_url=[URL],
            to=self.number
        )

    # delete message

    def mark_as_read(self):
        try:
            client.messages(self.sid).delete()
        except TwilioRestException:
            client.messages(self.sid) \
                .update(body="***")


# get all undeleted messages

def get_unread_messages():
    response = []
    messages = client.messages.list(
        to=cred.get_number(),
        limit=20
    )
    for message in messages:
        if message.body != "***":
            msg = Message()
            msg.content = message.body
            msg.number = message.from_
            msg.sid = message.sid
            msg.MMS_num_media = message.num_media
            if message.num_media != "0":
                msg.message_type = "mms"

            response.append(msg)
        else:
            mark_as_read(message.sid)
    return response


def send_sms(content, to):
    client.messages \
        .create(
        body=content,
        from_=cred.get_number(),
        to=to
    )


def send_mms(content, to, URL):
    client.messages \
        .create(
        body=content,
        from_=cred.get_number(),
        media_url=[URL],
        to=to
    )


def mark_as_read(sid):
    try:
        client.messages(sid).delete()
    except TwilioRestException:
        client.messages(sid) \
            .update(body="***")
