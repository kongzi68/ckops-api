# coding: utf-8
import logging
from flask import jsonify
from . import api
from ..models import ComEmployee
from .authentication import auth
# from .. import db

logger = logging.getLogger(__name__)

@auth.login_required
@api.route('/contact_list', methods=['GET'])
def get_contact_list():
    # all_employee = db.session.query(ComEmployee.name, ComEmployee.email, ComEmployee.phone).all()
    # print(all_employee)
    employees = ComEmployee.query.all()
    ret = jsonify([obj_item.query_contact_list() for obj_item in employees])
    return ret
