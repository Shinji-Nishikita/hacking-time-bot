import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/")
def test():
    return "Hello"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

from time import time
start = 0
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # userID = event.source.userID
    if event.message.text == "start hacking":
        reply_message = "measuring hacking time"
        global start
        start = time()
    else:
        end = time()
        dif = int(end - start)
        hour = dif // 3600
        minute = (dif % 3600) // 60
        second = dif % 60
        reply_message = f"hacking time is {hour}hour{minute}minutes{second}seconds"

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()
    

