FROM python:3-alpine

COPY . /bing
WORKDIR /bing

RUN apk add --no-cache gcc g++ linux-headers libc-dev pcre-dev && \
    pip install -r requirements.txt && \
    apk del linux-headers && \
    adduser uwsgi

USER uwsgi

CMD uwsgi --ini uwsgi.ini
