import os
import uuid

from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    abort,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from app.gallery import gallery
from app.extensions import db
from app.models import Child, Photo

from app.utils.permissions import has_child_access

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg"
}


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@gallery.route(
    "/children/<int:child_id>/gallery/upload",
    methods=["GET", "POST"]
)
@login_required
def upload_photo(child_id):

    child = Child.query.get_or_404(child_id)

    if not has_child_access(child, current_user):
        abort(403)

    if request.method == "POST":

        file = request.files["photo"]

        if file.filename == "":
            return "No selected file"

        if not allowed_file(file.filename):
            return "Invalid file type"

        original_filename = file.filename

        safe_filename = secure_filename(file.filename)

        extension = safe_filename.rsplit(
            '.',
            1
        )[1].lower()

        filename = f"{uuid.uuid4()}.{extension}"

        upload_folder = os.path.join(
            current_app.root_path,
            "static",
            "uploads",
            f"child_{child.id}"
        )

        os.makedirs(upload_folder, exist_ok=True)

        file.save(
            os.path.join(upload_folder, filename)
        )

        photo = Photo(
            title=request.form["title"],
            description=request.form["description"],
            filename=f"child_{child.id}/{filename}",
            original_filename=original_filename,
            upload_date=datetime.now().date(),
            child=child
        )

        db.session.add(photo)
        db.session.commit()

        return redirect(
            url_for(
                "gallery.list_photos",
                child_id=child.id
            )
        )

    return render_template(
        "gallery/upload.html",
        child=child
    )

@gallery.route(
    "/children/<int:child_id>/gallery"
)
@login_required
def list_photos(child_id):

    child = Child.query.get_or_404(child_id)

    if not has_child_access(child, current_user):
        abort(403)

    photos = Photo.query.filter_by(
        child_id=child.id
    ).order_by(
        Photo.upload_date.desc()
    ).all()

    return render_template(
        "gallery/list.html",
        child=child,
        photos=photos
    )

@gallery.route(
    "/photos/<int:photo_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_photo(photo_id):

    photo = Photo.query.get_or_404(photo_id)

    child = photo.child

    if not has_child_access(child, current_user):
        abort(403)


    if request.method == "POST":

        photo.title = request.form["title"]

        photo.description = request.form["description"]

        photo.upload_date = datetime.strptime(
            request.form["date"],
            "%Y-%m-%d"
        ).date()


        db.session.commit()


        return redirect(
            url_for(
                "gallery.list_photos",
                child_id=child.id
            )
        )


    return render_template(
        "gallery/edit.html",
        photo=photo
    )

@gallery.route(
    "/photos/<int:photo_id>/delete",
    methods=["POST"]
)
@login_required
def delete_photo(photo_id):

    photo = Photo.query.get_or_404(photo_id)


    child = photo.child


    if not has_child_access(child, current_user):
        abort(403)



    file_path = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        photo.filename
    )


    if os.path.exists(file_path):

        os.remove(file_path)



    db.session.delete(photo)

    db.session.commit()


    return redirect(
        url_for(
            "gallery.list_photos",
            child_id=child.id
        )
    )