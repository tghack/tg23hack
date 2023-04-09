FROM archlinux:latest

# https://github.com/GoogleContainerTools/kaniko/issues/2214
RUN rm -rf /var/mail /var/spool/mail

RUN pacman -Sy && pacman -S --noconfirm openssl base-devel

COPY src/ .

RUN make binexp

FROM archlinux:latest

COPY --from=0 binexp /srv/binexp

RUN chmod +x /srv/binexp && useradd binexp && chown binexp:binexp /srv/binexp

WORKDIR /srv

EXPOSE 1337

CMD ["./binexp", "TG23{345Y_8U7_w17h_4_7w157}", "1337"]
