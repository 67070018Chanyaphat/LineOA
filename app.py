from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import sys
import re

app = Flask(__name__)

def check_env_vars():
    required_vars = ['LINE_CHANNEL_ACCESS_TOKEN', 'LINE_CHANNEL_SECRET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"ERROR: Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

check_env_vars()

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
    user_message = event.message.text.lower()
    
    if "สวัสดี" in user_message:
        reply_text = """สวัสดีค่ะ/ครับ
นี่คือช่องทางติดต่ออย่างเป็นทางการและประชาสัมพันธ์ข่าวสารขององค์การนักศึกษา สจล."""

    elif "ติดต่อองค์การ" in user_message:
        reply_text = "รอตอบกลับจากองค์การนักศึกษาภายในเวลาทำการค่ะ/ครับ"

    elif "ช่องทางติดต่อ" in user_message:
        reply_text = """นี่คือช่องทางติดต่อของเรา
IG : https://www.instagram.com/sor.kmitlofficial
FB : https://www.facebook.com/sorkmitl
Tiktok : https://www.tiktok.com/@sorkmitlofficial"""
    elif "เดินทาง" in user_message:
        reply_text = """⁉️ วิธีเดินทางมายัง สจล. ง่ายๆแบบนี้เลย 🤔
🚂 รถไฟ ลงป้าย "หยุดรถไฟพระจอมเกล้า"
ตรวจสอบเวลาการเดินรถไฟ https://www.railway.co.th/SRTTimetable/StationListl
🚌 ขนส่งสาธารณะ รถเมล์ รถสองแถว รถตู้
ตรวจสอบสายรถ https://www.facebook.com/share/16i3DzyvUd/?mibextid=wwXIfr"""
    elif re.search(r"^first\s*step$" in user_message, re.IGNORECASE):
        reply_text = "รอติดตามประกาศเร็วๆนี้ ได้ที่ช่องทางประชาสัมพันธ์ขององค์การนักศึกษาได้เลย ‼️🥰"
    
    elif "รับน้อง" in user_message:
        reply_text = "รอติดตามประกาศเร็วๆนี้ ได้ที่ช่องทางประชาสัมพันธ์ของ องค์การนักศึกษาได้เลย ‼️🥰"
    elif "เร็ว" in user_message:
        reply_text = "ก็ต้องเป็นกิจกรรม First Step ยังไงล่ะ ชาวสจล.!! 🥰🌟"
    elif "ยังไง" in user_message or "อย่างไร" in user_message:
        reply_text = """ต้องการความช่วยเหลืออยู่หรือเปล่า 🤗
        📃 วิธีขอใบ Transcript 
            > https://drive.google.com/file/d/1DgA1IkmQmq7UuGDmEhbK33lSfmRXCPvY/view?usp=sharing
        ⌚ วิธีเช็คชั่วโมงกิจกรรม
            > https://drive.google.com/file/d/1T7AxhDnNPS1Vde67tFGmrEZCLs1j2-df/view?usp=sharing
        """
    

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
