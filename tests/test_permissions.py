from unittest.mock import Mock, patch

from app.utils.permissions import has_child_access


def test_parent_has_child_access():
    child = Mock()
    child.parent_id = 1
    child.id = 10

    user = Mock()
    user.id = 1

    result = has_child_access(child, user)

    assert result is True


@patch("app.utils.permissions.SharedAccess")
def test_shared_user_has_child_access(mock_shared_access):
    child = Mock()
    child.parent_id = 1
    child.id = 10

    user = Mock()
    user.id = 2

    mock_shared_access.query.filter_by.return_value.first.return_value = Mock()

    result = has_child_access(child, user)

    assert result is True

    mock_shared_access.query.filter_by.assert_called_once_with(
        child_id=10,
        user_id=2
    )


@patch("app.utils.permissions.SharedAccess")
def test_user_without_access_cannot_access_child(mock_shared_access):
    child = Mock()
    child.parent_id = 1
    child.id = 10

    user = Mock()
    user.id = 3

    mock_shared_access.query.filter_by.return_value.first.return_value = None

    result = has_child_access(child, user)

    assert result is False

    mock_shared_access.query.filter_by.assert_called_once_with(
        child_id=10,
        user_id=3
    )
