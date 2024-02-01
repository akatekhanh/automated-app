# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install negmas --no-deps
RUN apt-get update -y && apt-get install procps -y && apt-get install -y supervisor
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD [ "python", "worker.py", "&"]]
# CMD ["/usr/bin/supervisord", "-n"]