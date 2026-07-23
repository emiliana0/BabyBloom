from flask import Blueprint


notes = Blueprint(
    'notes',
    __name__
)


from app.notes import routes