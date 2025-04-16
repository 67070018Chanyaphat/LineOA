FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# ใช้วิธีที่ 2 (ง่ายและครอบคลุม)
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-8000}"]