FROM python:3.6-alpine

COPY . /root
WORKDIR /root

RUN apk add --no-cache bash git && pip3 install asyncio discord blessings pyyaml 

ENTRYPOINT ["/root/setup.sh"]
