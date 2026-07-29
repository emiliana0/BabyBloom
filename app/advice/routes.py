from flask import render_template
from flask_login import login_required

from app.advice import advice
from app.models import Advice

from app.utils.decorators import user_required

@login_required
@user_required
@advice.route("/advice")
def list_advice():

    advice_list = Advice.query.all()

    return render_template(
        "advice/list.html",
        advice_list=advice_list
    )