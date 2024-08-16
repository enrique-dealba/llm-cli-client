# llm-cli-client

## Getting Started:

1. Pip install:
```bash
pip install git+https://github.com/enrique-dealba/llm-cli-client.git
```

2. How to use:
```bash
llm-client --help
```

## Usage:

1. Check the health of the LLM server:

```bash
llm-client health
```

This should return `LLM is initialized and ready.`

2. Process a spaceplan skill:

```bash
llm-client process-skill --text "Track RSO target 28884 with sensors..."
```

Note: Both `llm_client.py process-skill` and `llm_client.py process_skill` work.

2.1. Here's an example for a Periodic Revisit Objective prompt:

```bash
llm-client process-skill --text \
"Track RSO target 28884 with the sensors RME01 and RME02 in TEST mode \
for a 36 hour plan, schedule four periodic revisits per hour and use 'U' markings. \
Start at 2024-05-25 17:30:00.500000+00:00, end at 2024-05-26 22:30:00.250000+00:00. \
Make sure to use RATE_TRACK_SIDEREAL tracking and set the priority to 3, \
and patience to 30 mins"
```

3. Generate general, unstructured text using the LLM:

```bash
llm-client generate --text "Your prompt here..."
```

## Configurations

The default LLM server URL is `http://localhost:8888`. You can change this by setting the `LLM_SERVER_URL` environment variable:

### On Linux or macOS:

```bash
export LLM_SERVER_URL="http://your-server-url:port"
python llm_client.py health
```

### On Windows:

```bash
set LLM_SERVER_URL=http://your-server-url:port
python llm_client.py health
```

## Tests

1. To run the tests:

```bash
pytest tests/test_llm_client.py
```

Note: If `pytest` is not yet installed then:

```bash
pip install pytest
```
