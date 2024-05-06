#!/bin/bash

docker build . -t seq-align
docker run -it -v .:/app seq-align
