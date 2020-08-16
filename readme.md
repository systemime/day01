## 环境导出/安装

pip freeze > requestion.txt
pip install -r requestion.txt

## 项目启动
### 启动web服务
> gunicorn day01.asgi:application -b 0.0.0.0:60013 --reload -w 2 -t 1 -k uvicorn.workers.UvicornWorker
> 或（nginx代理时推荐）
> gunicorn day01.asgi:application -b unix:/run/day01/gunicorn.socket --reload -w 1 -t 1 -k uvicorn.workers.UvicornWorker

或
> uvicorn --host 0.0.0.0 --port 60013 --reload day01.asgi:application

### 启动celery
> celery -A day01 worker -l info
> ## 调试
> celery -A day01 worker -l debug

## nginx配置
参见 `./conf/asgi.conf`

存放到自己的nginx配置中`include`指定目录下

## 计划更新
- 功能框架测试
- 正文爬虫
  - 正文识别Goose3、generalnewsextractor
  - 并发模拟selenium
  - 代理池
- 集成[picgo](https://picgo.github.io/PicGo-Doc/zh/guide/advance.html#http%E8%B0%83%E7%94%A8%E4%B8%8A%E4%BC%A0%E5%85%B7%E4%BD%93%E8%B7%AF%E5%BE%84%E5%9B%BE%E7%89%87)
- markdown生成
- 异步框架探索

