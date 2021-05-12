FROM python:3.8

RUN mkdir -p /home/app
RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTOCODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chown -R app:app $APP_HOME

USER app

CMD ["python", "manage.py", "wait_db.py"]
