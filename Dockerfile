FROM python:3.9.6-slim-buster

WORKDIR /usr/src/app

RUN mkdir data

COPY ./requirements_container.txt ./autocontents.py ./cli.py ./insights.py ./insights-plot.py ./githubstats ./github-contents.py ./

RUN pip install --no-cache-dir -r requirements_container.txt

CMD ["python", "cli.py"]