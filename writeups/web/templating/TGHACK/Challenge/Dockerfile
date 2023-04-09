FROM alpine:3.7

RUN apk update && apk add python python-dev py-pip build-base
RUN mkdir /app
COPY src /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]