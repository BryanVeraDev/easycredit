FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
#COPY requirements/* /app/
RUN pip install -r requirements.txt

COPY . /app/