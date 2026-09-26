FROM python:3.11-slim

LABEL name="南无那面 · 仁格智能体"
LABEL description="凡我所算，以仁为界。凡我所向，南无那面。"
LABEL version="1.0.0"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN mkdir -p /app/data

ENV PORT=5000
EXPOSE 5000

CMD ["python", "src/api/server.py"]