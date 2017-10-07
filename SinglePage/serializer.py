from datetime import datetime
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.attributes import InstrumentedAttribute
import copy


class Serializer():

    structures = {}
    # structures =
    # {
    #   User:
    #    {
    #      'name':'','gender':''
    #    },
    # }
    #

    def register_structure(self, instance, extends=None):
        self.class_type='structures'
        self.structures.update({type(instance): self.attr_dict_from_sqlalchemy_structures(instance)})
        for key, value in extends.items():
            self.structures.update({value: self.attr_dict_from_sqlalchemy_structures(value)})

    def dump(self, origin_instance, class_type='sqlalchemy'):
        # class_type choice 'sqlalchemy', 'basic'
        self.class_type = class_type
        if self.class_type == 'sqlalchemy':
            if isinstance(origin_instance, Query):
                origin_instance = origin_instance.all()
            return self.typping(origin_instance)
        elif self.class_type == 'basic':
            return self.typping(origin_instance)

    def cycling(self, instance):

        if isinstance(instance, (set, list)):
            m_list = []
            for item in instance:
                value = self.typping(item)
                m_list.append(value)
            return m_list
        if isinstance(instance, dict):
            m_dict = {}
            for item in instance:
                value = self.typping(instance[item])
                m_dict.update({item: value})
            return m_dict

    def typping(self, instance):
        if isinstance(instance, set):
            return self.cycling(instance)
        elif isinstance(instance, list):
            return self.cycling(instance)
        elif isinstance(instance, dict):
            return self.cycling(instance)
        elif isinstance(instance, (float, int, str, bytes, bool)):
            return instance
        elif isinstance(instance, datetime):
            return instance
        elif instance is None:
            return None
        else:
            return self.typping(self.mapping(instance))

    def mapping(self, instance):
        _type = type(instance)
        if self.structures.get(_type, None):
            return self.mapping_by_structure(instance)
        elif self.class_type == 'basic':
            return self.attr_dict_from_basic(instance)
        elif self.class_type == 'sqlalchemy':
            return self.attr_dict_from_sqlalchemy(instance)
        elif self.class_type == 'structures':
            return self.attr_dict_from_sqlalchemy_structures(instance)

    def mapping_by_structure(self, origin_instance):
        _type = type(origin_instance)
        structure = self.structures.get(_type, None)
        response = copy.copy(structure)
        for s in structure:
            value = getattr(origin_instance, s, None)
            response.update({s: value})
        return response

    def attr_dict_from_basic(self, instance):
        try:
            exclude = [e for e in instance.__exclude__]
        except:
            exclude = []
        full = dict([[e, getattr(instance, e)] for e in dir(instance)
                     if not e.startswith('_') and not hasattr(
                         getattr(instance, e), '__call__') and e not in exclude])
        propery = dict([[p, getattr(instance, e).__get__(instance, type(instance))]
                        for p in full if hasattr(full[p], 'fset')])
        full.update(propery)
        return full

    def attr_dict_from_sqlalchemy(self, instance):
        try:
            exclude = [e for e in instance.__exclude__]
        except:
            exclude = []
        try:
            property = [p for p in instance.__property__]
        except:
            property = []
        full = dict([[e, getattr(instance, e, None)]
                     for e in instance.__mapper__.c.keys() if e not in exclude])
        property = dict([[e, getattr(instance, e, None)]
                         for e in dir(instance) if e in property and e not in exclude])
        full.update(property)
        return full
    def attr_dict_from_sqlalchemy_structures(self, instance):
        try:
            exclude = [e for e in instance.__exclude__]
        except:
            exclude = []
        try:
            property = [p for p in instance.__property__]
        except:
            property = []
        full = dict([[e, None]
                     for e in instance.__mapper__.c.keys() if e not in exclude])
        relationships = dict([[e, None]
                     for e in instance.__mapper__.relationships.keys() if e not in exclude])
        property = dict([[e, None]
                         for e in dir(instance) if e in property and e not in exclude])
        full.update(property)
        full.update(relationships)
        return full

    def attr_dict_from_sqlalchemy_in_exclude(self, instance):
        try:
            in_exclude = [e for e in instance.__in_exclude__]
        except:
            in_exclude = []
        try:
            property = [p for p in instance.__property__]
        except:
            property = []
        full = dict([[e, getattr(instance, e, None)]
                     for e in instance.__mapper__.c.keys() if e not in in_exclude])
        property = dict([[e, getattr(instance, e, None)]
                         for e in dir(instance) if e in property and e not in in_exclude])
        full.update(property)
        return full

serializer = Serializer()
