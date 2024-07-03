from click.testing import CliRunner
from unittest.mock import patch
import resume_assist
import resume_assist.service
import resume_assist.service.cli


@patch("resume_assist.service.cli.create_fastapi_application")
@patch("resume_assist.service.cli.uvicorn.run")
def test_start_command(mock_uvicorn_run, mock_create_fastapi_application):
    runner = CliRunner()
    result = runner.invoke(
        resume_assist.service.cli.start, ["--host", "127.0.0.1", "--port", "8000"]
    )

    assert result.exit_code == 0
    mock_create_fastapi_application.assert_called_once()
    mock_uvicorn_run.assert_called_once_with(
        mock_create_fastapi_application.return_value, host="127.0.0.1", port=8000
    )


@patch("resume_assist.service.cli.create_fastapi_application")
@patch("resume_assist.service.cli.uvicorn.run")
def test_start_command_defaults(mock_uvicorn_run, mock_create_fastapi_application):
    runner = CliRunner()
    result = runner.invoke(resume_assist.service.cli.start)

    assert result.exit_code == 0
    mock_create_fastapi_application.assert_called_once()
    mock_uvicorn_run.assert_called_once_with(
        mock_create_fastapi_application.return_value, host="0.0.0.0", port=10010
    )
