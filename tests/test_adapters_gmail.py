from gws_wrapper.adapters import gmail
from gws_wrapper.models.gmail import GmailMessage


def test_list_messages_success(mocker):
    # Mock run_gws_command
    mock_run = mocker.patch("gws_wrapper.adapters.gmail.run_gws_command")

    # First call: list messages
    # Second call: get metadata for msg1
    mock_run.side_effect = [
        {"messages": [{"id": "msg1"}]},  # list call
        {  # get call
            "id": "msg1",
            "snippet": "Hello world",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Subject", "value": "Test Subject"},
                ]
            },
        },
    ]

    messages = gmail.list_messages(count=1)

    assert len(messages) == 1
    assert isinstance(messages[0], GmailMessage)
    assert messages[0].id == "msg1"
    assert messages[0].sender == "sender@example.com"
    assert messages[0].subject == "Test Subject"
    assert messages[0].snippet == "Hello world"

    assert mock_run.call_count == 2


def test_get_message_body_success(mocker):
    import base64

    mock_run = mocker.patch("gws_wrapper.adapters.gmail.run_gws_command")

    # URL-safe base64 of "This is the body"
    encoded_body = base64.urlsafe_b64encode(b"This is the body").decode("utf-8")

    mock_run.return_value = {"id": "msg1", "payload": {"body": {"data": encoded_body}}}

    body = gmail.get_message_body("msg1")
    assert body == "This is the body"
    mock_run.assert_called_once()


def test_delete_message_success(mocker):
    mock_run = mocker.patch("gws_wrapper.adapters.gmail.run_gws_command")
    mock_run.return_value = {}

    gmail.delete_message("msg1")

    mock_run.assert_called_once()
    args = mock_run.call_args[1]
    assert args["method"] == "delete"
    assert args["params"]["id"] == "msg1"


def test_trash_message_success(mocker):
    mock_run = mocker.patch("gws_wrapper.adapters.gmail.run_gws_command")
    mock_run.return_value = {}

    gmail.trash_message("msg1")

    mock_run.assert_called_once()
    args = mock_run.call_args[1]
    assert args["method"] == "trash"
    assert args["params"]["id"] == "msg1"
