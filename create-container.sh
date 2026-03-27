#!/bin/bash
docker run -d \
  --name=memex-redux \
  -e TZ=Europe/Oslo \
  -e CONFIG_FILE=config.json \
  --restart unless-stopped \
  -p 8002:8002 \
  memex-redux
