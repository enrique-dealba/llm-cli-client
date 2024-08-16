import json

import click
import requests

from config import settings


@click.group()
def cli():
    """CLI client for LLM Server."""
    pass


@cli.command()
def health():
    """Checks the health of the LLM server."""
    try:
        response = requests.get(f"{settings.LLM_SERVER_URL}/health")
        response.raise_for_status()
        click.echo(response.json())
    except requests.RequestException as e:
        click.echo(f"Error checking server health: {e}", err=True)
        exit(1)


@cli.command()
@click.option(
    "--text", prompt="Enter text to generate from", help="Input text for generation"
)
def generate(text):
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
)
def process_skill(text):
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
