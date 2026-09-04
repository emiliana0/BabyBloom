from app.models import SharedAccess


def has_child_access(child, user):
    if child.parent_id == user.id:
        return True

    shared = SharedAccess.query.filter_by(
        child_id=child.id,
        user_id=user.id
    ).first()

    return shared is not None

def is_child_parent(child, user):
    return child.parent_id == user.id