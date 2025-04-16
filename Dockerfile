FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# ใช้วิธีที่ 2 (ง่ายและครอบคลุม)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]  # ใช้พอร์ต 8000