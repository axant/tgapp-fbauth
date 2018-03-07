# -*- coding: utf-8 -*-

from ming import schema as s
from ming.odm import FieldProperty, RelationProperty, ForeignIdProperty
from ming.odm.declarative import MappedClass
from fbauth.model import DBSession


class FBAuthInfo(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'fbauth_info'
        indexes = [(('_user_id', ), )]

    _id = FieldProperty(s.ObjectId)
    registered = FieldProperty(s.Bool, if_missing=False)
    just_connected = FieldProperty(s.Bool, if_missing=False)
    profile_picture = FieldProperty(s.String)

    _user_id = ForeignIdProperty('User')
    user = RelationProperty('User')

    facebook_id = FieldProperty(s.String, required=True)
    access_token = FieldProperty(s.String, required=True)
    access_token_expiry = FieldProperty(s.DateTime, required=True)

    @classmethod
    def user_by_facebook_id(cls, facebook_id):
        return cls.query.find({'facebook_id': facebook_id}).first()

    @classmethod
    def fbauth_user(cls, user_id):
        return cls.query.find({'_user_id': user_id}).first()
