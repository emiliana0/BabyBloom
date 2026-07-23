from flask import Blueprint


children = Blueprint(
    'children',
    __name__
)


from app.children import routes