from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean, String
from sqlalchemy.orm import backref, relation

from fbauth.model import DeclarativeBase, DBSession
from tgext.pluggable import app_model, primary_key

class FBAuthInfo(DeclarativeBase):
    __tablename__ = 'fbauth_info'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    registered = Column(Boolean, default=False, nullable=False)
    just_connected = Column(Boolean, default=False, nullable=False)
    profile_picture = Column(String(512), nullable=True)

    user_id = Column(Integer, ForeignKey(primary_key(app_model.User)), nullable=False)
    user = relation(app_model.User, backref=backref('fbauth', uselist=False, cascade='all, delete-orphan'))

    facebook_id = Column(Unicode(255), nullable=False, index=True, unique=True)
    access_token = Column(Unicode(255), nullable=False)
    access_token_expiry = Column(DateTime, nullable=False)

    @classmethod
    def user_by_facebook_id(cls, facebook_id):
        fbauth = DBSession.query(cls).filter_by(facebook_id=facebook_id).first()
        if not fbauth:
            return None
        return fbauth.user

