#!/usr/bin/evn python
# coding=utf-8

import psycopg2
import psycopg2.extras

from  common import log_helper
from config import const

# 初始化数据参数
db_name = const.DB_NAME
db_host = const.DB_HOST
db_port = const.DB_PORT
db_user = const.DB_USER
db_pass = const.DB_PASS


def read(sql):
    '''
    连接pg数据库进行查询
    如果连接失败，会把错误写入日志，并返回false.如果成功，返回查询到的数据，这个数据是结果转换的，字典格式，其中key是数据表里的字段
    :param sql:
    :return:
    '''

    try:
        # 连接数据库
        conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
        # 获取游标
        cours = conn.cursor()
        # cours=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except Exception as e:
        print(e.args)
        log_helper.error(e.args, False)
        return False
    try:
        cours.execute(sql)
        data = [dict((cours.description[i][0], value) for i, value in enumerate(row)) for row in cours.fetchall()]
        # data=cours.fetchall()
    except Exception as e:
        log_helper.error('sql执行失败:' + str(e.args) + '执行sql:' + str(sql))
    finally:
        cours.close()
        conn.close()
    if data:
        return data
    else:
        return None


def write(sql, vars):
    '''
    链接数据库 进行写操作
    :param sql: sql语句
    :param vars: 参数
    :return:
    '''

    try:
        conn = psycopg2.connect(database=db_name, user=db_user, password=db_pass, port=db_port, host=db_host)
        cours = conn.cursor()
    except Exception as e:
        print(e.args)
        log_helper.error(e.args, False)
        return False
    try:
        cours.execute(sql, vars)
        conn.commit()
    except Exception as e:
        print(e.args)
        # 如果出错，则事务回滚
        conn.rollback()
        log_helper.error('sql执行失败:' + str(e.args) + ' sql:' + str(sql))
        return False
    else:
        # 获取数据
        try:
            # data = [dict((cours.description[i][0], value) for i, value in enumerate(row))
            #         for row in cours.fetchall()]
            data=cours.fetchone()
        except Exception as e:
            # 没有设置returning或执行修改或删除语句时，记录不存在
            data = None
    finally:
        cours.close()
        conn.close()
    return data
