# Build the image
docker build -t flask-avahi-poc .

# Run with host networking (required for mDNS)
docker run -it --rm \
    --net=host \
    --mount type=bind,source="./",target="/ws"\
    --workdir="/ws" \
    flask-avahi-poc /bin/bash
