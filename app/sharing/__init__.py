from flask import Blueprint

sharing = Blueprint(
    "sharing",
    __name__
)

from app.sharing import routes