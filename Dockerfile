# ต้องกำหนด Base Image ก่อนเสมอ (สำคัญที่สุด!)
FROM python:3.11-slim

# ตั้งค่า Working Directory
WORKDIR /app

# คัดลอก requirements.txt ก่อนเพื่อใช้ Docker cache
COPY requirements.txt .

# ติดตั้ง dependencies (ใช้คำสั่งนี้เพียงครั้งเดียว)
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมด
COPY . .

# คำสั่งรันแอป (สำคัญ!)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:$PORT"]