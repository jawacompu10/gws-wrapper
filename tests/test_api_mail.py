from fastapi.testclient import TestClient
from gws_wrapper.api.main import app
import pytest

client = TestClient(app)

def test_get_mail_list(mocker):
    # Mocking the adapter function which the route calls
    mock_list = mocker.patch("gws_wrapper.adapters.gmail.list_messages")
    mock_list.return_value = []
    
    response = client.get("/mail?count=5")
    assert response.status_code == 200
    assert response.json() == []
    mock_list.assert_called_once_with(5)

def test_get_mail_search(mocker):
    mock_search = mocker.patch("gws_wrapper.adapters.gmail.search_messages")
    mock_search.return_value = []
    
    response = client.get("/mail?q=test&count=5")
    assert response.status_code == 200
    assert response.json() == []
    mock_search.assert_called_once_with("test", 5)

def test_get_mail_body(mocker):
    mock_body = mocker.patch("gws_wrapper.adapters.gmail.get_message_body")
    mock_body.return_value = "This is a test body"
    
    response = client.get("/mail/msg123")
    assert response.status_code == 200
    assert response.json() == {"id": "msg123", "body": "This is a test body"}
    mock_body.assert_called_once_with("msg123")

def test_trash_messages(mocker):
    mock_trash = mocker.patch("gws_wrapper.adapters.gmail.trash_message")
    
    response = client.post("/mail/trash", json={"message_ids": ["id1", "id2"]})
    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert mock_trash.call_count == 2

def test_archive_messages(mocker):
    mock_archive = mocker.patch("gws_wrapper.adapters.gmail.archive_message")
    
    response = client.post("/mail/archive", json={"message_ids": ["id1", "id2"]})
    assert response.status_code == 200
    assert response.json()["count"] == 2
    assert mock_archive.call_count == 2

