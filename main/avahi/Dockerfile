FROM ubuntu:22.04

# Install dependencies with minimal prompts
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    avahi-daemon \
    libnss-mdns \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Flask and allow binding to port 80 without root
RUN pip3 install flask && \
    apt-get update && apt-get install -y libcap2-bin && \
    setcap 'cap_net_bind_service=+ep' /usr/bin/python3.10

# Copy application files
COPY app /app
COPY avahi/hw.local.service /etc/avahi/services/hw.local.service

# Configure Avahi
RUN sed -i 's/#host-name=foo/host-name=hw/' /etc/avahi/avahi-daemon.conf && \
    sed -i 's/#domain-name=local/domain-name=local/' /etc/avahi/avahi-daemon.conf && \
    sed -i 's/use-ipv6=yes/use-ipv6=no/' /etc/avahi/avahi-daemon.conf

# Expose ports (80 for now, 443 for future HTTPS)
EXPOSE 80

ENV PATH /app:$PATH
