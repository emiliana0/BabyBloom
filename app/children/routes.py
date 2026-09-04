from flask_login import login_required, current_user
from app.extensions import db
from app.models import Child
from app.children import children
from datetime import datetime


from flask import (
    render_template,
    request,
    redirect,
    url_for,
    abort
)

from app.utils.permissions import has_child_access, is_child_parent
from app.utils.decorators import user_required




@children.route('/children/create', methods=['GET','POST'])
@login_required
@user_required
def create_child():

    if request.method == 'POST':

        name = request.form['name']
        birth_date = datetime.strptime(
            request.form['birth_date'],
            '%Y-%m-%d'
        ).date()


        child = Child(
            name=name,
            birth_date=birth_date,
            parent=current_user
        )


        db.session.add(child)
        db.session.commit()


        return redirect(
            url_for('children.my_children')
        )


    return render_template(
        'children/create.html'
    )

@children.route('/children')
@login_required
@user_required
def my_children():

    children = current_user.children

    shared_children = [
        access.child
        for access in current_user.shared_children
    ]


    return render_template(
        'children/list.html',
        children=children,
        shared_children=shared_children
    )

@children.route('/children/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@user_required
def edit_child(id):

    child = Child.query.get_or_404(id)


    if not is_child_parent(child, current_user):
        abort(403)


    if request.method == 'POST':

        child.name = request.form['name']

        child.birth_date = datetime.strptime(
            request.form['birth_date'],
            '%Y-%m-%d'
        ).date()


        db.session.commit()


        return redirect(
            url_for('children.my_children')
        )


    return render_template(
        'children/edit.html',
        child=child
    )

@children.route('/children/delete/<int:id>', methods=['POST'])
@login_required
@user_required
def delete_child(id):

    child = Child.query.get_or_404(id)


    if not is_child_parent(child, current_user):
        abort(403)


    db.session.delete(child)
    db.session.commit()


    return redirect(
        url_for('children.my_children')
    )

@children.route("/children/<int:id>")
@login_required
def view_child(id):

    child = Child.query.get_or_404(id)

    if not has_child_access(child, current_user):
        abort(403)

    return render_template(
        "children/details.html",
        child=child
    )