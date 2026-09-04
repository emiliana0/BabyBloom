from unittest.mock import Mock

from app.notes.routes import apply_note_filters
from app.models import NoteCategory


def create_mock_query():
    query = Mock()

    query.filter.return_value = query
    query.filter_by.return_value = query
    query.order_by.return_value = query

    return query


def test_apply_note_filters_searches_title_and_content():
    query = create_mock_query()

    apply_note_filters(
        query=query,
        search="birthday"
    )

    query.filter.assert_called_once()

    query.filter_by.assert_not_called()


def test_apply_note_filters_filters_by_category():
    query = create_mock_query()

    apply_note_filters(
        query=query,
        category="HEALTH"
    )

    query.filter_by.assert_called_once_with(
        category=NoteCategory.HEALTH
    )


def test_apply_note_filters_filters_by_from_date():
    query = create_mock_query()

    apply_note_filters(
        query=query,
        from_date="2026-08-01"
    )

    query.filter.assert_called_once()


def test_apply_note_filters_filters_by_to_date():
    query = create_mock_query()

    apply_note_filters(
        query=query,
        to_date="2026-08-31"
    )

    query.filter.assert_called_once()


def test_apply_note_filters_sorts_newest_first():
    query = create_mock_query()

    apply_note_filters(
        query=query,
        sort="newest"
    )

    query.order_by.assert_called_once()


def test_apply_note_filters_sorts_oldest_first():
    query = create_mock_query()

    apply_note_filters(
        query=query,
        sort="oldest"
    )

    query.order_by.assert_called_once()


def test_apply_note_filters_can_apply_multiple_filters():
    query = create_mock_query()

    apply_note_filters(
        query=query,
        search="doctor",
        category="HEALTH",
        from_date="2026-08-01",
        to_date="2026-08-31",
        sort="oldest"
    )

    query.filter.assert_called()
    query.filter_by.assert_called_once_with(
        category=NoteCategory.HEALTH
    )
    query.order_by.assert_called_once()
