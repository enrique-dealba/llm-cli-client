import json

import click
import requests

from .config import save_config, settings


@click.group()
def cli():
    """CLI client for LLM Server."""
    pass


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
def generate(text: str):
    """Generate general text using the LLM."""
    try:
        response = requests.post(
            f"{settings.LLM_SERVER_URL}/generate", json={"text": text}
        )
        response.raise_for_status()
        click.echo(json.dumps(response.json(), indent=2))
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
def process_skill(text: str):
    """Process a spaceplan skill using the LLM."""
    try:
        response = requests.post(
            f"{settings.LLM_SERVER_URL}/process_skill", json={"text": text}
        )
        response.raise_for_status()
        click.echo(json.dumps(response.json(), indent=2))
    except requests.RequestException as e:
        click.echo(f"Error processing skill: {e}", err=True)
        exit(1)


# Alias for process-skill
cli.add_command(process_skill, name="process_skill")

if __name__ == "__main__":
    cli()
