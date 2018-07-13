#!/usr/bin/evn python
# coding=utf-8

import json

from bottle import get, put, delete, post

from common import db_helper, convert_helper, web_helper, json_helper


@get('/api/product_class/')
def callback():
    # 页面索引
    page_number = convert_helper.to_int_default(web_helper.get_query('page', '', False), 1)
    # 页面显示记录数量
    page_size = convert_helper.to_int_default(web_helper.get_query('rows', '', False), 10)
    # page_size = 2

    # 排序字段
    sidx = web_helper.get_query('sidx', '', False)
    # 排序方式
    sord = web_helper.get_query('sord', '', False)

    # 初始化输出格式
    data = {
        'records': 0,  # 总记录数
        'total': 0,  # 总页数
        'page': 1,  # 页数
        'rows': []
    }

    # 获取记录总数
    sql_count = 'select count(1) as records from product_class'
    result = db_helper.read(sql_count)
    if not result or result[0]['records'] == 0:
        return data
    data['records'] = result[0].get('records', 0)
    # 计算总页数
    if data['records'] % page_size == 0:
        page_total = data['records'] // page_size
    else:
        page_total = data['records'] // page_size + 1
    data['total'] = page_total
    data['page'] = page_number
    # 排序sql
    order_by = 'sort asc'
    if sidx:
        order_by = sidx + ' ' + sord
    if not order_by:
        order_by = ' id desc '

    # 分页sql
    record_number = (page_number - 1) * page_size
    paging = ' limit ' + str(page_size) + ' offset ' + str(record_number)
    # 获取数据
    sql_data = 'select * from product_class  order by %(orderby)s %(paging)s' % {'orderby': order_by, 'paging': paging}
    result = db_helper.read(sql_data)

    if result:
        data['rows'] = result
    if data:
        return web_helper.return_raise(json.dumps(data, cls=json_helper.CJsonEncoder))
    else:
        return web_helper.return_msg(-1, '没有数据', '')

@get('/api/product_class1/')
def callback():
    # 排序字段
    sidx = web_helper.get_query('sidx', '', False)
    # 排序方式
    sord = web_helper.get_query('sord', '', False)
    # 初始化输出格式
    data = {
        'rows': []
    }
    # 排序sql
    order_by = 'sort asc'
    if sidx:
        order_by = sidx + ' ' + sord
    if not order_by:
        order_by = ' id desc '

    # 获取数据
    sql_data = 'select * from product_class  order by %(orderby)s ' % {'orderby': order_by}
    result = db_helper.read(sql_data)

    if result:
        data['rows'] = result
    if data:
        return web_helper.return_raise(json.dumps(data, cls=json_helper.CJsonEncoder))
    else:
        return web_helper.return_msg(-1, '没有数据', '')


@get('/api/product_class/<id:int>/')
def callback(id):
    sql = 'select * from product_class where id=%s' % str(id)
    result = db_helper.read(sql)
    if result:
        return web_helper.return_msg(0, '成功', result[0])
    else:
        return web_helper.return_msg(-1, '')


@put('/api/product_class/<id:int>/')
def callback(id):
    name = web_helper.get_form('name', '', False)
    is_enable = convert_helper.to_int_default(web_helper.get_form('is_enable', '', False), 0)
    sql = '''update product_class set name=%(name)s ,is_enable=%(is_enable)s where id=%(id)s returning id'''
    par = {'name': name, 'is_enable': is_enable, 'id': id}

    result = db_helper.write(sql, par)
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, '失败')


@post('/api/product_class/')
def callback():
    name = web_helper.get_form('name', '', False)
    is_enable = convert_helper.to_int_default(web_helper.get_form('is_enable', '', False), 0)

    sql = '''insert into product_class (name,is_enable) VALUES (%(name)s,%(is_enable)s) returning id'''
    par = {'name': name, 'is_enable': is_enable}
    result = db_helper.write(sql, par)
    if result:
        return web_helper.return_msg(0, '成功')
    else:
        return web_helper.return_msg(-1, '失败')


@delete('/api/product_class/')
def callback():
    id = web_helper.get_query('id', '', False)
    id = convert_helper.to_int_default(id, 0)
    # 判断分类有没有被引用
    sql = 'select count(1) as records from product where product_class_id=%s' % str(id)
    result = db_helper.read(sql)
    if result and result[0].get('records', -1) > 0:
        return web_helper.return_msg(-1, '该分类已被引用，请清除对该分类的绑定后再来删除')
    else:
        sql = 'delete from product_class where id=%s returning id' % (id)
        val = (id)
        result = db_helper.write(sql, val)
        if result:
            return web_helper.return_msg(0, '成功')
        else:
            return web_helper.return_msg(-1, '失败')
