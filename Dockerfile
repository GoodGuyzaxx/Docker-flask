FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y \
    python3\
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /zax
COPY ./app .


RUN python3 -m venv /zax/venv
RUN /zax/venv/bin/pip install --upgrade pip
RUN /zax/venv/bin/pip install --ignore-installed -r requirements.txt


CMD ["/zax/venv/bin/gunicorn", "--bind", "0.0.0.0:8888", "app:app"]