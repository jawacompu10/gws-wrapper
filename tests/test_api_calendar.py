from fastapi.testclient import TestClient
from gws_wrapper.api.main import app
import pytest

client = TestClient(app)

def test_get_calendar_events(mocker):
    mock_list = mocker.patch("gws_wrapper.adapters.calendar.list_events")
    mock_list.return_value = []
    
    response = client.get("/calendar?days=7")
    assert response.status_code == 200
    mock_list.assert_called_once_with(7)
