from app import db
from flask_login import UserMixin
from enum import Enum


class NoteCategory(Enum):

    HEALTH = "Health"
    FOOD = "Food"
    FIRST_TIMES = "First Times"
    OTHER = "Other"

class RequestStatus(Enum):
    
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


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

    shared_children = db.relationship(
        "SharedAccess",
        backref="user",
        cascade="all, delete-orphan"
    )

    is_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False
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

    photos = db.relationship(
        "Photo",
        back_populates="child",
        cascade="all, delete"
    )

    shared_users = db.relationship(
        "SharedAccess",
        backref="child",
        cascade="all, delete-orphan"
    )

    share_codes = db.relationship(
        "ShareCode",
        back_populates="child",
        cascade="all, delete-orphan"
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


class Photo(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    original_filename = db.Column(
        db.String(255),
        nullable=False
    )

    upload_date = db.Column(
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
        back_populates="photos"
    )

class ShareCode(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    code = db.Column(
        db.String(6),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    used = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    child_id = db.Column(
        db.Integer,
        db.ForeignKey("child.id"),
        nullable=False
    )

    child = db.relationship(
        "Child",
        back_populates="share_codes"
    )

class AccessRequest(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    requester_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    child_id = db.Column(
        db.Integer,
        db.ForeignKey("child.id")
    )

    status = db.Column(
        db.Enum(RequestStatus),
        default=RequestStatus.PENDING,
        nullable=False
    )

    requester = db.relationship(
        "User",
        backref="access_requests"
    )

    child = db.relationship(
        "Child",
        backref="access_requests"
    )

class SharedAccess(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    child_id = db.Column(
        db.Integer,
        db.ForeignKey("child.id")
    )

class Advice(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )