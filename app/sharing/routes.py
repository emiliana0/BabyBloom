import random
import string
from datetime import datetime, timedelta

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    abort,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.sharing import sharing
from app.extensions import db
from app.models import (
    Child,
    ShareCode,
    AccessRequest,
    SharedAccess,
    RequestStatus
)
from app.utils.decorators import user_required
from app.utils.permissions import is_child_parent


def generate_share_code():
    return "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=6
        )
    )


def validate_share_code(share_code, child_name, now):
    if share_code is None:
        return "Invalid code."

    if share_code.expires_at < now:
        return "Code expired."

    if share_code.child.name != child_name:
        return "Wrong child."

    return None


def can_request_access(existing_access):
    return existing_access is None


@sharing.route(
    "/children/<int:child_id>/generate-code",
    methods=["GET", "POST"]
)
@login_required
@user_required
def generate_code(child_id):
    child = Child.query.get_or_404(child_id)

    if child.parent_id != current_user.id:
        abort(403)

    code = None

    if request.method == "POST":
        ShareCode.query.filter_by(
            child_id=child.id,
            active=True
        ).update(
            {
                "active": False
            }
        )

        code = generate_share_code()

        share_code = ShareCode(
            code=code,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(minutes=10),
            child=child
        )

        db.session.add(share_code)
        db.session.commit()

    return render_template(
        "sharing/generate_code.html",
        child=child,
        code=code
    )


@sharing.route(
    "/request-access",
    methods=["GET", "POST"]
)
@login_required
@user_required
def request_access():
    if request.method == "POST":
        child_name = request.form["child_name"]
        code = request.form["code"]

        share_code = ShareCode.query.filter_by(
            code=code,
            active=True,
            used=False
        ).first()

        validation_error = validate_share_code(
            share_code,
            child_name,
            datetime.now()
        )

        if validation_error:
            flash(
                validation_error,
                "danger"
            )

            return redirect(
                url_for("sharing.request_access")
            )

        if is_child_parent(
            share_code.child,
            current_user
        ):
            flash(
                "You cannot request access to your own child.",
                "danger"
            )

            return redirect(
                url_for("sharing.request_access")
            )

        existing = SharedAccess.query.filter_by(
            user_id=current_user.id,
            child_id=share_code.child.id
        ).first()

        if not can_request_access(existing):
            flash(
                "Already connected.",
                "info"
            )

            return redirect(
                url_for("sharing.request_access")
            )

        access_request = AccessRequest(
            requester_id=current_user.id,
            child_id=share_code.child.id
        )

        share_code.used = True

        db.session.add(access_request)
        db.session.commit()

        flash(
            "Access request sent — waiting for approval.",
            "success"
        )

        return redirect(
            url_for("children.my_children")
        )

    return render_template(
        "sharing/request_access.html"
    )


@sharing.route(
    "/access-requests"
)
@login_required
@user_required
def access_requests():
    requests = AccessRequest.query.join(
        Child
    ).filter(
        Child.parent_id == current_user.id,
        AccessRequest.status == RequestStatus.PENDING
    ).all()

    return render_template(
        "sharing/requests.html",
        requests=requests
    )


@sharing.route(
    "/approve/<int:request_id>",
    methods=["POST"]
)
@login_required
@user_required
def approve_request(request_id):
    access_request = AccessRequest.query.get_or_404(
        request_id
    )

    child = access_request.child

    if child.parent_id != current_user.id:
        abort(403)

    access_request.status = RequestStatus.APPROVED

    shared_access = SharedAccess(
        user=access_request.requester,
        child=child
    )

    db.session.add(shared_access)
    db.session.commit()

    return redirect(
        url_for(
            "sharing.manage_sharing",
            child_id=child.id
        )
    )


@sharing.route(
    "/reject/<int:request_id>",
    methods=["POST"]
)
@login_required
@user_required
def reject_request(request_id):
    access_request = AccessRequest.query.get_or_404(
        request_id
    )

    child = access_request.child

    if child.parent_id != current_user.id:
        abort(403)

    access_request.status = RequestStatus.REJECTED

    db.session.commit()

    return redirect(
        url_for(
            "sharing.manage_sharing",
            child_id=child.id
        )
    )


@sharing.route(
    "/children/<int:child_id>/sharing"
)
@login_required
@user_required
def manage_sharing(child_id):
    child = Child.query.get_or_404(child_id)

    if child.parent_id != current_user.id:
        abort(403)

    shared_accesses = SharedAccess.query.filter_by(
        child_id=child.id
    ).all()

    pending_requests = AccessRequest.query.filter_by(
        child_id=child.id,
        status=RequestStatus.PENDING
    ).all()

    return render_template(
        "sharing/manage.html",
        child=child,
        shared_accesses=shared_accesses,
        pending_requests=pending_requests
    )


@sharing.route(
    "/remove-access/<int:access_id>",
    methods=["POST"]
)
@login_required
@user_required
def remove_access(access_id):
    access = SharedAccess.query.get_or_404(access_id)

    child = access.child

    if child.parent_id != current_user.id:
        abort(403)

    db.session.delete(access)
    db.session.commit()

    return redirect(
        url_for(
            "sharing.manage_sharing",
            child_id=child.id
        )
    )