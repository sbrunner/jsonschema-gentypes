FROM ubuntu:20.04

RUN \
    apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install --assume-yes --no-install-recommends \
    python3-pip && \
    apt-get clean && \
    rm --recursive --force /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN python3 -m pip --no-cache-dir install --requirement=requirements.txt

COPY Pipfile* ./
RUN	pipenv sync --system

COPY setup.py .
RUN	pipenv sync --system --dev

CMD ["jsonschema-gentypes"]
COPY . ./
WORKDIR /src
