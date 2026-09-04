from datetime import datetime, timedelta
from unittest.mock import Mock

from app.sharing.routes import (
    generate_share_code,
    validate_share_code,
    can_request_access
)


def test_generate_share_code_has_six_characters():
    code = generate_share_code()

    assert len(code) == 6


def test_generate_share_code_contains_only_uppercase_letters_and_digits():
    code = generate_share_code()

    allowed_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    assert all(
        character in allowed_characters
        for character in code
    )


def test_generate_share_code_generates_different_codes():
    code1 = generate_share_code()
    code2 = generate_share_code()

    assert code1 != code2


def test_validate_share_code_returns_error_for_missing_code():
    result = validate_share_code(
        share_code=None,
        child_name="Emma",
        now=datetime.now()
    )

    assert result == "Invalid code."


def test_validate_share_code_returns_error_for_expired_code():
    share_code = Mock()

    share_code.expires_at = (
        datetime.now() - timedelta(minutes=1)
    )

    result = validate_share_code(
        share_code=share_code,
        child_name="Emma",
        now=datetime.now()
    )

    assert result == "Code expired."


def test_validate_share_code_returns_error_for_wrong_child():
    share_code = Mock()

    share_code.expires_at = (
        datetime.now() + timedelta(minutes=10)
    )

    share_code.child.name = "Anna"

    result = validate_share_code(
        share_code=share_code,
        child_name="Emma",
        now=datetime.now()
    )

    assert result == "Wrong child."


def test_validate_share_code_returns_none_for_valid_code():
    share_code = Mock()

    share_code.expires_at = (
        datetime.now() + timedelta(minutes=10)
    )

    share_code.child.name = "Emma"

    result = validate_share_code(
        share_code=share_code,
        child_name="Emma",
        now=datetime.now()
    )

    assert result is None


def test_can_request_access_when_user_has_no_existing_access():
    result = can_request_access(None)

    assert result is True


def test_cannot_request_access_when_user_already_has_access():
    existing_access = Mock()

    result = can_request_access(existing_access)

    assert result is False