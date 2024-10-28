# coding: utf-8
import os
import logging
import sys
from . import db
from .libs.constants import UserStatusEnum
from flask_login import UserMixin
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import Config


logger = logging.getLogger(__name__)
Base = declarative_base()
metadata = Base.metadata
SECRET_KEY = Config.SECRET_KEY
logger.debug(SECRET_KEY)

class Users(UserMixin, db.Model):
    """
    用户
    不指定 __bind_key__ 的话，这个表使用配置：SQLALCHEMY_DATABASE_URI
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum(UserStatusEnum))
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    updateed_at = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime, doc=u"最后登录时间")

    def __repr__(self):
        return self.username

    def hash_password(self, password):
        """ 生成用户的hash密码 """
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """ 验证用户的password """
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration):
        jws = Serializer(SECRET_KEY, expires_in=expiration)
        return jws.dumps({'username': self.username})

    @staticmethod
    def verify_auth_token(token):
        jws = Serializer(SECRET_KEY)
        try:
            data = jws.loads(token)
            logger.debug('TEST: {0}, {1}'.format(sys._getframe().f_code.co_name, data))
        except:
            return False
        username = Users.query.filter_by(username=data['username']).first()
        logger.debug('TEST: {0}, {1}'.format(sys._getframe().f_code.co_name, username))
        if username:
            g.current_user = username
            return username
        else:
            g.current_user = None
            return False



class ComCompany(db.Model):
    __tablename__ = 'com_company'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True,  info='公司名')
    site = Column(String(200), nullable=False,  info='官网')
    address = Column(String(200), nullable=False,  info='公司地址')
    tel = Column(String(50), nullable=False,  info='公司联系电话')
    created_by = Column(Integer, nullable=False,  info='创建者')
    created_time = Column(DateTime, nullable=False,  info='创建时间')
    updated_by = Column(Integer, nullable=False,  info='更新人')
    updated_time = Column(DateTime, nullable=False,  info='更新时间')


class ComDepartment(db.Model):
    __tablename__ = 'com_department'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False,  info='部门名称')
    com_id = Column(Integer, nullable=False,  info='公司ID')
    created_by = Column(Integer, nullable=False,  info='创建者')
    created_time = Column(DateTime, nullable=False,  info='创建时间')
    updated_by = Column(Integer, nullable=False,  info='更新人')
    updated_time = Column(DateTime, nullable=False,  info='更新时间')


class ComEmployee(db.Model):
    __tablename__ = 'com_employee'
    """
    __table_args__ = (
        Index('t_index_01', 'server_id', 'game_id', unique=True),
    )
    """

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True,  info='姓名')
    en_name = Column(String(20), nullable=False, unique=True,  info='英文名')
    phone = Column(BigInteger, nullable=False, unique=True,  info='手机号码')
    email = Column(String(200), nullable=False,  info='邮箱')
    status = Column(Integer, nullable=False, index=True,  info='用户状态')
    com_id = Column(Integer, nullable=False,  info='公司ID')
    com_dept_id = Column(Integer, nullable=False, index=True,  info='部门ID')
    com_pos_id = Column(Integer, nullable=False,  info='职位ID')
    created_by = Column(Integer, nullable=False,  info='创建者')
    created_time = Column(DateTime, nullable=False,  info='创建时间')
    updated_by = Column(Integer, nullable=False,  info='更新人')
    updated_time = Column(DateTime, nullable=False,  info='更新时间')

    """
    def to_json(self):
        json_ret = {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'status': self.status,
            'com_id': self.com_id,
            'com_dept_id': self.com_dept_id,
            'com_pos_id': self.com_pos_id,
            'created_by': self.created_by,
            'created_time': self.created_time,
            'updated_by': self.updated_by,
            'updated_time': self.updated_time
        }
        return json_ret
    """

    def query_contact_list(self):
        json_ret = {
            'name': self.name,
            'en_name': self.en_name,
            'phone': self.phone,
            'email': self.email,
        }
        return json_ret
