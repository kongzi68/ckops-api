# coding: utf-8
import logging
import sys
from . import api
from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from ..models import Users
from ops.libs.errors import *
from config import Config

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


@api.route('/token/')
@multi_auth.login_required
def get_token():
    logger.debug('TEST: {0}, {1}'.format(sys._getframe().f_code.co_name, g.current_user))
    if g.current_user:
        logger.debug('TEST: {0}, {1}'.format(sys._getframe().f_code.co_name, TOKEN_EXPIRATION))
        logger.debug('TEST: {0}, {1}'.format(sys._getframe().f_code.co_name, type(TOKEN_EXPIRATION)))
        token = g.current_user.generate_auth_token(expiration=TOKEN_EXPIRATION)
        return jsonify({'token': token.decode(), 'expiration': TOKEN_EXPIRATION})

# SLB 健康状态检查
@api.route('/checkstatus/')
def check_status():
    return  jsonify({'status':True})