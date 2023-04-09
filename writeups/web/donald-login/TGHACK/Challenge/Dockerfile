FROM ubuntu:focal
RUN apt-get update && apt install python3 python3-pip -y

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

RUN pip3 install flask
COPY ./src /home/ctf/
WORKDIR /home/ctf

RUN chown -R root:root /home/ctf
USER ctf
EXPOSE 5000

CMD ["python3", "main.py"]