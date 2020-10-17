docker build -t dockerstatus .
docker run --rm -d -v /home/ubuntu/data/dockerstatus:/data:ro