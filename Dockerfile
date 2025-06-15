FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y \
    python3\
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /hab
COPY ./app .


RUN python3 -m venv /hab/venv
RUN /hab/venv/bin/pip install --upgrade pip
RUN /hab/venv/bin/pip install --ignore-installed -r requirements.txt


CMD ["/hab/venv/bin/gunicorn", "--bind", "0.0.0.0:8888", "app:app"]