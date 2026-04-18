import pytest
from gws_wrapper.adapters import gmail
from gws_wrapper.models.gmail import GmailMessage

def test_list_messages_success(mocker):
    # Mock run_gws_command
    mock_run = mocker.patch("gws_wrapper.adapters.gmail.run_gws_command")
    
    # First call: list messages
    # Second call: get metadata for msg1
    mock_run.side_effect = [
        {"messages": [{"id": "msg1"}]},  # list call
        {                               # get call
            "id": "msg1",
            "snippet": "Hello world",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Subject", "value": "Test Subject"}
                ]
            }
        }
    ]

    messages = gmail.list_messages(count=1)
    
    assert len(messages) == 1
    assert isinstance(messages[0], GmailMessage)
    assert messages[0].id == "msg1"
    assert messages[0].sender == "sender@example.com"
    assert messages[0].subject == "Test Subject"
    assert messages[0].snippet == "Hello world"
    
    assert mock_run.call_count == 2
