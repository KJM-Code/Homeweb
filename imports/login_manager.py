# -*- coding: utf-8 -*-

from flask_login import LoginManager, login_required, login_user, logout_user, user_logged_in

#Imports/
from modules.users.database import SYS_USERS


login_manager = LoginManager()
login_manager.login_view = 'Users.login'

@login_manager.user_loader
def load_user(user_id):
    return SYS_USERS.query.get(int(user_id))


