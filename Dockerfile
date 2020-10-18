# To build the container, cd into the root directory of the repository (where this Dockerfile is) and type:
# sudo docker build -t dockermonitor .
# To run the container, use the following command:
# sudo docker run --rm -d -v /home/ubuntu/data/dockerstatus:/data dockerstatus:latest

# set base image (host OS)
FROM python:3.8
WORKDIR /home
RUN apt-get update

RUN apt-get install nano less

# set-up the working dir (incl. the code) and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
ADD templates ./templates
ADD static ./static

ENV FLASK_APP=main.py
# Run using flask webserver. To be replaced by gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
#CMD ["python", "main.py"]