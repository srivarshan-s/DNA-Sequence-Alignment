FROM debian:10


RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 -y

RUN useradd --create-home sequser
USER sequser

WORKDIR /app

