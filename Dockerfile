FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt python-dotenv

COPY backend/ .
COPY frontend/ ./frontend/

EXPOSE 8000

ENV MONGO_URI=mongodb://host.docker.internal:27017/

CMD ["python", "app.py"]
