FROM alpine:latest
RUN apk add --no-cache bind openrc
RUN mkdir -p /etc/bind/zone
COPY named.conf /etc/bind/named.conf
COPY zone /etc/bind/zone
CMD ["named", "-g"]