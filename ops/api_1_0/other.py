# coding: utf-8
from flask_login import AnonymousUserMixin
from .. import login_manager


def confirmed(self):
    status = self.status
    if status == 1:
        return True
    else:
        return False


class AnonymousUser(AnonymousUserMixin):

    def can(self):
        return False

    # confirmed = False
    @property
    def confirmed(self):
        return False


login_manager.anonymous_user = AnonymousUser
