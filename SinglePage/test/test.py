# coding:utf-8
import requests
import sys
import time
import uuid
sys.path.append('..')
from serializer import serializer
reload(sys)
sys.setdefaultencoding('utf-8')


def timer(func):
    def deco(*args, **krgs):
        start = time.time()
        fun = func(*args, **krgs)
        end = time.time()
        log.nor(args[0]._output, '|----耗时：%s' % str(end - start))
        return fun
    return deco


def note(func):
    def deco(*args, **krgs):
        id_ = str(uuid.uuid1())
        fun = func(*args, **krgs)
        if fun.status_code == 200:
            log.high(args[0]._output, '|%s %s 成功' %
                     (func.__doc__, args[0].__doc__))
        else:
            log.fail(args[0]._output, '|%s %s 失败' %
                     (func.__doc__, args[0].__doc__))
            log.fail(args[0]._output, '|--------错误代码：%s' % fun.status_code)
            if len(fun.text) > 200:
                file_name = args[0]._log_dir + '/' + id_
                log.fail(args[0]._output,
                         '|--------返回信息过长已存入文件：%s' % file_name)
                log.fail(args[0]._output, '|--------错误编号：%s' % id_)
                with open(file_name, 'a+') as f:
                    f.write('错误编号：%s\r\n' % id_)
                    f.write(fun.text)
            else:
                log.fail(args[0]._output, '|--------返回信息：%s' % fun.text)
        return fun
    return deco


def self_insert(func):
    def deco(*args, **krgs):
        fun = func(*args, **krgs)
        if fun.status_code == 200:
            data = fun.json().get('data', None)
            if data is None:
                log.nor(args[0]._output, 'data is None')
            attrs = serializer.attr_dict_from_basic(args[0])
            for attr in attrs:
                try:
                    setattr(args[0], attr, data[attr])
                except Exception as e:
                    pass
            file_name = args[0]._object_file
            with open(file_name, 'a+') as f:
                f.write(fun.text + "\r\n")
        return fun
    return deco


class log:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def nor(filename, info):
        print log.OKBLUE + info + log.ENDC
        with open(filename, 'a+') as f:
            f.write(info + '\r\n')

    @staticmethod
    def high(filename, info):
        print log.OKGREEN + info + log.ENDC
        with open(filename, 'a+') as f:
            f.write(info + '\r\n')

    @staticmethod
    def fail(filename, info):
        print log.FAIL + info + log.ENDC
        with open(filename, 'a+') as f:
            f.write(info + '\r\n')


class Test(object):
    _host = ''
    _url = ''
    _headers = ''
    _log_dir = 'err_log'
    _object_file = 'objects.log'
    _output = 'output.log'

    @self_insert
    @timer
    @note
    def _post(self, url=None, data=None, headers=None):
        '新建'
        return requests.post(url, json=data, headers=headers)

    # @self_insert
    @timer
    @note
    def _put(self, url=None, data=None, headers=None):
        '更新'
        return requests.put(url, json=data, headers=headers)

    def put(self):
        data = serializer.dump(self, 'basic')
        self._put(self._host + self._url + '%s' %
                  self.id, data=data, headers=self._headers)
        return self

    def post_get_response(self):
        '新建'
        data = serializer.dump(self, 'basic')
        return self._post(self._host + self._url, data=data, headers=self._headers)

    def post(self):
        '新建'
        data = serializer.dump(self, 'basic')
        self._post(self._host + self._url, data=data, headers=self._headers)
        return self
