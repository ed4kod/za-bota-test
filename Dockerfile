FROM python:3.11-slim

WORKDIR /bot

COPY . .

RUN pip install -e .

CMD ["python", "-m", "bot"]