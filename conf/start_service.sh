#!/usr/bin/env bash

cd ../

gunicorn day01.asgi:application -b 0.0.0.0:60013 --reload -w 2 -t 1 -k uvicorn.workers.UvicornWorker
# gunicorn day01.asgi:application -b unix:/tmp/gunicorn.sock --reload -w 2 -t 1 -k uvicorn.workers.UvicornWorker

# uvicorn --host 0.0.0.0 --port 60013 --reload day01.asgi:application

## TCP
# daphne -b 0.0.0.0 -p 60013 day01.asgi:application
## sock
# daphne -u /tmp/daphne.sock day01.asgi:application
