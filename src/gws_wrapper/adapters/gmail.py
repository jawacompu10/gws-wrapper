from typing import List, Dict, Any
from gws_wrapper.adapters.cli import run_gws_command

def get_message(message_id: str, format: str = "metadata") -> Dict[str, Any]:
    """
    Fetch details for a specific message.
    """
    return run_gws_command(
        service="gmail",
        resource="users",
        sub_resource="messages",
        method="get",
        params={
            "userId": "me",
            "id": message_id,
            "format": format
        }
    )

def list_messages(count: int) -> List[Dict[str, Any]]:
    """
    Fetch a list of messages with their metadata.
    """
    # 1. Get the list of IDs
    list_response = run_gws_command(
        service="gmail",
        resource="users",
        sub_resource="messages",
        method="list",
        params={
            "userId": "me",
            "maxResults": count
        }
    )
    
    messages = list_response.get("messages", [])
    detailed_messages = []
    
    # 2. Fetch metadata for each message
    for msg in messages:
        msg_id = msg["id"]
        details = get_message(msg_id)
        
        # Extract headers for easier use
        headers = details.get("payload", {}).get("headers", [])
        extracted = {
            "id": msg_id,
            "snippet": details.get("snippet"),
        }
        
        for header in headers:
            name = header.get("name")
            if name in ["From", "To", "Subject", "Date"]:
                extracted[name.lower()] = header.get("value")
                
        detailed_messages.append(extracted)
        
    return detailed_messages
