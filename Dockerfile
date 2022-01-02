# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# When you need zero interaction while installing the system via apt. It accepts the default answer for all questions.
ARG DEBIAN_FRONTEND=noninteractive

# update
RUN apt update -y

# common
RUN apt install git -y
RUN apt install wget -y
RUN apt install vim -y
RUN apt install curl -y

# aws
RUN apt install awscli -y

# pip
RUN apt-get update -y
RUN apt install python3-pip -y

# copy files
ADD app .

CMD [ "python3", "app/main.py" ]



#COPY scripts/artifact.py /usr/local/bin/artifact

#RUN chmod +x /usr/local/bin/artifact



#ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'b2ba78627a9c40d53c41c5b7a0387ba2';
#docker run -d -p 3306:3306 --name mysql-db  -e MYSQL_ROOT_PASSWORD=b2ba78627a9c40d53c41c5b7a0387ba2 --mount src=mysql-db-data,dst=/var/lib/mysql mysql



docker run -d --name price-history-scraper price-history-scraper