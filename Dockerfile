# To build the container, cd into the root directory of the repository (where this Dockerfile is) and type:
# sudo docker build -t dockermonitor .
# To run the container, use the following command:
# sudo docker run --rm -d -v /home/ubuntu/data/dockerstatus:/data dockerstatus:latest

# set base image (host OS)
FROM uv:python3.11-alpine
ADD . /app
WORKDIR /app
RUN uv sync --frozen
ENV FLASK_APP=main.py

CMD ["uv", "run", "gunicorn", "--bind", ":80", "--worker-tmp-dir", "/dev/shm", "--workers=1", "--threads=2", "main:app"]
