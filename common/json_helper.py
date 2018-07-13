#!/usr/bin/evn python
# coding=utf-8

import datetime
import json
import time


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        print(type(obj))
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, time.struct_time):
            return time.strftime('%Y-%m-%d %H:%M:%S', obj)
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    js = {
        'test5': datetime.datetime.now(),
        # 'test6': time.localtime(),
        'name': 'asdsdas'
    }
    # print(js)
    result = json.dumps(js, cls=CJsonEncoder)
    print(result)
