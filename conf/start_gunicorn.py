import os
import multiprocessing
# import gevent.monkey
# gevent.monkey.patch_all()


debug = True
loglevel = 'debug'
bind = '0.0.0.0:8800'  # 监听
timeout = 30  # 超时
pidfile = 'log/gunicorn.pid'
logfile = 'log/debug.log'
chdir = "/home/workon/project/ddjango/day01"

daemon = False  # 是否是守护进程（后台运行）

# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
threads = 1  # 指定每个进程开启的线程数
# worker_class = 'gunicorn.workers.ggevent.GeventWorker'
worker_class = 'uvicorn.workers.UvicornWorker'

worker_connections = 2000  # 最大并发

reload = True

x_forwarded_for_header = 'X-FORWARDED-FOR'

accesslog = "/home/test/server/log/gunicorn_access.log"      # 访问日志文件
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    # 设置gunicorn访问日志格式，错误日志无法设置

"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
errorlog = "/home/test/server/log/gunicorn_error.log"        # 错误日志文件
