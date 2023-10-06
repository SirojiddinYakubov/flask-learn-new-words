FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y netcat vim make

WORKDIR /code_
ENV PYTHONPATH "${PYTHONPATH}:/code_/app:/code_"

COPY deploy/requirements.txt /

RUN #pip install --upgrade pip && pip install -r requirements.txt

COPY ../code_ /code_
COPY deploy/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]