from unittest.mock import Mock, patch

from werkzeug.security import generate_password_hash

from app.auth.routes import is_valid_password


def test_is_valid_password_returns_true_for_correct_password():
    user = Mock()
    user.password = generate_password_hash("password123")

    assert is_valid_password(user, "password123") is True


def test_is_valid_password_returns_false_for_wrong_password():
    user = Mock()
    user.password = generate_password_hash("password123")

    assert is_valid_password(user, "wrongpassword") is False


def test_is_valid_password_returns_false_when_user_does_not_exist():
    assert is_valid_password(None, "password123") is False