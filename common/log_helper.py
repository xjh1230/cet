#!/usr/bin/evn python
# coding=utf-8

import logging
import logging.handlers
import traceback

from common import mail_helper, except_helper


def info(content):
    '''记录日志信息'''

    if content:
        logging.info(content)


def error(content='', is_send_mail=True):
    '''记录错误日志信息'''

    if traceback:
        content = content + '\n' + traceback.format_exc() + '\n'
        # 获取程序当前运行的堆栈信息
        detailtrace = except_helper.datailtrace()
        content = content + '程序调用的堆栈信息:' + detailtrace + '\n'

        logging.info(content)
    if is_send_mail:
        info = mail_helper.send_error_mail(content)
        if info: logging.info(info)
