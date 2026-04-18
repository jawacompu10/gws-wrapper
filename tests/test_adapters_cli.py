import subprocess
import pytest
import json
from gws_wrapper.adapters.cli import run_gws_command


def test_run_gws_command_success(mocker):
    # Mock subprocess.run
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.stdout = json.dumps({"status": "ok"})
    mock_run.return_value.returncode = 0

    result = run_gws_command("gmail", "users", "list")

    assert result == {"status": "ok"}
    mock_run.assert_called_once()
    # Check if 'gws' and 'json' format are in the command
    args = mock_run.call_args[0][0]
    assert "gws" in args
    assert "gmail" in args
    assert "--format" in args
    assert "json" in args


def test_run_gws_command_error(mocker):
    # Mock subprocess.run to raise CalledProcessError
    mock_run = mocker.patch("subprocess.run")
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="gws ...", stderr="API Error"
    )

    with pytest.raises(RuntimeError, match="gws CLI failed: API Error"):
        run_gws_command("gmail", "users", "list")


def test_run_gws_command_invalid_json(mocker):
    mock_run = mocker.patch("subprocess.run")
    mock_run.return_value.stdout = "Invalid JSON"

    with pytest.raises(RuntimeError, match="Invalid JSON response from gws CLI"):
        run_gws_command("gmail", "users", "list")
