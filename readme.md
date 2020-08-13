## 环境导出/安装

pip freeze > requestion.txt
pip install -r requestion.txt

## 项目启动

> gunicorn day01.asgi:application -b 0.0.0.0:60013 --reload -w 2 -t 1 -k uvicorn.workers.UvicornWorker

或
> uvicorn --host 0.0.0.0 --port 60013 --reload day01.asgi:application


## nginx配置
参见 `./conf/asgi.conf`

存放到自己的nginx配置中`include`指定目录下

