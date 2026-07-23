from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    children = db.relationship(
    'Child',
    back_populates='parent',
    cascade='all, delete'
    )

    def __repr__(self):
        return f"<User {self.username}>"
    
    
class Child(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    birth_date = db.Column(
        db.Date,
        nullable=False
    )

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    parent = db.relationship(
        'User',
        back_populates='children'
    )

    def __repr__(self):
        return f"<Child {self.name}>"