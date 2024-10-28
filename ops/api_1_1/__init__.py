from flask import Blueprint

api = Blueprint('api_1_1', __name__)

from . import employee, api_auth, call_phone