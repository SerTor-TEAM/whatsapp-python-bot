import datetime
from json import dumps

import requests


class WABot:
    token = 'abcdefg'
    APIUrl = 'https://eu41.chat-api.com/instance12345/'

    def __init__(self, json: dict):
        self.json = json
        self.dict_messages = json['messages']

        self.functions = dict()

    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatID, text):
        data = {"chatID": chatID,
                "body": text}
        answer = self.send_requests('sendMessage', data)
        return answer

    def register_function_decorator(self, name):
        def register_function_decorator_inside(function):
            self.functions.update({name: function})
            return function

        return register_function_decorator_inside

    def Router(self):
        @self.register_function_decorator("hi")
        def welcome(message: object, noWelcome=False):
            welcome_string = """Incorrect command
Commands:
1. chatid - show ID of the current chat
2. time - show server time
3. me - show your nickname
4. file [format] - get a file. Available formats: doc/gif/jpg/png/pdf/mp3/mp4
5. ptt - get a voice message
6. geo - get a location
7. group - create a group with the bot"""
            return self.send_message(message['chatId'], "WhatsApp Demo Bot Python\n" if not noWelcome else welcome_string)

        @self.register_function_decorator("time")
        def time(message: object):
            return self.send_message(message['chatId'], datetime.datetime.now().strftime('%d:%m:%Y'))

        @self.register_function_decorator("chatid")
        def show_chat_id(message):
            return self.send_message(message['chatId'], f"Chat ID : {message['chatId']}")

        @self.register_function_decorator("me")
        def me(message):
            return self.send_message(message['chatId'], message['senderName'])

        @self.register_function_decorator("file")
        def file(message):
            availableFiles = {'doc': 'document.doc',
                              'gif': 'giffile.gif',
                              'jpg': 'jpgfile.jpg',
                              'png': 'pngfile.png',
                              'pdf': 'presentation.pdf',
                              'mp4': 'video.mp4',
                              'mp3': 'mp3file.mp3'}
            if message['body'].split()[1] in availableFiles.keys():
                data = {
                    'chatId': message['chatId'],
                    'body': f"https://domain.com/Python/{availableFiles[message['body'].split()[1]]}",
                    'filename': availableFiles[message['body'].split()[1]],
                    'caption': f"'Get your file {availableFiles[message['body'].split()[1]]}'"
                }
                return self.send_requests('sendFile', data)

        @self.register_function_decorator("ptt")
        def ptt(message):
            data = {
                "audio": 'https://domain.com/Python/ptt.ogg',
                "chatId": message['chatId']}
            return self.send_requests('sendAudio', data)

        @self.register_function_decorator("geo")
        def geo(message):
            data = {
                "lat": '51.51916',
                "lng": '-0.139214',
                "address": 'Your address',
                "chatId": message['chatId']
            }
            answer = self.send_requests('sendLocation', data)
            return answer

        @self.register_function_decorator("group")
        def group(message):
            phone = message['author'].replace('@c.us', '')
            data = {
                "groupName": 'Group with the bot Python',
                "phones": phone,
                'messageText': 'It is your group. Enjoy'
            }
            answer = self.send_requests('group', data)
            return answer

    def processing(self):
        if self.dict_messages:
            for message in self.dict_messages:
                text = message['body'].split()
                if not message['fromMe']: return self.functions.get(text[0].lower())(message) if text[0].lower() in self.functions.keys() else self.functions.get("hi")(message, True)

                return 'No command found'
