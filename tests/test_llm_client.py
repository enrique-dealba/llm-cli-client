import json
from unittest.mock import mock_open, patch

import requests
from click.testing import CliRunner

from src.llm_client.cli import cli

runner = CliRunner()


def test_health_command():
    """Tests health command."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "healthy"}
        mock_get.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["health"])
        assert result.exit_code == 0
        assert "healthy" in result.output


def test_generate_command_default():
    """Tests generate command with default output."""
    mock_response = {
        "messages": [
            {"content": "User prompt", "user": True},
            {"content": "Howdy, world!", "user": False},
        ]
    }
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["generate"], input="Test prompt\n")

    assert result.exit_code == 0
    assert "Howdy, world!" in result.output.strip()
    assert "messages" not in result.output


def test_generate_command_verbose():
    """Tests generate command with verbose output."""
    mock_response = {
        "messages": [
            {"content": "User prompt", "user": True},
            {"content": "Howdy, world!", "user": False},
        ],
        "extra": "data",
    }
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["generate", "--verbose"], input="Test prompt\n")

    assert result.exit_code == 0
    assert "Howdy, world!" in result.output
    assert "extra" in result.output

    json_start = result.output.find("{")
    json_end = result.output.rfind("}") + 1
    json_str = result.output[json_start:json_end]

    output_json = json.loads(json_str)
    assert output_json == mock_response


def test_generate_command_error():
    """Tests generate command with error response."""
    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.RequestException("API error")
        result = runner.invoke(cli, ["generate"], input="Test prompt\n")

    assert result.exit_code == 1
    assert "Error generating text: API error" in result.output


def test_process_skill_command_default():
    """Tests process_skill command with default output."""
    mock_response = {
        "messages": [
            {"content": "User skill", "user": True},
            {"content": "Skill processed!", "user": False},
        ]
    }
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["process-skill"], input="Test skill\n")

    assert result.exit_code == 0
    assert "Skill processed!" in result.output.strip()
    assert "messages" not in result.output  # Ensure full JSON is not in output


def test_process_skill_command_verbose():
    """Tests process_skill command with verbose output."""
    mock_response = {
        "messages": [
            {"content": "User skill", "user": True},
            {"content": "Skill processed!", "user": False},
        ],
        "details": "Extra info!",
    }
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(
            cli, ["process-skill", "--verbose"], input="Test skill\n"
        )

    assert result.exit_code == 0
    assert "Skill processed!" in result.output
    assert "Extra info!" in result.output
    # Parse the JSON output, ignoring the prompt
    output_json = json.loads(result.output.split("\n", 1)[1])
    assert output_json == mock_response


def test_process_skill_command_error():
    """Tests process_skill command with error response."""
    with patch("requests.post") as mock_post:
        mock_post.side_effect = requests.RequestException("API error")
        result = runner.invoke(cli, ["process-skill"], input="Test skill\n")

    assert result.exit_code == 1
    assert "Error processing skill: API error" in result.output


def test_get_url_command():
    """Tests get_url command for default URL."""
    result = runner.invoke(cli, ["get-url"])
    
    assert result.exit_code == 0
    assert "http://localhost:8888" in result.output


def test_set_url_command():
    """Tests set_url command."""
    m = mock_open()
    with patch("src.llm_client.config.open", m):
        with patch("json.dump") as mock_json_dump:
            result = runner.invoke(cli, ["set-url", "http://new-llm-url:8888"])
            assert result.exit_code == 0
            assert "LLM server URL set to: http://new-llm-url:8888" in result.output
            mock_json_dump.assert_called_once()

            # Check that the correct URL was saved
            args, _ = mock_json_dump.call_args
            assert args[0]["LLM_SERVER_URL"] == "http://new-llm-url:8888"


def test_url_persistence():
    """Tests if set_url changes are reflected in subsequent get_url calls."""
    m = mock_open()
    with patch("src.llm_client.config.open", m):
        with patch("json.dump") as _, patch(
            "src.llm_client.config.load_config"
        ) as mock_load_config:
            # Sets the URL
            runner.invoke(cli, ["set-url", "http://new-url:8080"])
            mock_load_config.return_value = {"LLM_SERVER_URL": "http://new-url:8080"}

            # Get new URL
            result = runner.invoke(cli, ["get-url"])
            assert result.exit_code == 0
            assert "http://new-url:8080" in result.output
