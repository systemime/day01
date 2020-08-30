from django.test import TestCase

# Create your tests here.

# from functools import wraps
#
#
# class logger(object):
#     def __init__(self, level='INFO'):
#         self.level = level
#
#     def __call__(self, func):  # 接受函数
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             print("[{level}]: the function {func}() is running...".
#                   format(level=self.level, func=func.__name__))
#             func(*args, **kwargs)
#             print("执行结束")
#         return wrapper  # 返回函数
#
#
# @logger(level='WARNING')
# def say(something):
#     print("say {}!".format(something))
#
#
# say("hello")
# print(say.__name__)


a = ['s1', 's3', 's9', 's4', 'h1', 'p3', 'p2', 'q5', 'q4', 'q9', 'k1', 'k2']

def fun(cards):
    if not cards:
        return
    # 先按照字母顺序排序123456
    b= sorted(cards)
    # 获取花色列表（保留花色大小顺序）
    s = ['k', 's', 'h', 'p', 'q']
    ss = {i[:1] for i in cards}
    for i in s:
        if i not in ss:
            s.pop(s.index(i))
    # 按照花色大小顺序，顺序从cards中取卡牌放到新数组中
    arr = []
    for k in s:
        for i in b:
            if k in i:
                arr.append(cards.pop(cards.index(i)))
        if not a:
            break
    return arr

print(fun(a))

"""

"""