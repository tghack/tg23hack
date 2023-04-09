FROM node:alpine
COPY ./src /opt/www
WORKDIR /opt/www
RUN apk add imagemagick ghostscript-fonts libqrencode && \
    npm install
CMD nodejs server.js
