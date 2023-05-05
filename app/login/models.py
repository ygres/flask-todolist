from app.database import db
from app.utils.db import Base
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import UserMixin

class Users(Base, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    # tasks_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    task = db.relationship('Tasks', backref='user_task')

    def __repr__(self):
        return "<{}>".format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password, password)
