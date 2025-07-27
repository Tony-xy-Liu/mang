FROM alpine:latest

RUN apk add --no-cache avahi dbus
RUN mkdir -p /var/run/dbus

COPY avahi-daemon.conf /etc/avahi/avahi-daemon.conf

EXPOSE 5353/udp

CMD dbus-daemon --system && avahi-daemon --no-drop-root --debug