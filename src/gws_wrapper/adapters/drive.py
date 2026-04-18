from typing import List
from gws_wrapper.adapters.cli import run_gws_command
from gws_wrapper.models.drive import DriveFile

def search_files(query: str, limit: int = 10) -> List[DriveFile]:
    """
    Search for files in Google Drive by name.
    """
    # Drive API search query syntax: name contains 'query' and trashed = false
    q = f"name contains '{query}' and trashed = false"
    
    response = run_gws_command(
        service="drive",
        resource="files",
        method="list",
        params={
            "q": q,
            "pageSize": limit,
            "fields": "files(id, name, mimeType, kind, webViewLink)"
        }
    )
    
    files = response.get("files", [])
    return [
        DriveFile(
            id=f["id"],
            name=f["name"],
            mime_type=f["mimeType"],
            kind=f["kind"],
            web_view_link=f.get("webViewLink")
        ) for f in files
    ]
