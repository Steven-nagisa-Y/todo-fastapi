# coding=utf-8
import re
import time


def check_name(name: str):
    """
    正则检查用户名
    :param name: str
    :return: boolean
    """
    return re.search(r'\w+', name)


def get_time(length=10):
    """

    :param length: 生成时间长度：10 -> 秒级 13 -> 毫秒级
    :return:
    """
    t = time.time()
    if length == 10:
        return int(t)
    if length == 13:
        return int(round(t * 1000))


def gen_uuid():
    """
    生成UUID
    :return: str
    """
    import uuid
    return ''.join(str(uuid.uuid4()).upper().split('-'))
