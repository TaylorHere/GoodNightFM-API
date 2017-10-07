# coding:utf-8
from random_data import random_data as ran
from test import Test

host = 'http://127.0.0.1:5050'


class user(Test):
    """用户"""
    global host
    _host = host
    _url = '/users/'
    _headers = ''
    _log_dir = 'err_log'
    _object_file = 'datas/users.data'
    _output = 'outputs/output.log'

    def __init__(self):
        self.id = None
        self.telephone = ran().telephone()
        self.nickname = ran().people_name()
        self.sex = ran().sex()
        self.img_url = ran().img_url()
        self.openid = ran().id()
        self.pwd = ran().strings()
        self._save_pwd = self.pwd


class login(Test):
    """登录"""
    global host
    _host = host
    _url = '/logins/'
    _headers = ''
    _log_dir = 'err_log'
    _object_file = 'datas/logins.data'
    _output = 'outputs/output.log'

    def __init__(self, user=None):
        self.id = None
        self.user_id = None
        self.base = None
        self.login_time = None
        if user is None:
            self.pwd = ran().strings()
            self.openid = ran().id()
        else:
            self.pwd = user._save_pwd
            self.user_id = user.id
            self.openid = user.openid
            self._headers = user._headers


class address(Test):
    """地址"""
    global host
    _host = host
    _url = '/addresses/'
    _headers = ''
    _log_dir = 'err_log'
    _object_file = 'datas/address.data'
    _output = 'outputs/output.log'

    def __init__(self, user=None):
        if user is None:
            self.user_id = ran().id()
        else:
            self._headers = user._headers
            self.user_id = user.id
        self.id = None
        self.consignee = ran().people_name()
        self.phone = ran().telephone()
        self.community = ran().address()
        self.build = ran().address()
        self.detail = ran().address()
        self.describe = ran().address()
        self.is_default = ran().bool()
        self.is_authentic = ran().bool()


class escort(Test):
    """镖单"""
    global host
    _host = host
    _url = '/escorts/'
    _headers = ''
    _log_dir = 'err_log'
    _object_file = 'datas/escort.data'
    _output = 'outputs/output.log'

    def __init__(self, user=None, address=None):

        self.id = None
        self.paid = None
        self.is_transfer = None
        self.trade_number = None
        self.create_at = None
        if user is None:
            self.user_id = ran().id()
            self.name = ran().people_name()
        else:
            self.name = user.nickname
            self.user_id = user.id
            self._headers = user._headers
        self.progress = 'on'
        self.topic = '花草秀陪你过圣诞'
        self.time = ran().time()
        self.escortor_id = None
        self.phone = ran().telephone()
        self.information = ran().sentence()
        self.hide_information = ran().address() + ran().sentence()
        if address is None:
            self.address = ran().address()
        else:
            self.address = address.community + address.build + address.detail
        self.is_hide = ran().bool()
        self.fee = ran().int(0, 20)
        self.tip = ran().int(1, 10)
        self.expire_at = ran().time()
        self.pay_index = ran().int(0, 2)
        self.create_time = ''

    def put(self, progress, escortor_id=None):
        self.progress = progress
        self.escortor_id = escortor_id
        super(escort, self).put()
        # self.escortor_id = None


class escortor(Test):
    """镖师"""
    global host
    _host = host
    _url = '/escortores/'
    _headers = ''
    _log_dir = 'err_log'
    _object_file = 'datas/escortor.data'
    _output = 'outputs/output.log'

    def __init__(self, user):
        self._headers = user._headers
        self.id = None
        self.user_id = user.id
        self.passed = False
        self.name = user.nickname
        self.telephone = ran().telephone()
        self.school = ran().address()
        self.address_detail = ran().address()

if __name__ == '__main__':
    import requests
    requests.get(host + '/create_db/')
    for i in xrange(10000):
        user_1 = user()
        user_1._headers = {
            'XXX-base': 'base'
        }
        user_1.post()
        login_1 = login(user_1).post()
        user_1._headers = {
            'XXX-base': login_1.base
        }
        address_1 = address(user_1).post()
        # e = escort(user_1)
        # e.post()
        # e.put('off')
        # escort(user_1).post()
        escortor(user_1).post()
