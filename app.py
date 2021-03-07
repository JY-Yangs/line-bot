# 使用line官方的SDK (software development kit)
# https://github.com/line/line-bot-sdk-python

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

app = Flask(__name__)

line_bot_api = LineBotApi('uC6kgDCV1m8wA4TnPw4Czkzj0pB8RWLykGzn9kL9j33W2bcylmWGOqvn3KIH2fHUFW0X/QBl/b4FixNluoQWCX7+fcOTjR32v3/Xq5mCpY4hBEQN8EbaoWB1RH1bjHFadoAnmdtFmDYGWq6mRUNXrAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a20d40f80aa0dddd7f3fb519cacf3785')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text # 使用者傳過來的訊息
    r = '很抱歉，您說什麼'

    if msg == 'hi':
        r = 'hi'
    elif msg == '你吃飯了嗎':
        r = '還沒'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()