import os
from flask_bootstrap import Bootstrap
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor
from flask import abort
from flask_login import LoginManager, current_user
from models import User, app, db
from functools import wraps

OWN_EMAIL = os.getenv("OWN_EMAIL")
OWN_PASSWORD = os.getenv("OWN_PASSWORD")

ckeditor = CKEditor(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

# CONNECT TO DB


gravatar = Gravatar(app, size=30, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False,
                    base_url=None)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(entity=User, ident=user_id)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function
