# Agent.ai Serverless Mock

A simple tool for testing Agent.ai serverless functions locally.

## Overview

This tool allows you to run Agent.ai serverless functions on your local machine before deploying them to Agent.ai. It simulates the Agent.ai serverless environment by:

1. Creating a mock event object similar to what Agent.ai would send
2. Executing your function with this mock event
3. Displaying and saving the response

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

1. Clone this repository or download the files
2. No additional dependencies required!

## Usage

### Creating a New Function

The easiest way to create a new function is with the function creator script:

```bash
python create_function.py your_function_name
```

This will create:

- `your_function_name.py` - A template function file
- `your_function_name_context.json` - A template context file

### Running a Function

Use the runner script to run your function:

```bash
python run.py path/to/your_function.py [path/to/context.json]
```

### Using the Mock Server Directly

You can also use the mock server directly:

```bash
python mock_server.py path/to/your_function.py --context path/to/context.json
```

### Examples

```bash
# Create a new function
python create_function.py my_function

# Run the example function with the sample context
python run.py examples/example_function.py examples/sample_context.json

# Run your new function
python run.py my_function.py my_function_context.json
```

## How It Works

### Function Structure

Your Agent.ai serverless function should have an `execute` function that takes two parameters:

- `event`: Contains the request data, including the context in `event['body']`
- `context`: Usually empty in Agent.ai functions

Example:

```python
import json

def execute(event, context):
    # Extract context from the event
    agent_context = {}
    if event and 'body' in event:
        try:
            body_data = json.loads(event['body'])
            if 'context' in body_data:
                agent_context = body_data['context']
        except:
            pass

    # Access context variables
    run_id = agent_context.get('run_id', 'unknown')
    user_input = agent_context.get('user_input', '')

    # Your function logic here

    # Return response
    response = {
        "message": "Function executed successfully!",
        "data": {
            "run_id": run_id,
            "user_input": user_input
        }
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
```

### Context Data

The context data is a JSON object that contains variables you want to access in your function. For example:

```json
{
  "run_id": "8c9d1fb64d46473aab11f373fdabaadb",
  "user_input": "Tell me about HubSpot",
  "out_agent_list": {
    "list": [
      {
        "agent_id": "companyresearch",
        "name": "Company Research Agent"
      }
    ]
  }
}
```

In your function, you can access these variables through `agent_context`:

```python
run_id = agent_context.get('run_id', 'default_value')
user_input = agent_context.get('user_input', '')
agent_list = agent_context.get('out_agent_list', {}).get('list', [])
```

## Tips for Agent.ai Development

1. **Keep functions simple**: Agent.ai functions should be focused on a single task
2. **Handle errors gracefully**: Always use try/except blocks when parsing input
3. **Test locally first**: Use this mock server to test your functions before deploying
4. **Minimize dependencies**: Agent.ai has limited support for external libraries

## Project Structure

```text
agent-ai-serverless-mock/
├── mock_server.py         # The main mock server script
├── run.py                 # Simple runner script
├── create_function.py     # Function creator script
├── README.md              # This documentation
└── examples/              # Example files
    ├── example_function.py    # Example function for reference
    └── sample_context.json    # Sample context data
```

## Development Workflow

1. **Create a new function**:

   ```bash
   python create_function.py my_function
   ```

2. **Edit your function**:
   Open `my_function.py` and add your logic

3. **Edit your context**:
   Open `my_function_context.json` and add your test data

4. **Test your function**:

   ```bash
   python run.py my_function.py my_function_context.json
   ```

5. **Copy to Agent.ai**:
   Copy the contents of `my_function.py` to the Agent.ai function editor

## Copying to Agent.ai

Once you've tested your function locally, you can copy the function code directly into the Agent.ai function editor. Make sure to:

1. Include all necessary imports at the top
2. Keep the `execute(event, context)` function signature
3. Remove any debugging code or print statements
