FROM ubuntu:22.04 as base-all
LABEL maintainer Camptocamp "info@camptocamp.com"
SHELL ["/bin/bash", "-o", "pipefail", "-cux"]

RUN --mount=type=cache,target=/var/lib/apt/lists \
    --mount=type=cache,target=/var/cache,sharing=locked \
    apt-get update \
    && apt-get upgrade --assume-yes \
    && apt-get install --assume-yes --no-install-recommends python3-pip

# Used to convert the locked packages by poetry to pip requirements format
# We don't directly use `poetry install` because it force to use a virtual environment.
FROM base-all as poetry

# Install Poetry
WORKDIR /tmp
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache \
    python3 -m pip install --disable-pip-version-check --requirement=requirements.txt

# Do the conversion
COPY poetry.lock pyproject.toml ./
RUN poetry export --extras=tools --output=requirements.txt

# Base, the biggest thing is to install the Python packages
FROM base-all as base

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,from=poetry,source=/tmp,target=/poetry \
    python3 -m pip install --disable-pip-version-check --no-deps --requirement=/poetry/requirements.txt

CMD ["jsonschema-gentypes"]
COPY . ./
RUN --mount=type=cache,target=/root/.cache \
    sed --in-place 's/enable = true # disable on Docker/enable = false/g' pyproject.toml \
    && python3 -m pip install --disable-pip-version-check --no-deps --editable=. \
    && python3 -m pip freeze > /requirements.txt
WORKDIR /src
