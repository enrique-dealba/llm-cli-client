import json

import click
import requests

BASE_URL = "http://localhost:8888"


@click.group()
def cli():
    """CLI client for LLM Server."""
    pass


@cli.command()
def health():
    """Check the health of the LLM server."""
    response = requests.get(f"{BASE_URL}/health")
    click.echo(response.json())


@cli.command()
@click.option(
    "--text", prompt="Enter text to generate from", help="Input text for generation"
)
def generate(text):
    """Generate text using the LLM."""
    response = requests.post(f"{BASE_URL}/generate", json={"text": text})
    click.echo(json.dumps(response.json(), indent=2))


@cli.command("process-skill")
@click.option(
    "--text", prompt="Enter skill to process", help="Input text for skill processing"
)
def process_skill(text):
    """Process a skill using the LLM"""
    response = requests.post(f"{BASE_URL}/process_skill", json={"text": text})
    click.echo(json.dumps(response.json(), indent=2))


# Alias for process-skill
cli.add_command(process_skill, name="process_skill")


if __name__ == "__main__":
    cli()
