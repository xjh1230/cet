#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xingjh


import json
from bottle import post ,get
from common import web_helper,db_helper,json_helper


@get('/api/test/')
def test():
    name = web_helper.get_query('name')
    return name

@post('/api/record/')
def record():
    name = web_helper.get_form('name','姓名为空',False)
    cardno = web_helper.get_form('cardno','准考证号为空',False)
    ip = web_helper.get_ip()
    print(name,cardno,ip)
    sql = '''insert into searchrecord (name,cardno,ip) VALUES (%(name)s,%(cardno)s,%(ip)s) returning id'''
    par = {'name': name, 'cardno': cardno,'ip':ip}
    result = db_helper.write(sql, par)
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, '失败')

@get('/api/getrecord/')
def get_record():
    # 初始化输出格式
    data = {
        'records': 0,  # 总记录数
        'total': 0,  # 总页数
        'page': 1,  # 页数
        'rows': []
    }
    sql = '''select  * from searchrecord limit 500 offset 0 '''
    result = db_helper.read(sql)
    if result:
        data['rows'] = result
    if data:
        return web_helper.return_raise(json.dumps(data, cls=json_helper.CJsonEncoder))
    else:
        return web_helper.return_msg(-1, '没有数据', '')


