from uvicorn.workers import UvicornWorker as BaseUvicornWorker


# https://github.com/encode/uvicorn/issues/709
# 重载Uvicorn的work，解决超时问题
class UvicornWorker(BaseUvicornWorker):
    CONFIG_KWARGS = {
        "loop": "uvloop",
        "http": "httptools",
        "lifespan": "off"
    }
