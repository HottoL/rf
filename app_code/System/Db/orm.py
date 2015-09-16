#orm.py
# -*- coding: utf-8 -*-

class Field(object):
    def __init__(self, column_type, primary_key=False):
        self.column_type = column_type
        self.primary_key = primary_key
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class IntegerField(Field):
    def __init__(self, primary_key=False):
        super(IntegerField, self).__init__('int', primary_key)

class StringField(Field):
    def __init__(self, primary_key=False):
        super(StringField, self).__init__('varchar(100)', primary_key)

class ModelMetaclass(type): 
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mapping = dict()
        for k,v in attrs.iteritems():
            if isinstance(v, Field):
                mapping[k] = v
                #is it primary_key?
                if v.primary_key:   
                    primary_key = k
        #delete key from son class  
        for k in mapping.iterkeys():
            attrs.pop(k)
        #__table__ = cls.__table__

        attrs['__mapping__'] = mapping
        attrs['__primary_key__'] = primary_key
        #attrs['__table__'] = __table__

        return type.__new__(cls, name, bases, attrs)

class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def get(cls, pk):
        d = db.select_one('select * from %s where %s=?' % (cls.__table__, cls.__primary_key__.name), pk)
        return cls(**d) if d else None

    def insertTable(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mapping__.iteritems():
            fields.append(k)
            params.append('?')
            args = append(getattr(self, k, None))

        db.insert(self.__table__, **params)
        return self

    def insertTableMulti(self):
        fields = []
        params = []





