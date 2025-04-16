from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

# ==============================================
# ตรวจสอบ Environment Variables ที่จำเป็น
# ==============================================
required_vars = {
    "LINE_CHANNEL_ACCESS_TOKEN": "IHErWa6KxebYvT3R+hgdMp4I9zBAahIcrWoEZXLkOzJ7nalwgaskBvebUIoptdxgBBtovbd8x5o3k5nM/opU/5b0cgjgj7dpZolsQFJZyEl1+WURADioULaIrrtbB9ZDu5QVh6GrK9DdbL/an/IP+QdB04t89/1O/w1cDnyilFU=",
    "LINE_CHANNEL_SECRET": "fd557f38c164797fe7daf1eb5857c4de"
}

for var, description in required_vars.items():
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {description} ({var})")

# ==============================================
# กำหนดค่าจาก Environment Variables
# ==============================================
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
port = int(os.environ.get("PORT", "8000"))  # ใช้พอร์ต 8000 เป็นค่า default

# ==============================================
# เริ่มต้น Flask Application
# ==============================================
app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# ==============================================
# Webhook Endpoint
# ==============================================
@app.route("/webhook", methods=['POST'])
def webhook():
    # ตรวจสอบ Signature
    signature = request.headers['X-Line-Signature']
    
    # รับข้อมูลจาก LINE
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    
    return 'OK'

# ==============================================
# ตัวจัดการข้อความ
# ==============================================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip().lower()
    
    if user_message == "สวัสดี":
        reply_text = "สวัสดี! นี่คือช่องทางติดต่อองค์การนักศึกษา สจล."
    else:
        reply_text = "ขอโทษครับ ผมไม่เข้าใจคำถาม"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

# ==============================================
# เริ่มต้นเซิร์ฟเวอร์
# ==============================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)