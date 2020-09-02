#!/usr/bin/env bash

cd ../

# --------------------------------Gunicorn----------------------------------------
# # run gunicorn
## by socket
# gunicorn day01.asgi:application -b unix:/run/day01/gunicorn.socket --reload -w 2 -t 1 -k uvicorn.workers.UvicornWorker
gunicorn -c conf/start_gunicorn.py day01.asgi:application
# -----------------------------Other start Asgi-----------------------------------
## by TCP
# gunicorn day01.asgi:application -b 0.0.0.0:60013 --reload -w 2 -t 1 -k uvicorn.workers.UvicornWorker
## Run ASGI app from gunicorn, using asyncio and h11 (for pypy compatibility):
# gunicorn app:App -w 4 -k uvicorn.workers.UvicornH11Worker

# # by unvicorn
## TCP
# uvicorn --host 0.0.0.0 --port 60013 --reload day01.asgi:application
# # by daphne
## TCP
# daphne -b 0.0.0.0 -p 60013 day01.asgi:application
## sock
# daphne -u /tmp/daphne.sock day01.asgi:application

# -----------------------------------Nginx----------------------------------------
# reload nginx config
sudo nginx -s reload

# -----------------------------------Celery---------------------------------------
# # start celery and corntab
## 异步任务
celery -A day01 worker -l debug
## 定时任务:
nohup celery -A day01 beat -l info > logs/celery_beat.log 2>&1 &
# pip install eventlet  # 引入协程
# django3.x无法使用协程库
# nohup celery -A day01 worker -l info -P eventlet > logs/celery.log 2>&1 &
# 合并
# celery -A Vbox worker -b -l info

# sudo ln -s /usr/local/python3/bin/python3 /usr/bin/python3
# sudo ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
# sudo ln -s /usr/local/python3/bin/easy_install-3.7 /usr/bin/easy_install-3.7
# sudo ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip3.7
# sudo ln -s /usr/local/python3/bin/pydoc3 /usr/bin/pydoc3
# sudo ln -s /usr/local/python3/bin/pydoc3.7 /usr/bin/pydoc3.7
# sudo ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3.7
# sudo ln -s /usr/local/python3/bin/python3.7-config /usr/bin/python3.7-config
# sudo ln -s /usr/local/python3/bin/python3.7m /usr/bin/python3.7m
# sudo ln -s /usr/local/python3/bin/python3.7m-config /usr/bin/python3.7m-config
# sudo ln -s /usr/local/python3/bin/python3-config /usr/bin/python3-config
# sudo ln -s /usr/local/python3/bin/pyvenv /usr/bin/pyvenv
# sudo ln -s /usr/local/python3/bin/pyvenv-3.7 /usr/bin/pyvenv-3.7
