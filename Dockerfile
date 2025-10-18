FROM python:3.13.9-slim
LABEL maintainer="luisgsilva26@gmail.com"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./src /src
WORKDIR /src
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && apt-get install -y \
    postgresql-client \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev && \
    /py/bin/pip install -r /tmp/requirements.txt

ENV PATH="/py/bin:$PATH"

CMD ["python", "app.py"]