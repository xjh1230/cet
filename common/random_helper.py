#!/usr/bin/evn python
# coding=utf-8

import random
import uuid

### 定义常量 ###
# 小写字母
lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
# 大写字母
majuscule = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# 数字
numbers = "0123456789"


################


def ___get_randoms(length, text, isRepeat=False):
    """
    内部函数，获取指定长度的随机字符
    :param length: 将要生成的字符长度
    :param text: 生成随机字符的字符池
    :return: 生成好的随机字符串
    """
    if not isRepeat:
        return random.sample(text, length)
    else:
        return ((random.choice(list(text))) for i in range(0, length))


def get_number(length, isRepeat=False):
    """
    获取指定长度的数字，类型是字符串
    :param length: 将要生成的字符长度
    :return: 生成好的随机字符串
    """
    return ''.join(___get_randoms(length, numbers, isRepeat))


def get_number_for_range(small, max):
    """
    获取指定大小的整形数值
    :param small: 最小数值
    :param max: 最大数值
    :return: 生成好的随机数值
    """
    return random.randint(small, max)


def get_string(length, isRepeat=False):
    """
    获取指定长度的字符串（大小写英文字母+数字）
    :param length: 将要生成的字符长度
    :return: 生成好的随机字符串
    """
    return ''.join(___get_randoms(length, lowercase_letters + majuscule + numbers, isRepeat))


def get_letters(length, isRepeat=False):
    """
    生成随机英文字母字符串（大小写英文字母）
    :param length: 将要生成的字符长度
    :return: 生成好的随机字符串
    """
    return ''.join(___get_randoms(length, lowercase_letters + majuscule, isRepeat))


def get_uuid():
    """
    随机生成uuid
    :return: 生成好的uuid

    1、uuid1()——基于时间戳

               由MAC地址、当前时间戳、随机数生成。可以保证全球范围内的唯一性，
               但MAC的使用同时带来安全性问题，局域网中可以使用IP来代替MAC。

       2、uuid2()——基于分布式计算环境DCE（Python中没有这个函数）

                算法与uuid1相同，不同的是把时间戳的前4位置换为POSIX的UID。
                实际中很少用到该方法。

      3、uuid3()——基于名字的MD5散列值

                通过计算名字和命名空间的MD5散列值得到，保证了同一命名空间中不同名字的唯一性，
                和不同命名空间的唯一性，但同一命名空间的同一名字生成相同的uuid。

       4、uuid4()——基于随机数

                由伪随机数得到，有一定的重复概率，该概率可以计算出来。

       5、uuid5()——基于名字的SHA-1散列值

                算法与uuid3相同，不同的是使用 Secure Hash Algorithm 1 算法
    """
    return str(uuid.uuid4()).replace('-', '')
