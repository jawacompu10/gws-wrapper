from typing import List, Dict, Any
from gws_wrapper.adapters.cli import run_gws_command
from gws_wrapper.models.gmail import GmailMessage

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

def get_message_body(message_id: str) -> str:
    """
    Fetch the full body of a message.
    """
    details = get_message(message_id, format="full")
    payload = details.get("payload", {})
    
    def extract_body(part):
        if part.get("body", {}).get("data"):
            import base64
            data = part["body"]["data"]
            # Gmail uses URL-safe base64
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
        
        if "parts" in part:
            for subpart in part["parts"]:
                body = extract_body(subpart)
                if body:
                    return body
        return ""

    return extract_body(payload) or details.get("snippet", "")

def list_messages(count: int) -> List[GmailMessage]:
    """
    Fetch a list of messages with their metadata as Pydantic models.
    """
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
    
    for msg in messages:
        msg_id = msg["id"]
        details = get_message(msg_id)
        
        headers = details.get("payload", {}).get("headers", [])
        
        # Build the message data
        msg_data = {
            "id": msg_id,
            "thread_id": details.get("threadId"),
            "snippet": details.get("snippet"),
        }
        
        # Map headers to our model fields
        header_map = {
            "From": "sender",
            "Subject": "subject",
            "Date": "date"
        }
        
        for header in headers:
            name = header.get("name")
            if name in header_map:
                msg_data[header_map[name]] = header.get("value")
                
        detailed_messages.append(GmailMessage(**msg_data))
        
    return detailed_messages
