# coding: utf-8
import logging
from . import api
from flask import g
from flask_httpauth import HTTPBasicAuth
from ..models import Users
from .errors import *
from .other import AnonymousUser


logger = logging.getLogger(__name__)
auth = HTTPBasicAuth()


@api.before_request
@auth.login_required
def before_request():
    logger.debug('1')
    if g.current_user.is_anonymous and g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@auth.verify_password
def verify_password(username_or_token, password):
    # logger.debug(username_or_token)
    if username_or_token == '':
        g.current_user = AnonymousUser()
        return False
    if password == '':
        # logger.debug('333333')
        g.current_user = Users.verify_auth_token(username_or_token)
        g.token_used = True
        # logger.debug(g.current_user)
        return g.current_user is not None
    # first try to authenticate by token
    user = Users.verify_auth_token(username_or_token)
    # logger.debug(user)
    if not user:
        # try to authenticate with username/password
        user = Users.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    # logger.debug('3')
    g.current_user = user
    g.token_used = False
    # ret = user.verify_password(password)
    # logger.debug(ret)
    # return user.verify_password(password)
    return True

@auth.error_handler
def auth_error():
    logger.debug('2')
    return unauthorized('Invalid credentials')


@api.route('/posts/')
def get_posts():
    pass


@api.route('/token')
def get_token():
    logger.debug(g.token_used)
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    token = g.current_user.generate_auth_token(expiration=600)
    # logger.debug(type(token))
    # logger.debug(token)
    return jsonify({'token': token.decode(), 'expiration': 600})
