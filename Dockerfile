FROM python

WORKDIR /python-docker

COPY . .

CMD ["./run.sh", "prod"]
