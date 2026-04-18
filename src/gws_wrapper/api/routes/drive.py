from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from typing import List
import os
import tempfile
from gws_wrapper.adapters import drive
from gws_wrapper.models.drive import DriveFile

router = APIRouter(prefix="/drive", tags=["drive"])

@router.get("", response_model=List[DriveFile])
async def search_files(q: str, limit: int = 10):
    """
    Search for files in Google Drive.
    """
    try:
        return drive.search_files(q, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{file_id}")
async def download_file(file_id: str):
    """
    Download a file from Google Drive.
    """
    try:
        file_info = drive.get_file_info(file_id)
        # Create a temporary file to hold the download
        # Note: In a production environment, we should ensure the tmp file is cleaned up after the response is sent.
        # FastAPI's FileResponse handles the file opening, but we need to be careful with cleanup.
        # For now, we use a temp file in a temp directory.
        tmp_dir = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_dir, file_info.name)
        
        drive.download_file(file_id, tmp_path)
        
        return FileResponse(
            path=tmp_path,
            filename=file_info.name,
            media_type="application/octet-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
