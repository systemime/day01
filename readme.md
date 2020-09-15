## 更新中
django 3.1

## 环境导出/安装

pip freeze > requestion.txt
pip install -r requestion.txt

## 代码提交
exclude: |
            (?x)(
                ^settings/|
                ^node_modules/|
                ^migrations/*
            )
```shell script
npm install -g eslint
pip install pre-commit
pre-commit install
git add .
git commit -m ""

......

```

## 项目启动
### 启动web服务
> gunicorn day01.asgi:application -b 0.0.0.0:60013 --reload -w 2 -t 1 -k uvicorn.workers.UvicornWorker
> 自定义的UvicornWorker类，支持参数传递
> gunicorn -c conf/start_gunicorn.py day01.asgi:application
> 配合celery task的websocket任务300s后会触发强制超时错误，请合理解决
> 或（nginx代理时推荐, 如果存在websocket链接，则使用上方方式启动或建立wss链接并配置相应证书）
> gunicorn day01.asgi:application -b unix:/run/day01/gunicorn.socket --reload -w 1 -t 1 -k uvicorn.workers.UvicornWorker

或
> uvicorn --host 0.0.0.0 --port 60013 --reload day01.asgi:application

### 启动celery
> celery -A day01 worker -c 1  -l info
> -- worker_concurrency  cpu内核数量
> -- worker_prefetch_multiplier  并发数量

### 备注
> 缓存在redis 1库
> django channles 结果在2库
> celery 任务结果在2库

### 调试
> celery -A day01 worker -l debug

## nginx配置
参见 `./conf/asgi.conf`

存放到自己的nginx配置中`include`指定目录下

## celery使用systemctl管理
### celery配置文件
> systemd优先从系统配置文件中读取，不选择配置celery专门的环境变量的话，可以直接在系统profile文件或用户bashrc文件中配置环境变量，相应命令变化自行调整


```shell script
sudo vim /etc/default/celeryd

CELERYD_NODES=worker
# CELERYD_NODES="worker1 worker2 worker3"
# alternatively, you can specify the number of nodes to start:
# CELERYD_NODES=10

# python环境直接使用celery即可
CELERY_BIN=celery
#CELERY_BIN="/virtualenvs/def/bin/celery"

# django项目名
CELERY_APP=day01
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# How to call manage.py
CELERYD_MULTI=multi

# Extra command-line arguments to the worker
CELERYD_OPTS='--time-limit=300 --concurrency=8'
# Configure node-specific settings by appending node name to arguments:
#CELERYD_OPTS="--time-limit=300 -c 8 -c:worker2 4 -c:worker3 2 -Ofair:worker1"

# Set logging level to DEBUG
CELERYD_LOG_LEVEL=info

# pid和日志位置，也可以指定其他位置
CELERYD_LOG_FILE=/home/workon/project/ddjango/day01/logs/%n%I.log
CELERYD_PID_FILE=/home/workon/project/ddjango/day01/logs/%n.pid

# 使用的python环境，使用whereis python命令查看python所在位置
WORKON=/home/workon/env/envbuild/ddjango/bin/python

# 手动创建工作用户和组 celery/celery，也可以选择当前用户，但是不建议使用root用户
# CELERYD_USER="nobody"
# CELERYD_GROUP="nobody"

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
# CELERY_CREATE_DIRS=1
```

```shell script
sudo vim /etc/systemd/system/celery.service

[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
EnvironmentFile=/etc/default/celery
WorkingDirectory=/home/workon/project/ddjango/day01
ExecStart=/bin/sh -c '${WORKON} -m ${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${WORKON} -m ${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${WORKON} -m ${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

[Install]
WantedBy=multi-user.target
```

```shell script
# 启动celery
sudo systemctl daemon-reload
sudo systemctl start celery.service
# 查看是否启动成功
systemctl status celery
```

### django守护文件配置
```shell script
# django systemctl 配置文件

[Unit]
Description=django daemon service
After=network.target

[Service]
WorkingDirectory=/opt/Django-Project  # Django项目路径
ExecStart=/usr/local/bin/gunicorn day01.asgi:application -b unix:/run/day01/gunicorn.socket --reload -w 1 -t 1 -k uvicorn.workers.UvicornWorker

[Install]
WantedBy=multi-user.target
```

## docker-compose安装使用
> pip3 install --upgrade --force-reinstall --no-cache-dir docker-compose

```yaml
version: '3'
services:
    mysql:
        image: mysql:5.7
        container_name: mysql01
        restart: always
        ports:
            - "3306:3306"
        volumes:
            - ~/docker-com/etc/mysql/conf.d:/etc/mysql/conf.d
            - ~/docker-com/data/mysql:/var/lib/mysql
        environment:
            MYSQL_ROOT_PASSWORD: Abc123...

    redis:
        image: redis
        container_name: redis01
        command: redis-server --requirepass Abc123...
        restart: always
        ports:
            - "6379:6379"
```

```shell script
docker exec -it redis01 /bin/bash -c "redis-cli -a Abc123..."
# 或
docker exec -it redis01 /bin/bash -c "redis-cli -h xxx.xxx.xxx.xxx -p xxxx"
auth myPassword

# 重设密码
config set requirepass newPassword
config get requirepass
```

## 计划更新
- 功能框架测试
- 正文爬虫
  - 正文识别Goose3、generalnewsextractor
  - 并发模拟selenium
  - 代理池
- 集成[picgo](https://picgo.github.io/PicGo-Doc/zh/guide/advance.html#http%E8%B0%83%E7%94%A8%E4%B8%8A%E4%BC%A0%E5%85%B7%E4%BD%93%E8%B7%AF%E5%BE%84%E5%9B%BE%E7%89%87)
- markdown生成
- 异步框架探索

