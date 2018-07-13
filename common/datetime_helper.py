#!/usr/bin/evn python
# coding=utf-8

import datetime
import time


def to_date(dt):
    if isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%d')
    elif isinstance(dt, datetime.date):
        return dt.strftime('%Y-%m-%d')
    else:
        raise Exception("日期类型错误")


def to_datetime(dt):
    if isinstance(dt, datetime.datetime):
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(dt, datetime.date):
        return dt.strftime('%Y-%m-%d')
    else:
        raise Exception("日期类型错误")


def get_week(date):
    '''
    获取当前日期为周几
    :param date:
    :return:
    '''
    if isinstance(date, datetime):
        return date.isoweekday()
    else:
        return 0


def get_year_week(date):
    '''
    获取日期为当前年第几周
    :param date:日期
    :return:第几周
    '''
    if isinstance(date, date):
        return date.isocalender()[1]
    else:
        return 0


def to_number(format=''):
    '''将当前时间转换成年月日时分秒共10位字符串'''
    if format:
        return datetime.datetime.now().strftime(format)
    else:
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def to_timestamp10():
    '''获取当前时间长度为10位长度的时间戳'''
    return int(time.time())


def to_timestamp13():
    '''获取当前时间长度为13位长度的时间戳'''
    return int(time.time() * 1000)


def timedetla(sign, dt, value):
    '''
    对指定时间进行加减运算，几秒、几分、几小时、几日、几周、几月、几年
    :param sign:y = 年, m = 月, w = 周, d = 日, h = 时, n = 分钟, s = 秒
    :param dt:日期，只能是datetime或datetime.date类型
    :param value:加减的数值
    :return:返回运算后的datetime类型值
    '''
    if not isinstance(dt, datetime.datetime) and not isinstance(dt, datetime.date):
        print(str(dt))
        print(isinstance(dt, datetime.datetime))
        print(isinstance(dt, datetime.date))
        raise Exception('不是有效的时间格式')
    if sign == 'y':
        year = dt.year + value
        if isinstance(dt, datetime.datetime):
            return datetime.datetime(year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        elif isinstance(dt, datetime.date):
            return datetime.date(year, dt.month, dt.day)
        else:
            return None
    elif sign == 'm':
        year = dt.year
        month = dt.month + value
        if month == 0:
            month = 12
            year = year - 1
        else:
            year = year + month // 12
            month = month % 12
        if isinstance(dt, datetime.datetime):
            return datetime.datetime(year, month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        elif isinstance(dt, datetime.date):
            return datetime.date(year, month, dt.day)
        else:
            return None

    elif sign == 'w':
        return dt + datetime.timedelta(weeks=value)
    elif sign == 'd':
        return dt + datetime.timedelta(days=value)
    elif sign == 'h':
        return dt + datetime.timedelta(hours=value)
    elif sign == 'n':
        return dt + datetime.timedelta(minutes=value)
    elif sign == 's':
        return dt + datetime.timedelta(milliseconds=value)
    else:
        return dt
