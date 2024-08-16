from unittest.mock import patch

from click.testing import CliRunner

from llm_client import cli

runner = CliRunner()


def test_health_command():
    """Tests health command."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "healthy"}
        mock_get.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["health"])
        assert result.exit_code == 0
        assert "healthy" in result.output


def test_generate_command():
    """Tests generate command."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {"generated_text": "Hello, world!"}
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["generate"], input="Test prompt")
        assert result.exit_code == 0
        assert "Hello, world!" in result.output


def test_process_skill_command():
    """Tests process_skill command."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = {
            "processed_skill": "Skill processed"
        }
        mock_post.return_value.raise_for_status.return_value = None
        result = runner.invoke(cli, ["process-skill"], input="Test skill")
        assert result.exit_code == 0
        assert "Skill processed" in result.output
