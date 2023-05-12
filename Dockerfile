FROM archlinux:latest
ENV TZ=America/Los_Angeles
ENV DEBIAN_FRONTEND=noninteractive
RUN pacman -Syu --noconfirm && pacman -S --noconfirm tzdata cronie nano python-pip

COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob

RUN pip install requests requests_oauthlib
COPY twitbot.py /twitbot/twitbot.py
COPY constants.py /twitbot/constants.py

CMD ["crond", "-f"]
