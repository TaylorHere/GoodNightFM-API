from .permission import permission
from .serializer import serializer
from sqlalchemy import text, desc
from sqlalchemy.orm import joinedload, load_only
from .singlepage import SinglePage
from .singlepage import *


class GeneralViewWithSQLAlchemy(SinglePage):
    """docstring for GeneralView"""

    def filter(self, query, value):
        return query.filter(text(value))

    def asc_order_by(self, query, value):
        return query.order_by(text(value))

    def desc_order_by(self, query, value):
        return query.order_by(desc(text(value)))

    def limit(self, query, value):
        return query.limit(value)

    def offset(self, query, value):
        offset = int(value)
        if offset > 0:
            return query.offset(offset - 1)
        else:
            return query

    def includes(self, query, value):
        key = value.split(',')
        _query = query
        for k in key:
            extends_resources = app.config['resources'][k]
            self.extends_class.update({k: extends_resources})
            _query = _query.options(joinedload(k))
        return _query

    def fileds(self, query, value):
        vs = value.split(',')
        exclude = self.__exclude__
        self.set_exclude([])
        members = serializer.dump(self)
        self.set_exclude([e for e in members if e not in vs] + list(exclude))
        for v in vs:
            query.options(load_only(v))
        return query

    db_session = None
    real_delete = True
    # 过滤器实现于args名称字典
    __in_exclude__ = []
    # 定义哪些字段不展示给前端
    __exclude__ = []
    # 定义属性装饰方法
    __property__ = {}
    __permission__ = [permission]
    __query_args__ = [{'filter': filter}, {'asc_order_by': asc_order_by}, {
        'desc_order_by': desc_order_by}, {'offset': offset}, {
        'limit': limit}, {'fileds': fileds}, {'includes': includes}]
    ########################
    #      权限处理

    def set_permission(self, permission):
        self.__permission__ = permission

    def set_exclude(self, exclude):
        self.__exclude__ = exclude

    def set_in_exclude(self, in_exclude):
        self.__in_exclude__ = in_exclude

    def get_permission_passed(self, pk):
        for permission in self.__permission__:
            passed, memo, status_code = permission().get(
                self.db_session, self.object, pk, self)
            if not passed:
                return False, permission, memo, status_code
        return True, None, None, 200

    def put_permission_passed(self, pk):
        for permission in self.__permission__:
            passed, memo, status_code = permission().put(
                self.db_session, self.object, pk, self)
            if not passed:
                return False, permission, memo, status_code
        return True, None, None, 200

    def post_permission_passed(self):
        for permission in self.__permission__:
            passed, memo, status_code = permission().post(
                self.db_session, self.object, self)
            if not passed:
                return False, permission, memo, status_code
        return True, None, None, 200

    def delete_permission_passed(self, pk):
        for permission in self.__permission__:
            passed, memo, status_code = permission().delete(
                self.db_session, self.object, pk, self)
            if not passed:
                return False, permission, memo, status_code
        return True, None, None, 200
    ########################
    #  hook

    def get_hook_on_get_query(self, query):
        return query

    def post_hook_before_create_object(self, data):
        return data

    ########################
    #  http method
    def get(self, pk, *args, **kwargs):
        '获取资源列表或资源'
        self.extends_class = {}
        passed, permission, memo, status_code = self.get_permission_passed(pk)
        if not passed:
            if memo is not None:
                return (memo, status_code), 'origin'
            return (permission().get.__doc__, status_code), 'origin'
        if pk is not None:
            query = self.db_session.query(
                self.object).filter(self.object.id == pk)
        else:
            query = self.db_session.query(self.object)
        for arg in self.__query_args__:
            value = request.args.get(list(arg.keys())[0], None)
            if value is not None:
                query = list(arg.values())[0](self, query, value)
        query = self.get_hook_on_get_query(query)
        return query, 'sqlalchemy'

    def post(self, *args, **kwargs):
        '新建该资源'
        # 获取request的json并新建一个用户
        passed, permission, memo, status_code = self.post_permission_passed()
        if not passed:
            if memo is not None:
                return (memo, status_code), 'origin'
            return (permission().post.__doc__, status_code), 'origin'
        class_dict = serializer.attr_dict_from_sqlalchemy_in_exclude(self)
        data = request.get_json()
        if data is not None:
            try:
                for key in class_dict:
                    value = data[key]
            except KeyError as e:
                return ('if you want to create a new resources, you need thoese keywords: %s,and you miss this key %s' % (' ,'.join(class_dict), key), 403), 'origin'
        data = self.post_hook_before_create_object(data)
        obj = self.create_object(data)
        self.db_session.add(obj)
        self.db_session.commit()
        return obj, 'sqlalchemy'

    def delete(self, pk, *args, **kwargs):
        '删除一个资源'
        passed, permission, memo, status_code = self.delete_permission_passed(
            pk)
        if not passed:
            if memo is not None:
                return (memo, status_code), 'origin'
            return (permission().delete.__doc__, status_code), 'origin'
        if self.real_delete:
            if pk is not None:
                self.db_session.query(self.object).filter(
                    self.object.id == pk).delete()
                self.db_session.commit()
                return self.db_session().query(self.object).filter(
                    self.object.id == pk), 'sqlalchemy'
            else:
                return 'need pk', 'basic'
        else:
            if pk is not None:
                self.db_session().query(self.object).filter(
                    self.object.id == pk).update({self.object.deleted: True})
                self.db_session().commit()
                return self.db_session().query(self.object).filter(
                    self.object.id == pk), 'sqlalchemy'
            else:
                return 'need pk', 'basic'

    def put(self, pk, *args, **kwargs):
        '更新一个资源'
        passed, permission, memo, status_code = self.put_permission_passed(
            pk)
        if not passed:
            if memo is not None:
                return (memo, status_code), 'origin'
            return (permission().put.__doc__, status_code), 'origin'
        if pk is not None:
            query = self.db_session().query(self.object).filter(
                self.object.id == pk)
            self = query.first()
            data = request.json
            properties = [d for d in data if d in self.__property__]
            for d in properties:
                setattr(self, d, data[d])
                value = getattr(self, d)
                del data[d]
                data[self.__property__[d]] = value
            if data != {}:
                query.update(data)
            self.db_session().commit()
            return self.db_session().query(self.object).filter(
                self.object.id == pk), 'sqlalchemy'
        else:
            return 'need pk', 'basic'
