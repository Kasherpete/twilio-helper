import asyncio

import twilio.rest
from twilio.base.exceptions import TwilioRestException
import credentials
import requests
import json
import mimetypes
import time

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

    def send_sms(self, content: str):
        twilio_client.messages.create(
            body=content,
            from_=self.message_to,
            to=self.number

        )

    # respond with mms

    def send_mms(self, content: str, path: str):
        twilio_client.messages.create(
            body=content,
            from_=self.message_to,
            media_url=[path],
            to=self.number
        )

    def send_multiple_mms(self, content: str, paths: list):
        twilio_client.messages.create(
            body=content,
            from_=self.message_to,
            media_url=paths,
            to=self.number
        )

    # delete message

    def mark_as_read(self):

        try:

            # if server has not received changes
            twilio_client.messages(self.sid).delete()

        except TwilioRestException:

            if self.sid not in dummy_list:

                # append to delete list
                dummy_list.append(self.sid)

    # download message

    def MMS_mv(self, file_name: str):

        # get uri link
        string1 = f"https://api.twilio.com{self.beta_uri}"
        # parse
        string1 = f"{string1[:-5]}/Media{string1[-5:]}"

        # get media link
        r = requests.get(string1, auth=(self.account_sid, self.account_auth))
        r = json.loads(r.text)
        # parse
        r = r["media_list"][0]  # gets first media found, TODO: make multiple MMS receiving - Message
        sid = r["sid"]
        mime_type = r["content_type"]
        media_url = f"{string1[:-5]}/{sid}"

        # gets media data
        r2 = requests.get(media_url)

        # finally download
        with open(f'{file_name}{mimetypes.guess_extension(mime_type, strict=True)}', 'wb') as handler:
            handler.write(r2.content)

    def MMS_raw_data(self):

        # get uri link
        string1 = f"https://api.twilio.com{self.beta_uri}"
        # parse
        string1 = f"{string1[:-5]}/Media{string1[-5:]}"

        # get media link
        r = requests.get(string1, auth=(self.account_sid, self.account_auth))
        r = json.loads(r.text)
        # parse
        r = r["media_list"][0]  # first media found, see above
        sid = r["sid"]
        mime_type = r["content_type"]

        # get data
        media_url = f"{string1[:-5]}/{sid}"
        r2 = requests.get(media_url)

        return r2.content, mime_type

    def ask(self, question: str, timeout: int = 60, default: str = "", advanced: bool = False):

        # init
        client = Client(credentials.twilio_get_number(), credentials.twilio_get_sid(), credentials.twilio_get_auth())
        timer_timeout = time.perf_counter()
        self.send_sms(question)

        # while timer not out
        while time.perf_counter() - timer_timeout <= timeout:
            time.sleep(1)
            new_messages = client.get_unread_messages(
                6)  # idk why I make it this number, it seems best for high capacity

            for message in new_messages:

                # if from actual user
                if message.number == self.number:
                    message.mark_as_read()
                    if advanced:
                        # return message class
                        return message
                    else:
                        # return message data
                        return message.content

        # timeout error messages - delete if u want

        time.sleep(1)
        if default != "":
            self.send_sms(f'ERROR:TIMEOUT. User took too long to respond. Default response: {default}.')
        else:
            self.send_sms("ERROR:TIMEOUT. User took too long to respond. Please use command again to retry.")

        return default

    async def async_ask(self, question: str, timeout: int = 60, default: str = "", advanced: bool = False):

        # init
        client = Client(credentials.twilio_get_number(), credentials.twilio_get_sid(), credentials.twilio_get_auth())
        timer_timeout = time.perf_counter()
        self.send_sms(question)

        # while message not received
        while time.perf_counter() - timer_timeout <= timeout:
            await asyncio.sleep(1)
            new_messages = client.get_unread_messages(
                6)  # idk why I make it this number, it seems best for high capacity

            for message in new_messages:

                # if from actual user
                if message.number == self.number:
                    message.mark_as_read()
                    if advanced:
                        # return message class
                        return message
                    else:
                        # return message data
                        return message.content

        # timeout error messages, again see above

        await asyncio.sleep(1)
        if default != "":
            self.send_sms(f'ERROR:TIMEOUT. User took too long to respond. Default response: {default}.')
        else:
            self.send_sms("ERROR:TIMEOUT. User took too long to respond. Please use command again to retry.")

        return default


class Client:
    number = ""
    sid = ""
    auth = ""

    def __init__(self, number: str, sid: str, auth: str):
        self.number = number
        self.sid = sid
        self.auth = auth

    def get_unread_messages(self, list_count: int = 20):
        response = []
        messages = twilio_client.messages.list(
            to=self.number,
            limit=list_count
        )
        for message in messages:
            if message.sid not in dummy_list:  # if the message should be deleted, see mark_as_read()
                # assign values to Message class
                msg = Message()
                msg.content = message.body
                msg.number = message.from_
                msg.sid = message.sid
                msg.message_to = message.to
                msg.account_auth = self.auth
                msg.account_sid = self.sid

                # message type
                msg.beta_uri = message.uri
                if message.num_media != "0":
                    msg.message_type = "mms"
                else:
                    msg.message_type = "sms"

                response.append(msg)
            else:
                dummy_list.remove(message.sid)
                self.mark_as_read(message.sid)

        # return list of Message objects
        return response

    def send_sms(self, content: str, to: str):
        twilio_client.messages.create(
            body=content,
            from_=self.number,
            to=to
        )

    def send_mms(self, content: str, to: str, path: str):
        twilio_client.messages.create(
            body=content,
            from_=self.number,
            media_url=[path],
            to=to
        )

    def send_multiple_mms(self, content: str, to: str, paths: list):
        twilio_client.messages.create(
            body=content,
            from_=self.number,
            media_url=paths,
            to=to
        )

    def mark_as_read(self, sid):

        try:
            # if server has not received changes
            twilio_client.messages(sid).delete()
        except TwilioRestException:

            if sid not in dummy_list:
                # add to delete/ignore list until changes received by server
                dummy_list.append(sid)

    def mark_all_read(self, number: int = 200):

        messages = self.get_unread_messages(number)
        for message in messages:
            message.mark_as_read()

    async def async_ask(self, question: str, msg: Message, timeout: int = 60, default: str = "",
                        advanced: bool = False):
        timer_timeout = time.perf_counter()
        msg.send_sms(question)

        while time.perf_counter() - timer_timeout <= timeout:
            await asyncio.sleep(1)
            new_messages = self.get_unread_messages(
                6)  # idk why I make it this number, it seems best for high capacity

            for message in new_messages:

                if message.number == msg.number:
                    message.mark_as_read()
                    if advanced:
                        return message
                    else:
                        return message.content

        # timeout error messages

        await asyncio.sleep(1)
        if default != "":
            msg.send_sms(f'ERROR:TIMEOUT. User took too long to respond. Default response: {default}.')
        else:
            msg.send_sms("ERROR:TIMEOUT. User took too long to respond. Please use command again to retry.")

        return default

    def ask(self, question: str, msg: Message, timeout: int = 60, default: str = "", advanced: bool = False):
        timer_timeout = time.perf_counter()
        msg.send_sms(question)

        while time.perf_counter() - timer_timeout <= timeout:
            time.sleep(1)
            new_messages = self.get_unread_messages(
                6)  # idk why I make it this number, it seems best for high capacity

            for message in new_messages:

                if message.number == msg.number:
                    message.mark_as_read()
                    if advanced:
                        return message
                    else:
                        return message.content

        # timeout error messages

        time.sleep(1)
        if default != "":
            msg.send_sms(f'ERROR:TIMEOUT. User took too long to respond. Default response: {default}.')
        else:
            msg.send_sms("ERROR:TIMEOUT. User took too long to respond. Please use command again to retry.")

        return default
