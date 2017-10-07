# coding:utf-8
from SinglePage.serializer import serializer
from SinglePage.singlepage import SinglePage, app


def get_docs():
    resources = app.config['resources']
    docs = [[{"url": '/%s/' % resource, "resource": resources[resource].__doc__,
              "GET": resources[resource].get.__doc__,
              "PUT": resources[resource].put.__doc__,
              "POST": resources[resource].post.__doc__,
              "content": serializer.dump(resources[resource]()),
              "fileds": serializer.attr_dict_from_sqlalchemy_in_exclude(resources[resource]()),
              "DELETE": resources[resource].delete.__doc__}]
            for resource in resources if resource != 'query' and resource != 'doc']
    _docs = [[{"url": '/%s/' % resource, "resource": resources[resource].__doc__,
               "GET": resources[resource].get.__doc__,
               "PUT": resources[resource].put.__doc__,
               "POST": resources[resource].post.__doc__,
               "DELETE": resources[resource].delete.__doc__}]
             for resource in resources if resource == 'query' or resource == 'doc']
    docs.append(_docs)
    return docs


class Documents(SinglePage):
    """此资源可以将其它资源当作文档资源来使用，你可以使用此资源获得接口信息"""

    def get(self, cls):
        '你可以通过此资源获得所有资源情况'
        get_docs()
        return docs, 'basic'

    def get_permission_passed(self, pk):
        return True, None

    def put(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass
