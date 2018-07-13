#!/usr/bin/evn python
# coding=utf-8

import datetime
import decimal


def to_int(s):
    try:
        return int(s)
    except:
        return 0


def to_int_default(s, default=0):
    '''转换为int 如果小于0，返回default'''
    result = to_int(s)

    if not result or result < 0:
        result = default
    return result


def to_float(s):
    '''转换为float'''
    try:
        return float(s)
    except:
        return 0.0


def to_decimal(s):
    try:
        return decimal.Decimal(s)
    except:
        return 0


def to_datetime(s):
    if not s:
        return None
    # 定义字典根据时间字符串匹配不同的格式
    time_dict = {
        1: "%Y-%m-%d %H:%M:%S.%f",
        2: "%Y-%m-%d %H:%M",
        3: "%Y-%m-%d %H:%M:%S",
    }
    try:
        # 如果中间含有时间部分就用：判断
        if str(s).find('.') > -1:
            return datetime.datetime.strptime(s, time_dict[0])
        elif ':' in s:
            return datetime.datetime.strptime(s, time_dict[len(str(s).split(':'))])
        else:
            return datetime.datetime.strptime(s, '%Y-%m-%d')
    except Exception as e:
        return None


def to_data(s):
    '''转日期'''
    date = to_datetime(s)
    if date:
        return date.date()
    else:
        return None


def to_timestamp10(text):
    """将时间格式的字符串转化为长度为10位长度的时间戳"""
    d = to_datetime(text)
    if d:
        return int(d.timestamp())
    else:
        return 0


def to_timestamp13(text):
    """将时间格式的字符串转化为长度为10位长度的时间戳"""
    d = to_datetime(text)
    if d:
        return int(d.timestamp() * 1000)
    else:
        return 0

