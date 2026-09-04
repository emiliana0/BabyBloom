from unittest.mock import Mock

from app.gallery.routes import (
    allowed_file,
    apply_photo_filters
)


def create_mock_query():
    query = Mock()

    query.filter.return_value = query
    query.filter_by.return_value = query
    query.order_by.return_value = query

    return query


# --------------------------------------------------
# allowed_file()
# --------------------------------------------------


def test_allowed_file_accepts_png():
    assert allowed_file("photo.png") is True


def test_allowed_file_accepts_jpg():
    assert allowed_file("photo.jpg") is True


def test_allowed_file_accepts_jpeg():
    assert allowed_file("photo.jpeg") is True


def test_allowed_file_is_case_insensitive():
    assert allowed_file("photo.PNG") is True
    assert allowed_file("photo.JPG") is True
    assert allowed_file("photo.JPEG") is True


def test_allowed_file_rejects_invalid_extension():
    assert allowed_file("photo.gif") is False


def test_allowed_file_rejects_file_without_extension():
    assert allowed_file("photo") is False


def test_allowed_file_rejects_empty_filename():
    assert allowed_file("") is False


# --------------------------------------------------
# apply_photo_filters()
# --------------------------------------------------


def test_apply_photo_filters_searches_title_and_description():

    query = create_mock_query()

    apply_photo_filters(
        query=query,
        search="birthday"
    )

    query.filter.assert_called_once()


def test_apply_photo_filters_filters_from_date():

    query = create_mock_query()

    apply_photo_filters(
        query=query,
        from_date="2026-08-01"
    )

    query.filter.assert_called_once()


def test_apply_photo_filters_filters_to_date():

    query = create_mock_query()

    apply_photo_filters(
        query=query,
        to_date="2026-08-31"
    )

    query.filter.assert_called_once()


def test_apply_photo_filters_sorts_newest_first():

    query = create_mock_query()

    apply_photo_filters(
        query=query,
        sort="newest"
    )

    query.order_by.assert_called_once()


def test_apply_photo_filters_sorts_oldest_first():

    query = create_mock_query()

    apply_photo_filters(
        query=query,
        sort="oldest"
    )

    query.order_by.assert_called_once()


def test_apply_photo_filters_can_apply_multiple_filters():

    query = create_mock_query()

    apply_photo_filters(
        query=query,
        search="birthday",
        from_date="2026-08-01",
        to_date="2026-08-31",
        sort="oldest"
    )

    assert query.filter.call_count == 3

    query.order_by.assert_called_once()