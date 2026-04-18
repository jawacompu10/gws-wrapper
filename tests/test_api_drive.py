from fastapi.testclient import TestClient
from gws_wrapper.api.main import app
import pytest

client = TestClient(app)

def test_drive_search(mocker):
    """
    Test the drive search endpoint.
    """
    mock_search = mocker.patch("gws_wrapper.adapters.drive.search_files")
    mock_search.return_value = []
    
    response = client.get("/drive?q=test")
    assert response.status_code == 200
    mock_search.assert_called_once_with("test", 10)

def test_drive_download(mocker):
    """
    Test the drive download endpoint.
    """
    mock_get_info = mocker.patch("gws_wrapper.adapters.drive.get_file_info")
    mock_download = mocker.patch("gws_wrapper.adapters.drive.download_file")
    
    from gws_wrapper.models.drive import DriveFile
    mock_get_info.return_value = DriveFile(
        id="file1",
        name="test.txt",
        mime_type="text/plain",
        kind="drive#file"
    )
    
    # Create a dummy file when download_file is called
    def side_effect(file_id, output_path):
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write("test content")
    
    mock_download.side_effect = side_effect
    
    response = client.get("/drive/file1")
    assert response.status_code == 200
    assert response.content == b"test content"
    mock_get_info.assert_called_once_with("file1")
    assert mock_download.called
