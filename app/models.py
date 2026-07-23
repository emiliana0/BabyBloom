from app import db
from flask_login import UserMixin
from enum import Enum


class NoteCategory(Enum):

    HEALTH = "Health"

    FOOD = "Food"

    FIRST_TIMES = "First Times"

    OTHER = "Other"
    

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

    notes = db.relationship(
        "Note",
        back_populates="child",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Child {self.name}>"


class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    category = db.Column(db.Enum(NoteCategory), nullable=False)

    created_at = db.Column(
        db.Date,
        nullable=False
    )

    child_id = db.Column(
        db.Integer,
        db.ForeignKey("child.id"),
        nullable=False
    )

    child = db.relationship(
        "Child",
        back_populates="notes"
    )