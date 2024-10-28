# coding: utf-8
from flask import jsonify


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def notfound(message):
    response = jsonify({'error': 'notfound', 'message': message})
    response.status_code = 404
    return response
