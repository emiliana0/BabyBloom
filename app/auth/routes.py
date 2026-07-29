from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app.auth import auth

from app.extensions import db

from app.models import User



@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.home")
        )


    if request.method == "POST":

        username = request.form["username"]

        email = request.form["email"]

        password = request.form["password"]



        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()



        if existing_user:

            flash(
                "Username or email already exists.",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )



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



        flash(
            "Registration successful. You can now log in.",
            "success"
        )



        return redirect(
            url_for("auth.login")
        )



    return render_template(
        "register.html"
    )





@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.home")
        )



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


            if user.is_admin:

                return redirect(
                    url_for("admin.dashboard")
                )



            return redirect(
                url_for("main.home")
            )




        flash(
            "Invalid email or password.",
            "danger"
        )



    return render_template(
        "login.html"
    )





@auth.route("/logout")
@login_required
def logout():


    logout_user()



    flash(
        "You have been logged out.",
        "info"
    )



    return redirect(
        url_for("main.home")
    )





@auth.route("/profile")
@login_required
def profile():


    return render_template(
        "profile.html"
    )