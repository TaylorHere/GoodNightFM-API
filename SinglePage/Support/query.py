# coding:utf-8
import json
from datetime import date, datetime

import redis

from SinglePage.singlepage import SinglePage, app, serializer

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)


class Query(SinglePage):
    """query资源将其它资源当作可query对象，query资源本身具有缓存能力，缓存服务器为redis，他可以执行其它接口的查询操作，并缓存结果"""

    def get(self, request, key):
        return ('unimplament api', 401), 'origin'

    def put(self, request, cls):
        '你可以强制更新缓存内容，它会根据你的cls和参数生成键'
        data = request.get_json()
        pk = data.get('pk', None)
        try:
            resources = app.config['resources']
            resource = resources[cls]
        except:
            return ('get resource err,need cls in url', 401),'origin'
        passed, permission = resource().get_permission_passed(pk)
        if not passed:
            return ("permission hint: " + permission().get.__doc__,401), 'origin'
        key = cls + str(data)
        request.args = data
        value, type = resource().get(pk)
        to_chache = {'data': serializer.dump(value, type)}
        r.set(key, json.dumps(to_chache))
        return value, type

    def post(self, request, cls):
        '你可以在json中放置过滤参数，他会根据cls和参数生成缓存键，如果键存在，则会使用redis服务器中的内容，否则进入数据库然后缓存到redis'
        data = request.get_json()
        pk = data.get('pk', None)
        try:
            resources = app.config['resources']
            resource = resources[cls]
        except:
            return ('get resource err,need cls in url', 401),'origin'
        passed, permission = resource().get_permission_passed(pk)
        if not passed:
            return ("permission hint: " + permission().get.__doc__,401), 'origin'
        key = cls + str(data)
        if r.exists(key):
            value = r.get(key)
            return (value, 200, {'Content-Type': 'application/json'}), 'origin'
        else:
            class MyEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, datetime):
                        return obj.strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(obj, date):
                        return obj.strftime('%Y-%m-%d')
                    else:
                        return json.JSONEncoder.default(self, obj)
            request.args = data
            value, type = resource().get(pk)
            to_chache = {'data': serializer.dump(value, type)}
            r.set(key, json.dumps(to_chache, cls=MyEncoder))
            return value, type

    def delete(self, request):
        return ('unimplament api', 401), 'origin'
