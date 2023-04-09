FROM python:3.10-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./src/main.py main.py

RUN adduser -D ctf
USER ctf

ENTRYPOINT ["python"]
CMD ["main.py"]