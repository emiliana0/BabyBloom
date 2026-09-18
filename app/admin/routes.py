from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user

from app.admin import admin
from app.extensions import db
from app.models import User, Child, Advice
from app.utils.decorators import admin_required


@admin.route("/admin")
@login_required
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")


@admin.route("/admin/users/<int:id>/make-admin", methods=["POST"])
@login_required
@admin_required
def make_admin(id):
    user = User.query.get_or_404(id)

    if user.is_admin:
        return redirect(url_for("admin.list_users"))

    user.is_admin = True
    db.session.commit()

    return redirect(url_for("admin.list_users"))


@admin.route("/admin/users/<int:id>/remove-admin", methods=["POST"])
@login_required
@admin_required
def remove_admin(id):
    user = User.query.get_or_404(id)

    if user.id == current_user.id:
        flash("You cannot remove your own administrator rights.", "danger")

        return redirect(url_for("admin.list_users"))

    user.is_admin = False
    db.session.commit()

    return redirect(url_for("admin.list_users"))


@admin.route("/admin/advice")
@login_required
@admin_required
def list_advice():
    advice_list = Advice.query.all()

    return render_template("admin/advice_list.html", advice_list=advice_list)


@admin.route("/admin/advice/create", methods=["GET", "POST"])
@login_required
@admin_required
def create_advice():
    if request.method == "POST":
        advice = Advice(
            title=request.form["title"],
            content=request.form["content"]
        )

        db.session.add(advice)
        db.session.commit()

        return redirect(url_for("admin.list_advice"))

    return render_template("admin/advice_create.html")


@admin.route("/admin/advice/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_advice(id):
    advice = Advice.query.get_or_404(id)

    if request.method == "POST":
        advice.title = request.form["title"]
        advice.content = request.form["content"]

        db.session.commit()

        return redirect(url_for("admin.list_advice"))

    return render_template("admin/advice_edit.html", advice=advice)


@admin.route("/admin/advice/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_advice(id):
    advice = Advice.query.get_or_404(id)

    db.session.delete(advice)
    db.session.commit()

    return redirect(url_for("admin.list_advice"))


@admin.route("/admin/users")
@login_required
@admin_required
def list_users():
    users = User.query.all()

    return render_template("admin/users.html", users=users)


@admin.route("/admin/users/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)

    deleting_self = user.id == current_user.id

    db.session.delete(user)
    db.session.commit()

    if deleting_self:
        logout_user()

        flash("Your account has been deleted.", "info")

        return redirect(url_for("main.home"))

    return redirect(url_for("admin.list_users"))


@admin.route("/admin/children")
@login_required
@admin_required
def list_children():
    children = Child.query.all()

    return render_template("admin/children.html", children=children)


@admin.route("/admin/children/delete/<int:id>", methods=["POST"])
@login_required
@admin_required
def delete_child(id):
    child = Child.query.get_or_404(id)

    db.session.delete(child)
    db.session.commit()

    return redirect(url_for("admin.list_children"))
