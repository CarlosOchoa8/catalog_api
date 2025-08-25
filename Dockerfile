FROM python:3.13-slim as builder

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get clean \
    && apt-get -y install libpq-dev curl

# DBMATE
RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
RUN chmod +x /usr/local/bin/dbmate

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV TZ="America/Mexico_City"

COPY . .

CMD ["sh", "-c", "python -m scripts.db_init && uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload"]
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
