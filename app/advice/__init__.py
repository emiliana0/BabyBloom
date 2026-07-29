from flask import Blueprint

advice = Blueprint(
    "advice",
    __name__
)

from app.advice import routes