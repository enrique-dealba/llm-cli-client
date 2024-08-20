from unittest.mock import mock_open, patch

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
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"text": "Howdy, world!"}
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["generate"], input="Test prompt")
    assert result.exit_code == 0
    assert "Howdy, world!" in result.output
    assert '{"text":' not in result.output  # Ensure full JSON is not in output

def test_generate_command_verbose():
    """Tests generate command with verbose output."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"text": "Howdy, world!", "extra": "data"}
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["generate", "--verbose"], input="Test prompt")
    assert result.exit_code == 0
    assert '"text": "Howdy, world!"' in result.output
    assert '"extra": "data"' in result.output

def test_process_skill_command_default():
    """Tests process_skill command with default output."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"text": "Skill processed!"}
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["process-skill"], input="Test skill")
    assert result.exit_code == 0
    assert "Skill processed!" in result.output
    assert '{"text":' not in result.output  # Ensure full JSON is not in output

def test_process_skill_command_verbose():
    """Tests process_skill command with verbose output."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"text": "Skill processed!", "details": "Extra info!"}
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["process-skill", "--verbose"], input="Test skill")
    assert result.exit_code == 0
    assert '"text": "Skill processed!"' in result.output
    assert '"details": "Extra info!"' in result.output


def test_get_url_command():
    """Tests get_url command."""
    with patch("src.llm_client.config.Settings") as MockSettings:
        # Create a mock Settings instance
        mock_settings = MockSettings.return_value

        # Set the LLM_SERVER_URL attribute on the mock
        mock_settings.LLM_SERVER_URL = "http://test-url:9999"

        # Patch the settings in the config module
        with patch("src.llm_client.config.settings", mock_settings):
            result = runner.invoke(cli, ["get-url"])

            assert result.exit_code == 0
            assert "http://test-url:9999" in result.output


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
        with patch("json.dump") as mock_json_dump, patch(
            "src.llm_client.config.load_config"
        ) as mock_load_config:
            # Sets the URL
            runner.invoke(cli, ["set-url", "http://new-url:8080"])
            mock_load_config.return_value = {"LLM_SERVER_URL": "http://new-url:8080"}

            # Get new URL
            result = runner.invoke(cli, ["get-url"])
            assert result.exit_code == 0
            assert "http://new-url:8080" in result.output
