# Build the image
docker build -t minimal-avahi .

# Run the container
docker run --rm --net=host minimal-avahi