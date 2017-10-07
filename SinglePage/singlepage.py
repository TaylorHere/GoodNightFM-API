# coding: utf-8
import inspect

from flask import *
from flask.views import *
from .serializer import *

app = Flask(__name__)
app.config['resources'] = {}


def register(cls, endpoint=''):
    endpoint = endpoint
    view = cls.as_view(cls.__name__)
    cls.pk_list = {}
    resource_name = endpoint.replace('/', '')
    app.config['resources'].update({resource_name: cls})
    for method in cls.methods:
        lowcase_method = method.lower()
        try:
            func = getattr(cls, lowcase_method)
        except AttributeError as e:
            pass
        args = []
        defaults = []
        if inspect.getargspec(func)[0] is not None:
            args = [e for e in inspect.getargspec(
                func)[0] if e is not 'self']

        if inspect.getargspec(func)[3] is not None:
            defaults = [e for e in inspect.getargspec(
                func)[3] if e is not 'self']
        defaults_dict = dict([(arg, default)
                              for arg in args for default in defaults])
        for arg in args:
            cls.pk_list.update({lowcase_method: arg})
            app.add_url_rule(endpoint + '<' + arg + '>',
                             view_func=view, defaults=defaults_dict, methods=[method, ])
    cls.object = cls
    cls().add_args()
    app.add_url_rule(endpoint, view_func=view)


class SinglePage(View):
    """this is the base class of single page"""
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    pk_list = {}
    object = None
    extends_class = {}

    def get(self, *args, **kargs):
        pass

    def post(self, *args, **kargs):
        pass

    def put(self, *args, **kargs):
        pass

    def delete(self, *args, **kargs):
        pass

    def add_args(self):
        pass

    def create_object(self, json=None):
        if json is not None:
            class_dict = serializer.attr_dict_from_sqlalchemy_in_exclude(self)
            for item in class_dict:
                setattr(self, item, json[item])
        return self

    def make_links(self, response):
        """
        ~ 一个指向集合资源的 self 链接。
        ~ 如果集合是分页的，并且还有下一页，要有一个指向下一页的链接。 
        ~ 如果集合是分页的，并且还有上一页，要有一个指向上一页的链接。
        ~ 一个集合大小的指示符。
        """
        link = {}
        root = request.url_root[0:len(request.url_root)-1]
        url = request.url
        base = request.base_url
        path = request.path
        next_url = ''
        prev_url = ''
        self_url = request.url
        args_str = url.replace(base, '')
        args_dict = request.args
        if args_dict.get('offset', None):
            next = args_dict.get('offset', None, type=int) + 1
            perv = args_dict.get('offset', None, type=int) - 1
            orgin_offset = 'offset='+args_dict.get('offset', None)
            next_str = args_str.replace(orgin_offset, 'offset=' + str(next))
            prev_str = args_str.replace(orgin_offset, 'offset=' + str(perv))
            next_url = base + next_str
            prev_url = base + prev_str
        else:
            path_list = path.split('/')
            if path_list[-1] != '':
                pk = int(path_list[-1])
                next = '/' + path_list[1] + '/' + str(pk + 1)
                prev = '/' + path_list[1] + '/' + str(pk - 1)
                next_url = root + next + args_str
                prev_url = root + prev + args_str
            else:
                next_url = self_url
                prev_url = self_url
        link.update({'count': response.count()})
        link.update({'self': self_url})
        link.update({'next': next_url})
        link.update({'prev': prev_url})
        return link

    def json_response(self, response, class_type):
        serializer = Serializer()
        serializer.class_type = class_type
        serializer.register_structure(self, self.extends_class)

        if class_type == 'origin':
            return response
        if class_type == 'basic':
            return jsonify(response)
        if class_type == 'sqlalchemy':
            response = serializer.dump(response)
            return jsonify(response)

    def dispatch_request(self, *args, **kwargs):
        if request.method == 'GET':
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['get']: None}
                except KeyError as e:
                    pass
            response, class_type = self.get(*args, **kwargs)
            return self.json_response(response, class_type)
        elif request.method == 'POST':
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['post']: None}
                except KeyError as e:
                    pass
            response, class_type = self.post(*args, **kwargs)
            return self.json_response(response, class_type)
        elif request.method == 'PUT':
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['put']: None}
                except KeyError as e:
                    pass
            response, class_type = self.put(*args, **kwargs)
            return self.json_response(response, class_type)
        elif request.method == 'DELETE':
            if kwargs == {}:
                try:
                    kwargs = {self.pk_list['delete']: None}
                except KeyError as e:
                    pass
            response, class_type = self.delete(*args, **kwargs)
            return self.json_response(response, class_type)
