# Serverless Mock

A lightweight Python package for locally testing AWS Lambda functions by simulating the Lambda execution environment. This package is particularly useful when you need to test Lambda functions that rely on context variables without deploying to AWS.

## Features

- Simulate AWS Lambda execution environment locally
- Easy management of context variables
- Mimics AWS Lambda event and context structures
- Type hints for better IDE support
- Minimal dependencies

## Project Structure

```
serverless-mock/
├── serverless_mock/        # Main package
│   ├── __init__.py
│   ├── lambda_context.py
│   └── lambda_runner.py
├── examples/               # Example Lambda functions and usage
│   ├── hello_world.py     # Example Lambda function
│   └── test_hello_world.py # Example of how to test the function
├── tests/                 # Unit tests
│   └── test_lambda_mock.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone this repository
2. Install the requirements:

```bash
pip install -r requirements.txt
```

## Quick Start

1. Create your Lambda function (see `examples/hello_world.py`):

```python
import json
from typing import Dict, Any

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    # Parse the body from the event
    body = json.loads(event['body'])
    agent_context = body.get('context', {})

    # Access context variables
    agent_name = agent_context.get('out_agent_name', 'unknown')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Hello, {agent_name}!"
        })
    }
```

2. Test your function (see `examples/test_hello_world.py`):

```python
from serverless_mock import LambdaRunner
from hello_world import handler

# Create runner
runner = LambdaRunner()

# Set context variables
runner.context.set_variable('out_agent_name', 'test_agent')

# Run the function
response = runner.run(handler)
print(response)
```

## Running Tests

### Running the Example

To run the example Lambda function:

```bash
python examples/test_hello_world.py
```

### Running Unit Tests

To run the unit tests:

```bash
python -m unittest tests/test_lambda_mock.py
```

## API Reference

### LambdaRunner

The main class for executing Lambda functions locally.

```python
runner = LambdaRunner()
```

Methods:

- `run(handler, additional_body=None)`: Execute a Lambda function with the current context
  - `handler`: Your Lambda function
  - `additional_body`: Optional dictionary of additional body parameters

### LambdaContext

Manages context variables for the Lambda execution.

```python
context = runner.context
```

Methods:

- `set_variable(key, value)`: Set a single context variable
- `set_variables(variables)`: Set multiple context variables at once
- `get_variable(key, default=None)`: Get a context variable
- `clear()`: Clear all context variables

## Example Usage

### Basic Example

See `examples/hello_world.py` for a complete Lambda function example and `examples/test_hello_world.py` for how to test it.

### Setting Multiple Variables

```python
runner = LambdaRunner()

# Set multiple variables at once
variables = {
    'out_agent_name': 'test_agent',
    '_hubspot_company': 'test_company',
    'environment': 'development'
}
runner.context.set_variables(variables)
```

### Adding Additional Body Parameters

```python
runner = LambdaRunner()
runner.context.set_variable('user_id', '12345')

# Add additional body parameters
additional_body = {
    'timestamp': '2024-03-11T18:24:35Z',
    'request_id': 'test-123'
}

response = runner.run(handler, additional_body=additional_body)
```

## Event Structure

The package generates an event structure that matches AWS Lambda's format:

```python
{
    "body": json.dumps({
        "context": {
            # Your context variables here
        },
        # Additional body parameters here
    }),
    "headers": {
        "content-type": "application/json",
        "user-agent": "Serverless-Mock-Local-Test"
    },
    "requestContext": {
        "http": {
            "method": "POST",
            "path": "/"
        }
    },
    "isBase64Encoded": False,
    "rawPath": "/",
    "version": "2.0"
}
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Add tests for any new functionality
4. Ensure all tests pass
5. Submit a pull request

Feel free to submit issues and enhancement requests!
