# coding: utf-8
import logging
from flask import jsonify
from ..models import ComEmployee
from . import api
from .api_auth import multi_auth, basic_auth, token_auth
# from .. import db

logger = logging.getLogger(__name__)


@api.route('/contact_list', methods=['GET'])
@multi_auth.login_required
def get_contact_list():
    # all_employee = db.session.query(ComEmployee.name, ComEmployee.email, ComEmployee.phone).all()
    # print(all_employee)
    employees = ComEmployee.query.all()
    ret = jsonify([obj_item.query_contact_list() for obj_item in employees])
    return ret
