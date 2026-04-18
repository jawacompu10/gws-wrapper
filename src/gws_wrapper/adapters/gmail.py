from gws_wrapper.adapters.cli import run_gws_command

def list_messages(count: int):
    """
    Fetch the list of messages from Gmail.
    """
    params = {
        "userId": "me",
        "maxResults": count
    }
    return run_gws_command(
        service="gmail",
        resource="users",
        sub_resource="messages",
        method="list",
        params=params
    )
