from unittest.mock import Mock, patch

import pytest
from werkzeug.exceptions import HTTPException

from app.utils.decorators import user_required, admin_required


# =========================
# user_required
# =========================

def test_user_required_rejects_unauthenticated_user():
    view = Mock()

    with patch("app.utils.decorators.current_user") as mock_user:
        mock_user.is_authenticated = False

        wrapped = user_required(view)

        with pytest.raises(HTTPException) as exception:
            wrapped()

        assert exception.value.code == 401

    view.assert_not_called()


def test_user_required_rejects_admin_user():
    view = Mock()

    with patch("app.utils.decorators.current_user") as mock_user:
        mock_user.is_authenticated = True
        mock_user.is_admin = True

        wrapped = user_required(view)

        with pytest.raises(HTTPException) as exception:
            wrapped()

        assert exception.value.code == 403

    view.assert_not_called()


def test_user_required_allows_regular_user():
    view = Mock(return_value="success")

    with patch("app.utils.decorators.current_user") as mock_user:
        mock_user.is_authenticated = True
        mock_user.is_admin = False

        wrapped = user_required(view)

        result = wrapped()

        assert result == "success"

    view.assert_called_once_with()


# =========================
# admin_required
# =========================

def test_admin_required_rejects_unauthenticated_user():
    view = Mock()

    with patch("app.utils.decorators.current_user") as mock_user:
        mock_user.is_authenticated = False

        wrapped = admin_required(view)

        with pytest.raises(HTTPException) as exception:
            wrapped()

        assert exception.value.code == 401

    view.assert_not_called()


def test_admin_required_rejects_regular_user():
    view = Mock()

    with patch("app.utils.decorators.current_user") as mock_user:
        mock_user.is_authenticated = True
        mock_user.is_admin = False

        wrapped = admin_required(view)

        with pytest.raises(HTTPException) as exception:
            wrapped()

        assert exception.value.code == 403

    view.assert_not_called()


def test_admin_required_allows_admin_user():
    view = Mock(return_value="success")

    with patch("app.utils.decorators.current_user") as mock_user:
        mock_user.is_authenticated = True
        mock_user.is_admin = True

        wrapped = admin_required(view)

        result = wrapped()

        assert result == "success"

    view.assert_called_once_with()
