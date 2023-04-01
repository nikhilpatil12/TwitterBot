FROM ubuntu:latest
ENV TZ=America/Los_Angeles
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y tzdata
RUN apt install -y pip
RUN pip install requests requests_oauthlib
COPY twitbot.py /twitbot/twitbot.py
COPY constants.py /twitbot/constants.py
RUN cd /twitbot/
RUN python3 twitbot.py