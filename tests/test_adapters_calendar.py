import pytest
from gws_wrapper.adapters import calendar


def test_list_events_success(mocker):
    mock_run = mocker.patch("gws_wrapper.adapters.calendar.run_gws_command")
    mock_run.return_value = {
        "items": [
            {
                "id": "evt1",
                "summary": "Meeting",
                "start": {"dateTime": "2026-04-18T10:00:00Z"},
                "end": {"dateTime": "2026-04-18T11:00:00Z"},
            }
        ]
    }

    events = calendar.list_events(days=1)
    assert len(events) == 1
    assert events[0].summary == "Meeting"
    assert events[0].id == "evt1"


def test_create_event_success(mocker):
    mock_run = mocker.patch("gws_wrapper.adapters.calendar.run_gws_command")
    mock_run.return_value = {
        "id": "new_evt",
        "summary": "Lunch",
        "start": {"dateTime": "2026-04-18T12:00:00Z"},
        "end": {"dateTime": "2026-04-18T13:00:00Z"},
    }

    event = calendar.create_event(
        summary="Lunch",
        start_time="2026-04-18T12:00:00Z",
        end_time="2026-04-18T13:00:00Z",
    )

    assert event.id == "new_evt"
    assert event.summary == "Lunch"
    mock_run.assert_called_once()

    # Check if body was passed correctly
    _, kwargs = mock_run.call_args
    assert kwargs["body"]["summary"] == "Lunch"
    assert kwargs["body"]["start"]["dateTime"] == "2026-04-18T12:00:00Z"

@pytest.mark.parametrize("input_str", [
    "tomorrow 10am",
    "Tuesday 3pm",
    "today 5pm",
    "in 2 hours",
])
def test_parse_start_time_success(input_str):
    from datetime import datetime
    dt = calendar.parse_start_time(input_str)
    assert isinstance(dt, datetime)
    assert dt.tzinfo is not None
    # With PREFER_DATES_FROM: future, it should be in the future
    assert dt > datetime.now(dt.tzinfo)

def test_parse_start_time_invalid():
    with pytest.raises(ValueError, match="Could not parse date string"):
        calendar.parse_start_time("not a date")

def test_parse_start_time_future_preference():
    # If today is Monday, 'Monday' should parse to next Monday (future), not today or past.
    # We can't easily mock the internal clock of dateparser without complex setup,
    # but we can verify it returns something in the future.
    from datetime import datetime
    dt = calendar.parse_start_time("Monday")
    assert dt > datetime.now(dt.tzinfo)
