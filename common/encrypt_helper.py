#!/usr/bin/evn python
# coding=utf-8

import hashlib


def md5(text):
    m = hashlib.md5()
    if not isinstance(text, bytes):
        text = str(text).encode('utf-8')
    m.update(text)
    return m.hexdigest()
