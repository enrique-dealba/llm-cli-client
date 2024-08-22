import json
import sys

import click
import requests

from .config import save_config, settings


def debug_print(message):
    print(f"DEBUG: {message}", file=sys.stderr)


@click.group()
def cli():
    """CLI client for LLM Server."""
    debug_print("Entering cli() function")
    debug_print(f"Registered commands: {list(cli.commands.keys())}")
    # pass


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


def process_default_response(data):
    """Process the default response format."""
    if isinstance(data, dict):
        return data.get("text", json.dumps(data, indent=2))
    return json.dumps(data, indent=2)


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
@click.option("--version3", "-v3", is_flag=True, help="Use v0.0.3 output format")
def generate(text: str, verbose: bool, version3: bool):
    """Generate general text using the LLM."""
    try:
        response = requests.post(
            f"{settings.LLM_SERVER_URL}/generate", json={"text": text}
        )
        response.raise_for_status()
        data = response.json()

        if verbose:
            click.echo(json.dumps(data, indent=2))
        elif version3:
            content = extract_last_ai_message(data)
            click.echo(content)
        else:
            click.echo(process_default_response(data))
    except requests.RequestException as e:
        click.echo(f"Error generating text: {e}", err=True)
        exit(1)
    except json.JSONDecodeError as e:
        click.echo(f"Error parsing response: {e}", err=True)
        exit(1)


@cli.command("process-skill")
@click.option(
    "--text",
    prompt="Enter skill to process",
    help="Input text for spaceplan skill processing",
    type=str,
)
@click.option("--verbose", "-v", is_flag=True, help="Display full JSON response")
@click.option("--version3", "-v3", is_flag=True, help="Use v0.0.3 output format")
def process_skill(text: str, verbose: bool, version3: bool):
    """Process a spaceplan skill using the LLM."""
    print("DEBUG: Entering process_skill function")
    try:
        print(f"DEBUG: Sending request to {settings.LLM_SERVER_URL}/process_skill")
        response = requests.post(
            f"{settings.LLM_SERVER_URL}/process_skill", json={"text": text}
        )
        response.raise_for_status()
        print(f"DEBUG: Received response with status code {response.status_code}")
        data = response.json()
        print(f"DEBUG: Parsed JSON data: {data}")
        
        if verbose:
            print("DEBUG: Verbose mode activated")
            click.echo(json.dumps(data, indent=2))
        elif version3:
            print("DEBUG: Version3 mode activated")
            content = extract_last_ai_message(data)
            click.echo(content)
        else:
            print("DEBUG: Default mode activated")
            if "text" in data:
                print(f"DEBUG: 'text' field found in data")
                click.echo(data["text"])
            else:
                print(f"DEBUG: 'text' field not found in data. Available keys: {list(data.keys())}")
                click.echo("No 'text' field found in the response")
    except requests.RequestException as e:
        print(f"DEBUG: RequestException occurred: {e}")
        click.echo(f"Error processing skill: {e}", err=True)
        exit(1)
    except json.JSONDecodeError as e:
        print(f"DEBUG: JSONDecodeError occurred: {e}")
        click.echo(f"Error parsing response: {e}", err=True)
        exit(1)
    except Exception as e:
        print(f"DEBUG: Unexpected error occurred: {e}")
        click.echo(f"An unexpected error occurred: {e}", err=True)
        exit(1)
    print("DEBUG: Exiting process_skill function")


# Alias for process-skill
cli.add_command(process_skill, name="process_skill")


if __name__ == "__main__":
    cli()
