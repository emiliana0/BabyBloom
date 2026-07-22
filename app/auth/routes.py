from flask import render_template, request, redirect, url_for

from app.auth import auth

from app.extensions import db

from app.models import User

from werkzeug.security import generate_password_hash


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]


        hashed_password = generate_password_hash(
            password
        )


        user = User(
            username=username,
            email=email,
            password=hashed_password
        )


        db.session.add(user)

        db.session.commit()


        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "register.html"
    )


from flask_login import login_user

from werkzeug.security import check_password_hash



@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]


        user = User.query.filter_by(
            email=email
        ).first()


        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)


            return redirect(
                url_for("main.home")
            )


    return render_template(
        "login.html"
    )

from flask_login import logout_user


@auth.route("/logout")
def logout():

    logout_user()


    return redirect(
        url_for("main.home")
    )

from flask_login import login_required


@auth.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html"
    )