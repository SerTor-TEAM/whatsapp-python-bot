from flask import Flask, request

from wabot import WABot

app = Flask(__name__)

bot = WABot(request.json)


@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST': return bot.processing()


if __name__ == '__main__':
    app.run()
