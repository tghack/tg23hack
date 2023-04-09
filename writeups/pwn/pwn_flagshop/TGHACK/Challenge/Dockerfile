FROM ubuntu:22.04

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf

WORKDIR /home/ctf

COPY ./src/. .

RUN chmod +x ynetd
RUN chmod +x ./butikk

USER ctf
EXPOSE 1337
CMD ./ynetd -p 1337 ./butikk
