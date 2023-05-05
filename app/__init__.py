from flask import Flask
from flask_login import LoginManager
from .database import db
from flask_wtf.csrf import CSRFProtect
from app.login.models import Users

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")
    csrf.init_app(app)

    db.init_app(app)
    lm = LoginManager(app)
    lm.login_view = 'login.auth'

    @lm.user_loader
    def load_user(user_id):
        return db.session.query(Users).get(user_id)

    with app.test_request_context():
        db.create_all()

    # if app.debug == True:
    #     try:
    #         from flask_debugtoolbar import DebugToolbarExtension
    #         toolbar = DebugToolbarExtension(app)
    #     except:
    #         pass

    import app.tasks.controllers as tasks
    import app.login.controllers as login
    # import app.comment.controllers as comment

    app.register_blueprint(tasks.module)
    app.register_blueprint(login.module)
    # app.register_blueprint(comment.module)

    return app
