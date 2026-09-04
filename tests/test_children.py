from unittest.mock import Mock

from app.children.routes import is_child_parent


def test_is_child_parent_returns_true_for_parent():
    child = Mock()
    child.parent_id = 1

    user = Mock()
    user.id = 1

    assert is_child_parent(child, user) is True


def test_is_child_parent_returns_false_for_other_user():
    child = Mock()
    child.parent_id = 1

    user = Mock()
    user.id = 2

    assert is_child_parent(child, user) is False
