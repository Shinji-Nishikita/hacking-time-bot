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
from time import time

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


# start = 0
users = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    if event.message.text == "start hacking":
        reply_message = "measuring hacking time"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0
        users[userId]["start"] = time()
    else:
        end = time()
        dif = int(end - users[userId]["start"])
        users[userId]["total"] += dif
        hour = dif // 3600
        minute = (dif % 3600) // 60
        second = dif % 60
        totalhour = users[userId]["total"] // 3600
        totalminutes = (users[userId]["total"] % 3600) // 60 
        totalseconds = users[userId]["total"] % 60
        # reply_message = f"Hacking time is { hour }hour{ minute }minutes{ second }seconds. Total hacking time is {users[userId]['total']}seconds"
        reply_message = f"Hacking time is { hour }hour{ minute }minutes{ second }seconds. Total hacking time is { totalhour }hour{ totalminutes }minutes{ totalseconds }seconds."

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message))

if __name__ == "__main__":
    app.run()
    

