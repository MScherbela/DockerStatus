docker build -t dockerstatus .
docker run --rm -it -v /home/ubuntu/data/dockerstatus:/data:ro -p 80:80 dockerstatus:latest