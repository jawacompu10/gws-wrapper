import pytest
from gws_wrapper.adapters import drive
from gws_wrapper.models.drive import DriveFile

def test_search_files_success(mocker):
    mock_run = mocker.patch("gws_wrapper.adapters.drive.run_gws_command")
    mock_run.return_value = {
        "files": [
            {
                "id": "file123",
                "name": "Project Proposal.pdf",
                "mimeType": "application/pdf",
                "kind": "drive#file",
                "webViewLink": "https://drive.google.com/file/d/file123/view"
            }
        ]
    }

    files = drive.search_files(query="Project", limit=1)
    
    assert len(files) == 1
    assert isinstance(files[0], DriveFile)
    assert files[0].name == "Project Proposal.pdf"
    assert files[0].id == "file123"
    
    # Verify the query was constructed correctly
    _, kwargs = mock_run.call_args
    assert "name contains 'Project'" in kwargs["params"]["q"]
    assert "webViewLink" in kwargs["params"]["fields"]
