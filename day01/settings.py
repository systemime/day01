"""
Django settings for day01 project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.conf import settings
from kombu import Exchange, Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+ar605wz%(^y7r1n(f+_=w2z_c0bj1#w0@8rl3#*x3c@d626cv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'celery',
    'app01.apps.App01Config',
    'app02.apps.App02Config',
    'app03.apps.App03Config',
    'chat'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 压缩 https://docs.djangoproject.com/en/3.1/ref/middleware/#module-django.middleware.gzip
    'django.middleware.gzip.GZipMiddleware',
    # 添加浏览器支持 https://docs.djangoproject.com/en/3.1/topics/performance/#conditionalgetmiddleware
    'django.middleware.http.ConditionalGetMiddleware'
]

ROOT_URLCONF = 'day01.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }, {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'day01.base_jinja.environment',
            'context_processors': [],
        },
    },
]

WSGI_APPLICATION = 'day01.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "HOST": "127.0.0.1",
        'NAME': 'day01',
        'USER': "root",
        "PASSWORD": "123456",
        "PORT": 3306
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

# If you set this to True, Django will format dates, numbers and calendars
# according to user current locale.
USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# -- 其他文件路径
MEDIA_URL = "/media/"      # 跟STATIC_URL类似，指定用户可以通过这个路径找到文件
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # media是约定成俗的文件夹名,头像存放

# Maximum number of GET/POST parameters that will be read before a
# SuspiciousOperation (TooManyFieldsSent) is raised.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000

# -- 用户继承模型
AUTH_USER_MODEL = 'app01.UserProfile'

# -- 异步安全选项
# Django的某些关键部分在异步环境中无法安全运行，因为它们的全局状态不支持协同程序。
# Django的这些部分被分类为“异步不安全”，并且受到保护，无法在异步环境中执行。ORM是主要示例，但是其他部分也以这种方式受到保护。
# ---
# 如果您尝试从存在运行中事件循环的线程中运行这些部件中的任何一个，则会收到 SynchronousOnlyOperation错误消息。
# 请注意，您不必直接在异步函数内部即可发生此错误。
# 如果您直接从异步函数中调用了同步函数，而没有使用sync_to_async()或类似方法，则它也可能发生。
# 这是因为您的代码即使未声明为异步代码，也仍在具有活动事件循环的线程中运行。
# ---
# 如果遇到此错误，则应修复代码以免从异步上下文中调用有问题的代码。
# 而是编写自己的与异步不安全函数对话的代码，同步函数，然后使用asgiref.sync.sync_to_async()（或在其自己的线程中运行同步代码的任何其他方式）进行调用 。
# ---
# 您可能仍然被迫从异步上下文中运行同步代码。
# 例如，如果外部环境（例如Jupyter笔记本电脑）强加了您的要求 。
# 如果您确定不可能同时运行代码，并且绝对需要从异步上下文中运行此同步代码，则可以通过设置警告来禁用警告 DJANGO_ALLOW_ASYNC_UNSAFE 环境变量为任何值。
# ---
# https://docs.djangoproject.com/en/3.1/topics/async/#async-safety
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# -- Channels
ASGI_APPLICATION = 'day01.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# -- 缓存配置
# MemcachedCache 缓存替换原则是LRU算法（速度快，安全性低，数据格式必须简单，弃用换redis）
CACHES = {
    'default': {
        # 指定缓存使用的引擎
        'BACKEND': 'django_redis.cache.RedisCache',
        # 与celery结果存放于同一数据库，尝试获取执行结果
        'LOCATION': 'redis://127.0.0.1:6379/1',  # 分片行为，可以直接使用默认的0库
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",  # 激活数据压缩
            "IGNORE_EXCEPTIONS": True,  # 防止redis意外关闭造成异常，memcached backend 的默认行为
            # "PASSWORD": "密码",
        }
    }
}


# -- celery配置
# Celery application definition 异步任务设置
BROKER_URL = 'amqp://guest:guest@localhost:5672//'  # RabbitMQ 默认连接
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'  # 结果存放，可用于跟踪结果
# 存放在django-orm 数据表中
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
# CELERY_RESULT_SERIALIZER = 'json'  # 结果的序列化方式
# CELERY_TASK_SERIALIZER = 'json'  # 消息任务的序列化方式
# 时区
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = TIME_ZONE

# 性能配置
CELERYD_CONCURRENCY = 2  # celery worker的并发数 命令行 -c 指定的数目,worker不是越多越好,保证任务不堆积,加上一定新增任务的预留就可以
CELERYD_PREFETCH_MULTIPLIER = 4  # celery worker 每次去 rabbitMQ 取任务的数量, 日后需要区分低频与高频任务分开设置
CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker执行了多少任务就会死掉（重制），默认无限, 业务增长容易爆内存
# CELERY_DEFAULT_QUEUE = "message_queue"  # 默认的队列，如果一个消息不符合其他的队列就会放在默认队列里面,发现如果设置无法选择其他路由
CELERY_RESULT_EXPIRES = 60 * 3  # celery worker 超时 180s

# 详细队列设置 RabbitMQ 队列设置
CELERY_QUEUES = (
    # "default_qf": {  # 这是上面指定的默认队列, 另一种写法
    #     "exchange": "default",  # 消息交换机，按路由规则指定到哪个队列
    #     "exchange_type": "direct",  # 交换机类型
    #     "routing_key": "default"  # 路由关键字，交换机按key进行消息投递
    # },
    Queue(name='select_queue', exchange='select_queue', routing_key='select_router'),  # 队列 - 查询服务
    # Queue(name='cud_queue', exchange='cud_queue', routing_key='cud_router'),  # 队列 - 增删改
)
# Queue的路由
CELERY_ROUTES = {
    'app01.tasks.select': {
            'queue': 'select_queue',
            'routing_key': 'select_router',
            # 'priority': 10  # 优先级指定 仅在redis或rabbitmq时
    },
}

# 日志配置
# CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "%n%I.log")
# CELERYD_PID_FILE = os.path.join(BASE_DIR, "logs", "%n.pid")
# CELERYDBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "%n_beat.log")
# CELERYBEAT_PID_FILE = os.path.join(BASE_DIR, "logs", "celeryd.pid")

# # 动态定时任务
# DJANGO_CELERY_BEAT_TZ_AWARE = False
# # 可以使用redisbeat包存入redis中，安全性考虑不适用这个包
# # 此处配置后, 默认的定时任务也会出现在表django_celery_beat_periodictask中
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# # django_celery_beat.models.PeriodicTask 定义要运行的单个周期性任务。
# # django_celery_beat.models.IntervalSchedule 以特定间隔（例如，每5秒）运行的计划。
# # django_celery_beat.models.CrontabSchedule 与像在cron项领域的时间表 分钟小时日的一周 DAY_OF_MONTH month_of_year
# # django_celery_beat.models.PeriodicTasks 仅用作索引以跟踪计划何时更改

# -- session缓存配置
# 重建数据库后一定要运行cache.clear()清除缓存中残留的session，否则无法登录
# cached_db缓存模式，session先存储到缓存中，再存储到数据库（同读取顺序）
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"  # 官方
SESSION_CACHE_ALIAS = "default"
# session 过期时间， django 本身要么设置固定时间，要么关闭浏览器失效
SESSION_COOKIE_AGE = 60 * 240  # 4小时
SESSION_SAVE_EVERY_REQUEST = True  # 是否每次请求都保存session，默认修改后才保存 即，false到期实际马上失效，true每次请求重新计时
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效
SESSION_COOKIE_NAME = "vboxsuper"  # 浏览器中session字符串key标识
SESSION_COOKIE_SECURE = True  # 进行设置True以避免在HTTP上意外传输会话cookie
# SESSION_COOKIE_DOMAIN = None  # session的cookie保存的域名(在哪个域名下可用,None 子域名)
# SESSION_COOKIE_PATH = "/"  # 默认所有页面都能使用session
# SESSION_COOKIE_SECURE = False  # 是否https传输cookie
# SESSION_COOKIE_HTTPONLY = True  # 是否session的cookie只支持http传输

# -- 邮件配置
# smtp 服务器地址
EMAIL_HOST = "smtp.qq.com"
# 默认端口25，若请求超时可尝试465
EMAIL_PORT = 465
# 用户名
EMAIL_HOST_USER = "cchandler@qq.com"
# 邮箱代理授权码（不是邮箱密码）
EMAIL_HOST_PASSWORD = "erqlgnfdeuefbcad"
# 是否使用了SSL 或者TLS（两者选其一）
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
# 发送人
EMAIL_FROM = "cchandler@qq.com"
# 默认显示的发送人，（邮箱地址必须与发送人一致），不设置的话django默认使用的webmaster@localhost
DEFAULT_FROM_EMAIL = "Vbox 注册 <cchandler@qq.com>"

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': './debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }
#
# SERVER_EMAIL = 'cchandler@qq.com'
# DEFAULT_FROM_EMAIL = 'cchandler@qq.com'
# ADMINS = [('qifeng', 'q547feng@163.com')]
# EMAIL_HOST = 'smtp.qq.com'
# EMAIL_PORT = 465
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'cchandler@qq.com'
# EMAIL_HOST_PASSWORD = 'erqlgnfdeuefbcad'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
