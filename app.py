from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("IHErWa6KxebYvT3R+hgdMp4I9zBAahIcrWoEZXLkOzJ7nalwgaskBvebUIoptdxgBBtovbd8x5o3k5nM/opU/5b0cgjgj7dpZolsQFJZyEl1+WURADioULaIrrtbB9ZDu5QVh6GrK9DdbL/an/IP+QdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.getenv("fd557f38c164797fe7daf1eb5857c4de"))

@app.route("/webhook", methods=['POST'])
def webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if user_message == "สวัสดี":
        reply_text = "สวัสดี! นี่คือช่องทางติดต่อองค์การนักศึกษา สจล."
    else:
        reply_text = "ขอโทษครับ ผมไม่เข้าใจคำถาม"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
