from app.database import db
from app.utils.db import Base



class Tasks(Base):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    deadline = db.Column(db.DateTime, default=None)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #comments = db.relationship('Comment', backref='tasks')

    def __str__(self):
        return self.name

