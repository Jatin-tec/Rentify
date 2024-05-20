# pull official base image
FROM python:3.11.4-slim-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Kolkata

# Update the System & install dependencies
RUN apt-get update && \
    apt-get install -y  \
        cron \
        libpq-dev \
        libpython3-dev:amd64 \
        postgresql-contrib \
        python3-dev \
        python3-pip \
        python3-cffi \
        python3-brotli \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        libcairo2 \
        libpangocairo-1.0-0 -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache

RUN apt update
# Starting cron daemon service and setting up cron settings
# RUN service cron start
RUN touch /var/log/cron.log
RUN chmod 600 /etc/crontab

# Install app dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . /app

# set work directory
WORKDIR /app

# run entrypoint.sh
COPY ./entrypoint.sh /

# grant permission to execute entrypoint.sh
RUN chmod +x /entrypoint.sh

# run entrypoint.sh
CMD ["/entrypoint.sh"]
