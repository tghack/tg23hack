FROM python:3.10-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./src/ /app/webapp/
COPY run.py /app/run.py
COPY flag.txt /flag.txt

RUN adduser -D ctf
USER ctf

ENTRYPOINT ["python"]
CMD ["run.py"]