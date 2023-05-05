from sqlalchemy import event

from app.database import db

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    content = db.Column(db.Text())

    tasks_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

    def __str__(self):
        return self.name