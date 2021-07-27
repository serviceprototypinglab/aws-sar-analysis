FROM python:3.9.6-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN mkdir data

COPY ./ ./

RUN pip install --no-cache-dir -r requirements_container.txt

CMD ["python", "cli.py", "all", "--timestamp", "--light"]