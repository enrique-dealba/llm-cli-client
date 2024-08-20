import json

import click
import requests

from .config import save_config, settings


@click.group()
def cli():
    """CLI client for LLM Server."""
    pass


def prettify_json(json_str):
    """Convert JSON string to pretty-printed text."""
    parsed = json.loads(json_str)
    return json.dumps(parsed, indent=2)


def extract_last_ai_message(response):
    """Extract content of LLM response."""
    messages = response.get("messages", [])
    ai_messages = [msg for msg in messages if not msg.get("user", True)]
    if ai_messages:
        return ai_messages[-1].get("content", "")
    return ""


@cli.command()
@click.argument("url", type=str)
def set_url(url: str):
    """Sets the LLM server URL."""
    settings.LLM_SERVER_URL = url
    save_config({"LLM_SERVER_URL": url})
    click.echo(f"LLM server URL set to: {url}")


@cli.command()
def get_url():
    """Get current LLM server URL."""
    click.echo(f"{settings.LLM_SERVER_URL}")


@cli.command()
def health():
    """Checks the health of the LLM server."""
    click.echo(f"Checking health for LLM server at: {settings.LLM_SERVER_URL}")
    try:
        response = requests.get(f"{settings.LLM_SERVER_URL}/health")
        response.raise_for_status()
        click.echo(response.json())
    except requests.RequestException as e:
        click.echo(f"Error checking server health: {e}", err=True)
        exit(1)


@cli.command()
@click.option(
    "--text",
    prompt="Enter text to prompt LLM",
    help="Input text for generation",
    type=str,
)
@click.option("--verbose", "-v", is_flag=True, help="Display full JSON response")
def generate(text: str, verbose: bool):
    """Generate general text using the LLM."""
    try:
        response = requests.post(
            f"{settings.LLM_SERVER_URL}/generate", json={"text": text}
        )
        response.raise_for_status()
        data = response.json()

        if verbose:
            click.echo(prettify_json(json.dumps(data)))
        else:
            content = extract_last_ai_message(data)
            click.echo(prettify_json(content))
    except requests.RequestException as e:
        click.echo(f"Error generating text: {e}", err=True)
        exit(1)


@cli.command("process-skill")
@click.option(
    "--text",
    prompt="Enter skill to process",
    help="Input text for spaceplan skill processing",
    type=str,
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Display full JSON response"
)
def process_skill(text: str, verbose: bool):
    """Process a spaceplan skill using the LLM."""
    try:
        response = requests.post(
            f"{settings.LLM_SERVER_URL}/process_skill", json={"text": text}
        )
        response.raise_for_status()
        data = response.json()
        
        if verbose:
            click.echo(json.dumps(data, indent=2))
        else:
            messages = data.get('messages', [])
            ai_messages = [msg for msg in messages if not msg.get('user', True)]
            if ai_messages:
                click.echo(ai_messages[-1].get('content', 'No content found'))
            else:
                click.echo("No AI response found")
    except requests.RequestException as e:
        click.echo(f"Error processing skill: {e}", err=True)
        exit(1)
    except json.JSONDecodeError as e:
        click.echo(f"Error parsing response: {e}", err=True)
        exit(1)


# Alias for process-skill
cli.add_command(process_skill, name="process_skill")

if __name__ == "__main__":
    cli()
