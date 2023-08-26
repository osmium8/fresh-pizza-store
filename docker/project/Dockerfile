FROM python:3.8.15-alpine

RUN apk update && apk add python3-dev gcc libc-dev pkgconf

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./ /app
# ADD ./docker /app/docker

RUN chmod +x /app/docker/project/server-entrypoint.sh
RUN chmod +x /app/docker/project/worker-entrypoint.sh