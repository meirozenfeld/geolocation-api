FROM python:3.6.8-alpine3.9

RUN apk add --no-cache mongodb

VOLUME /data/db
EXPOSE 27017

COPY run.sh /root
ENTRYPOINT [ "/root/run.sh" ]

WORKDIR /var/www

ADD . /var/www/
RUN pip install -r /var/www/requirements.txt

EXPOSE 8080
