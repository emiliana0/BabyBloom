from flask import (
    render_template,
    request,
    redirect,
    url_for,
    abort
)

from flask_login import (
    login_required,
    current_user
)

from datetime import datetime

from app.notes import notes
from app.extensions import db
from app.models import Child, Note, NoteCategory

from app.utils.permissions import has_child_access


@notes.route(
    '/children/<int:child_id>/notes/create',
    methods=['GET', 'POST']
)
@login_required
def create_note(child_id):

    child = Child.query.get_or_404(child_id)


    if not has_child_access(child, current_user):
        abort(403)


    if request.method == 'POST':

        note = Note(

            title=request.form['title'],

            content=request.form['content'],

            category=NoteCategory[request.form['category']],

            created_at=datetime.now().date(),

            child=child
        )


        db.session.add(note)

        db.session.commit()


        return redirect(
            url_for(
                'notes.list_notes',
                child_id=child.id
            )
        )


    return render_template(
        'notes/create.html',
        child=child
    )

@notes.route(
    '/children/<int:child_id>/notes'
)
@login_required
def list_notes(child_id):

    child = Child.query.get_or_404(child_id)


    if not has_child_access(child, current_user):
        abort(403)


    query = Note.query.filter_by(
        child_id=child.id
    )


    category = request.args.get(
        'category'
    )


    date = request.args.get(
        'date'
    )


    if category:
        query = query.filter_by(
            category=category
        )


    if date:
        query = query.filter(
            Note.created_at.like(
                f'{date}%'
            )
        )


    notes = query.all()


    return render_template(
        'notes/list.html',
        notes=notes,
        child=child
    )

@notes.route(
    '/notes/<int:id>/edit',
    methods=['GET','POST']
)
@login_required
def edit_note(id):

    note = Note.query.get_or_404(id)


    if not has_child_access(note.child, current_user):
        abort(403)



    if request.method == 'POST':

        note.title = request.form['title']

        note.content = request.form['content']

        note.category = NoteCategory[request.form['category']]


        db.session.commit()


        return redirect(
            url_for(
                'notes.list_notes',
                child_id=note.child_id
            )
        )


    return render_template(
        'notes/edit.html',
        note=note
    )

@notes.route(
    '/notes/<int:id>/delete',
    methods=['POST']
)
@login_required
def delete_note(id):

    note = Note.query.get_or_404(id)


    if not has_child_access(note.child, current_user):
        abort(403)


    db.session.delete(note)

    db.session.commit()


    return redirect(
        url_for(
            'notes.list_notes',
            child_id=note.child_id
        )
    )