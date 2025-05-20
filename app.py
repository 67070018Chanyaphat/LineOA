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

    elif "ติดต่อองค์การ" in user_message or "องค์การ" in user_message:
        reply_text = """รอตอบกลับจากองค์การนักศึกษาภายในเวลาทำการค่ะ/ครับ 
        สามารถทิ้งคำถาม หรือข้อสงสัยไว้ได้เลยย 🤗💖"""
    elif "ข่าวสาร" in user_message:
        reply_text = """ข่าวสารล่าสุด องค์การขอเสิร์ฟ 🥳
ประกาศผล การออกแบบเสื้องาน KMITL FIRST STEP 2025 : THE OCEAN ADVENTURE
> https://www.instagram.com/p/DJy3lbwT1zN/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="""

    elif "ช่องทางติดต่อ" in user_message:
        reply_text = """นี่คือช่องทางติดต่อของเรา
IG : https://www.instagram.com/sor.kmitlofficial
FB : https://www.facebook.com/sorkmitl
Tiktok : https://www.tiktok.com/@sorkmitlofficial"""
    elif "เดินทาง" in user_message:
        reply_text = """⁉️ วิธีเดินทางมายัง สจล. ง่ายๆแบบนี้เลย 🤔
🚂 รถไฟ ลงป้าย "หยุดรถไฟพระจอมเกล้า"
ตรวจสอบเวลาการเดินรถไฟ https://ttsview.railway.co.th/v3/
🚌 ขนส่งสาธารณะ รถเมล์ รถสองแถว รถตู้
ตรวจสอบสายรถ https://www.facebook.com/share/16i3DzyvUd/?mibextid=wwXIfr"""
    elif re.search(r"\bfirst\s*step\b", user_message, re.IGNORECASE):
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
    elif "ปฏิทิน" in user_message:
        reply_text = """🗓️ ปฏิทินกิจกรรมการศึกษา 
        > https://www.reg.kmitl.ac.th/educalendar/2568/th-2.pdf
ส่วนกิจกรรมสนุกๆ ภายในปีการศึกษา 2568 
กดติดตามช่องทางประชาสัมพันธ์ องค์การนักศึกษาไว้เลย
IG : https://www.instagram.com/sor.kmitlofficial
FB : https://www.facebook.com/sorkmitl
Tiktok : https://www.tiktok.com/@sorkmitlofficial
🥰🌟❤️‍🔥"""
    elif "เข็ม" in user_message or "ไท" in user_message or "ตุ้ง" in user_message or "กระดุม" in user_message:
        reply_text = """🤔⁉️ สำหรับน้องๆ นักศึกษาชั้นปีที่ 1 สามารถติดตามประกาศ การซื้อเครื่องหนังและเครื่องโลหะ ได้ที่ช่องทางประชาสัมพันธ์ของสโมสรนักศึกษา ที่สังกัดอยู่ได้เลย 
        
โดยพิมพ์ว่า สโม ในช่องแชทนี้ 
เพื่อรับช่องทางติดต่อสโมสรนักศึกษา ของแต่ละคณะ 🥳‼️"""
    elif "สภา" in user_message:
        reply_text = """ช่องทางติดต่อสภานักศึกษา 🌟
> https://www.instagram.com/kmitlsc/"""
    elif "สโม" in user_message:
        reply_text = """ช่องทางติดต่อสโมสรนักศึกษา 🌟
⚙️ สโมสรนักศึกษา คณะวิศวกรรมศาสตร์ หลักสูตรปกติ
> https://www.instagram.com/kmitl.esa.official/
⚙️ สโมสรนักศึกษา คณะวิศวกรรมศาสตร์ หลักสูตรต่อเนื่อง
> https://www.instagram.com/kmitl.ecsa/
📐 สโมสรนักศึกษา คณะสถาปัตยกรรม ศิลปะและการออกแบบ
> https://www.instagram.com/smo.archkmitl/
🖋️ สโมสรนักศึกษา คณะครุศาสตร์อุตสาหกรรม และเทคโนโลยี
> https://www.instagram.com/smo.kharusart.kmitl/
🌿 สโมสรนักศึกษา คณะเทคโนโลยีการเกษตร
> https://www.instagram.com/smoagritech.kmitl/
🧪 สโมสรนักศึกษา คณะวิทยาศาสตร์
> https://www.instagram.com/smoscience.kmitl/
💻 สโมสรนักศึกษา คณะเทคโนโลยีสารสนเทศ
> https://www.instagram.com/smo.itkmitl/
🍜 สโมสรนักศึกษา คณะอุตสาหกรรมอาหาร
> https://www.instagram.com/smofoodind.kmitl/
💵 สโมสรนักศึกษา คณะบริหารธุรกิจ
> https://www.instagram.com/smokbs.kmitl/
🦾 สโมสรนักศึกษา คณะเทคโนโลยีนวัตกรรมบูรณาการ
> https://www.instagram.com/smosiitec.kmitl/
✈️ สโมสรนักศึกษา วิทยาลัยอุตสาหกรรมการบินนานาชาติ
> https://www.instagram.com/smoiaai.kmitl/
🗣️ สโมสรนักศึกษา คณะศิลปศาสตร์
> https://www.instagram.com/smola_kmitl/
🩺 สโมสรนักศึกษา คณะแพทยศาสตร์
> https://www.instagram.com/smomdkmitl/
🎵 สโมสรนักศึกษา วิทยาลัยวิศวกรรมสังคีต
> https://www.instagram.com/smo.imse/
🦷 สโมสรนักศึกษา คณะทันตแพทยศาสตร์
> https://www.instagram.com/smodentkmitl/
"""
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
