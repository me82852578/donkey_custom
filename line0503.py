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

line_bot_api = LineBotApi('0UFOoFnN2ddZVdnDWLS9gRFIu4xp3wAXxnSD4DIIe883xvJBcgVXRb/Rwwqr1sGIPpsvvu9dORgCTRl1Z9kYauD48OL0X3TResYkx8lTmPYBVyoCELSYE68aNv3kwNC5EfkHZVlrgNqxuONthir0qAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8dd0ccb984c1294f197e9b85e3707061')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    print(event)
    print('------')
    client_text = event.message.text

    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='好喔！為您{}'.format(client_text)))
    print(client_text)
    print('================')
    print(client_text[2])
    client_order = client_text[2]
    return client_order


if __name__ == "__main__":
    app.run()