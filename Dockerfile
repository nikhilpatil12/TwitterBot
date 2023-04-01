FROM ubuntu:latest
ENV TZ=America/Los_Angeles
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y tzdata
RUN apt install -y pip cron nano systemd
COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob

RUN pip install requests requests_oauthlib
COPY twitbot.py /twitbot/twitbot.py
COPY constants.py /twitbot/constants.py

# Enable and start the cron service using systemd
RUN systemctl enable cron.service

# Set the default command for the container
CMD ["/lib/systemd/systemd"]