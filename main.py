#!/usr/bin/evn python
# coding=utf-8

import logging
import os
import sys
import urllib.parse

import bottle
from beaker.middleware import SessionMiddleware
from bottle import hook, default_app, get, run, response, request, static_file

import api
from common import web_helper, log_helper

#############################################
# 初始化bottle框架相关参数
#############################################
# 获取当前main.py文件所在服务器的绝对路径
program_path = os.path.split(os.path.realpath(__file__))[0]
# 将路径添加到python环境变量中
sys.path.append(program_path)
# 让提交数据最大改为2M（如果想上传更多的文件，可以在这里进行修改）
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 2
# 定义upload为上传文件存储路径
# upload_path = os.path.join(program_path, 'upload')
upload_path = os.path.join(program_path, 'upload')

#############################################
# 初始化日志相关参数
#############################################
# 如果日志目录log文件夹不存在，则创建日志目录
if not os.path.exists('log'):
    os.mkdir('log')
# 初始化日志目录路径
log_path = os.path.join(program_path, 'log')
# 定义日志输出格式与路径
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    filename="%s/info.log" % log_path,
                    filemode='a')

# 设置session参数
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 3600,
    'session.data_dir': '/tmp/sessions/simple',
    'session.auto': True
}


@hook('before_request')
def validate():
    """使用勾子处理接口访问事件"""
    r = request

    # 获取路径
    path_info = request.environ.get('PATH_INFO')
    # 记录参数
    # 图标等不用处理 直接返回
    if path_info in ['/favicon.ico', '/', '/api/verify/']:
        return
    request_log = 'url:' + path_info + ';ip:' + web_helper.get_ip()
    try:
        if request.json:
            request_log = request_log + ';params(json):' + urllib.parse.unquote(str(request.json))
    except:
        pass
    try:
        if request.query_string:
            request_log = request_log + ';params(get):' + request.query_string
        if request.method == 'POST':
            request_log = request_log + ';params(post):' + urllib.parse.unquote(str(request.params.__dict__))
        log_helper.info(request_log)
        print(request_log)
    except:
        pass

    # put等方法特殊处理
    if request.method == 'POST':
        _method=web_helper.get_form('_method',False)
        if _method:
        # if request.POST.get('_method'):
            request.environ['REQUEST_METHOD'] = _method #request.POST.get('_method', '')
            print('_method:' + _method + '|')
        # elif request.json.get()
    # 登录验证
    url_list = ["/api/login/", "/api/logout/"]
    if path_info in url_list:
        return
    else:
        s = str(api.__dict__)
        session = web_helper.get_session()
        # 获取用户id
        manager_id = session.get('id', 0)
        login_name = session.get('login_name', 0)
        print('manager_id:' + str(manager_id) + 'login_name:' + str(login_name))
        # 判断用户是否登录
        # if not manager_id or not login_name:
        #     web_helper.return_raise(web_helper.return_msg(-404, "您的登录已失效，请重新登录"))
        print(4)




@get('/upload/<filepath:path>')
def upload_static(filepath):
    """设置静态内容路由"""
    response.add_header('Content-Type', 'application/octet-stream')
    return static_file(filepath, root=upload_path)

class EnableCors(object):
    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)
        return _enable_cors

app = bottle.app()
app.install(EnableCors())
# 函数主入口
if __name__ == '__main__':
    app_argv = SessionMiddleware(default_app(), session_opts)
    # app_argv.install(EnableCors())
    run(app=app_argv, host='0.0.0.0', port=8088, debug=True, reloader=True)
else:
    # 使用uwsgi方式处理python访问时，必须要添加这一句代码，不然无法访问
    application = SessionMiddleware(default_app(), session_opts)
