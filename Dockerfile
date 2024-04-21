FROM python:3.10-alpine

WORKDIR /Server

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

COPY . .

RUN apk update \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r  requirements.txt

CMD ["python3", "manage.py", "makemigrations"]