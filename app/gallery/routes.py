import os
import uuid
from datetime import datetime

from flask import (
    render_template, request, redirect, url_for, abort, current_app, flash
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import or_

from app.gallery import gallery
from app.extensions import db
from app.models import Child, Photo
from app.utils.permissions import has_child_access
from app.utils.decorators import user_required


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOADS_DIR = "uploads"
DATE_FORMAT = "%Y-%m-%d"
SORT_OLDEST = "oldest"
SORT_NEWEST = "newest"


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def apply_photo_filters(
    query, search=None, from_date=None, to_date=None, sort=SORT_NEWEST
):
    if search:
        query = query.filter(
            or_(
                Photo.title.ilike(f"%{search}%"),
                Photo.description.ilike(f"%{search}%")
            )
        )

    if from_date:
        query = query.filter(Photo.upload_date >= from_date)

    if to_date:
        query = query.filter(Photo.upload_date <= to_date)

    if sort == SORT_OLDEST:
        query = query.order_by(Photo.upload_date.asc())
    else:
        query = query.order_by(Photo.upload_date.desc())

    return query


@gallery.route("/children/<int:child_id>/gallery/upload", methods=["GET", "POST"])
@login_required
@user_required
def upload_photo(child_id):
    child = Child.query.get_or_404(child_id)

    if not has_child_access(child, current_user):
        abort(403)

    if request.method == "POST":
        file = request.files["photo"]

        if file.filename == "":
            flash("No file selected.", "danger")

            return redirect(url_for("gallery.upload_photo", child_id=child.id))

        if not allowed_file(file.filename):
            flash("Only PNG, JPG and JPEG files are allowed.", "danger")

            return redirect(url_for("gallery.upload_photo", child_id=child.id))

        extension = secure_filename(file.filename).rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4()}.{extension}"

        upload_folder = os.path.join(
            current_app.root_path, "static", UPLOADS_DIR, f"child_{child.id}"
        )

        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, filename))

        photo = Photo(
            title=request.form["title"],
            description=request.form["description"],
            filename=f"child_{child.id}/{filename}",
            original_filename=file.filename,
            upload_date=datetime.now().date(),
            child=child
        )

        db.session.add(photo)
        db.session.commit()

        flash("Photo uploaded successfully.", "success")

        return redirect(url_for("gallery.list_photos", child_id=child.id))

    return render_template("gallery/upload.html", child=child)


@gallery.route("/children/<int:child_id>/gallery")
@login_required
@user_required
def list_photos(child_id):
    child = Child.query.get_or_404(child_id)

    if not has_child_access(child, current_user):
        abort(403)

    query = apply_photo_filters(
        query=Photo.query.filter_by(child_id=child.id),
        search=request.args.get("search"),
        from_date=request.args.get("from_date"),
        to_date=request.args.get("to_date"),
        sort=request.args.get("sort", SORT_NEWEST)
    )

    return render_template(
        "gallery/list.html", child=child, photos=query.all()
    )


@gallery.route("/photos/<int:photo_id>/edit", methods=["GET", "POST"])
@login_required
@user_required
def edit_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    child = photo.child

    if not has_child_access(child, current_user):
        abort(403)

    if request.method == "POST":
        photo.title = request.form["title"]
        photo.description = request.form["description"]
        photo.upload_date = datetime.strptime(
            request.form["date"], DATE_FORMAT
        ).date()

        db.session.commit()

        return redirect(url_for("gallery.list_photos", child_id=child.id))

    return render_template("gallery/edit.html", photo=photo)


@gallery.route("/photos/<int:photo_id>/delete", methods=["POST"])
@login_required
@user_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    child = photo.child

    if not has_child_access(child, current_user):
        abort(403)

    file_path = os.path.join(
        current_app.root_path, "static", UPLOADS_DIR, photo.filename
    )

    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(photo)
    db.session.commit()

    return redirect(url_for("gallery.list_photos", child_id=child.id))
