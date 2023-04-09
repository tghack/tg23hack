# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt


# switch working directory
WORKDIR /app

# install gcc (required for compiling some of the python dependencies)
RUN apk add gcc libffi-dev libc-dev
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy all content from the local file to the image
COPY . /app


# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

USER root
EXPOSE 3301
CMD ["server.py" ]