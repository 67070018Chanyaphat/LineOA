from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import sys

app = Flask(__name__)

# ตรวจสอบ Environment Variables ก่อนเริ่มทำงาน
def check_env_vars():
    required_vars = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"ERROR: Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

check_env_vars()

# เริ่มใช้งาน LINE API
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

@app.route("/", methods=['GET'])
def home():
    return "LINE Bot is running!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.lower()  # แปลงเป็นตัวเล็กทั้งหมดเพื่อตรวจสอบง่าย
    
    if "สวัสดี" in user_message:
        reply_text = """สวัสดีค่ะ/ครับ
        นี่คือช่องทางติดต่ออย่างเป็นทางการและประชาสัมพันธ์ข่าวสารขององค์การนักศึกษา สจล.
        สามารถติดตามข่าวสารได้ที่ :
        - Facebook: องค์การนักศึกษา KMITL
        - Instagram: sor.kmitlofficial"""
    
    elif "ข่าวสารล่าสุด" in user_message:
        reply_text = ""ผู้อัญเชิญพระมหามงกุฎและฉัตรปริวาร ประจำปี 2568 
        www.instagram.com/p/DGvgOCaB1qL""
    
    else:
        reply_text = "หากต้องการติดต่อองค์การนักศึกษาโดยตรง สามารถทิ้งข้อความแล้วรอตอบกลับในเวลาทำการค่ะ/ครับ"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
