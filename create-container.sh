#!/bin/bash

set -o xtrace

# Cleanup container and image
docker container stop memex-redux
docker container rm memex-redux
docker image rm memex-redux

# Build and tag image
docker build -t memex-redux .

# Create and run container
docker run -d \
  --name=memex-redux \
  -e TZ=Your/Timezone \
  --restart unless-stopped \
  -p 8002:8002 \
  memex-redux
