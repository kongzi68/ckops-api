# coding: utf-8
import logging
import sys
from . import auth
from .. import db
from ..models import Users
from config import Config
from datetime import datetime
from flask import g, request, abort
from ops.libs.errors import *
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

logger = logging.getLogger(__name__)
TOKEN_EXPIRATION = Config.TOKEN_EXPIRATION
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    user = Users.query.filter_by(username=username).first()
    if user:
        g.current_user = user
        logger.debug('TEST: {0}, {1}'.format(sys._getframe().f_code.co_name, user))
        if user.verify_password(password):
            return username
    else:
        g.current_user = None
        return False


@basic_auth.error_handler
def auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    logger.debug('TEST: {0}, {1}'.format(sys._getframe().f_code.co_name, token))
    return Users.verify_auth_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)


@auth.route('/user/test', methods=['GET'])
@multi_auth.login_required
def test_auth():
    return jsonify({"data": "123"})


def json_msg(status, msg, data=None):
    """
    :param status: 返回的状态码
    :param msg: 返回的消息内容
    :param data: 返回的数据
    :return:
    """
    if data:
        return jsonify({'status': status, 'data': data, 'msg': msg})
    else:
        return jsonify({'status': status, 'msg': msg})


@auth.route('/user/regist', methods=['POST'])
@multi_auth.login_required
def user_regist():
    logger.debug(request.values)
    username = request.values.get('username', None)
    password = request.values.get('password', None)
    if not username:
        return json_msg(400, '用户名必填')
    if len(password) < 6:
        return json_msg(200, '密码必须大于6位')
    ret = Users.query.filter_by(username=username).first()
    if ret is not None:
        return json_msg(200, '该用户已经注册')
    users = Users(
        username=username,
        created_at=datetime.now()
    )
    logger.debug("username: {0}, password: {1}".format(username, password))
    # 设置用户的密码
    users.hash_password(password)
    db.session.add(users)
    # 保存用户数据
    db.session.commit()
    return json_msg(200, '注册成功', {'user': username})


@auth.route('/user/change_password', methods=['POST'])
@multi_auth.login_required
def change_password():
    username = request.values.get('username', None)
    password = request.values.get('password', None)
    if not username:
        return json_msg(400, '用户名必填')
    ret = Users.query.filter_by(username=username).first()
    if ret:
        ret.hash_password(password)
        ret.updateed_at = datetime.now()
        db.session.commit()
        return json_msg(200, '修改密码成功')
    else:
        return json_msg(200, '用户名不存在')


@auth.route('/user/change_user_status', methods=['POST'])
@multi_auth.login_required
def change_user_status():
    username = request.values.get('username')
    is_valid = request.values.get('is_valid')
    if is_valid == 'True' or is_valid == '1':
        is_valid = True
    elif is_valid == 'False' or is_valid == '0':
        is_valid = False
    else:
        return json_msg(200, 'is_valid的值只能为: True or False')
    if not username:
        return json_msg(400, '用户名必填')
    ret = Users.query.filter_by(username=username).first()
    if ret:
        logger.debug(ret.is_valid)
        if ret.is_valid != is_valid:
            ret.is_valid = is_valid
            ret.updateed_at = datetime.now()
            db.session.commit()
            logger.debug(type(is_valid))
            if is_valid:
                return json_msg(200, '启用用户')
            else:
                return json_msg(200, '停用用户')
        else:
            return json_msg(200, '未修改用户状态')
    else:
        return json_msg(200, '用户名不存在')

