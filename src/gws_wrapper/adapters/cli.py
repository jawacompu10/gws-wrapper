import subprocess
import json
from typing import Any, Dict, List, Optional
from loguru import logger

def run_gws_command(
    service: str,
    resource: str,
    method: str,
    sub_resource: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Execute a gws CLI command and return the parsed JSON output.
    """
    cmd = ["gws", service, resource]
    if sub_resource:
        cmd.append(sub_resource)
    cmd.append(method)

    if params:
        cmd.extend(["--params", json.dumps(params)])
    
    if body:
        cmd.extend(["--json", json.dumps(body)])

    cmd.extend(["--format", "json"])

    logger.debug(f"Executing: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if not result.stdout.strip():
            return {}
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() or e.stdout.strip() or "Unknown error"
        logger.error(f"gws CLI error: {error_msg}")
        raise RuntimeError(f"gws CLI failed: {error_msg}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse gws output: {e}")
        raise RuntimeError("Invalid JSON response from gws CLI")
