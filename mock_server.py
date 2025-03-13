#!/usr/bin/env python3
import json
import os
import importlib.util
import argparse

def load_function(file_path):
    """Load a Python function from a file path."""
    module_name = os.path.basename(file_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def create_mock_event(context_data):
    """Create a mock event object similar to what Agent.ai would send."""
    return {
        "body": json.dumps({"context": context_data}),
        "headers": {
            "content-type": "application/json",
            "host": "localhost",
            "user-agent": "MockServer/1.0"
        },
        "isBase64Encoded": False,
        "rawPath": "/",
        "requestContext": {
            "http": {
                "method": "POST",
                "path": "/"
            }
        },
        "version": "2.0"
    }

def run_function(function_path, context_file=None):
    """Run a serverless function with mock data."""
    # Load the function
    module = load_function(function_path)
    
    # Load context data
    context_data = {}
    if context_file and os.path.exists(context_file):
        with open(context_file, 'r') as f:
            context_data = json.load(f)
    
    # Create mock event
    event = create_mock_event(context_data)
    
    # Execute the function
    print(f"Running function from {function_path}...")
    result = module.execute(event, {})
    
    # Print and save the result
    if isinstance(result, dict) and 'body' in result:
        result_obj = json.loads(result['body'])
        print(json.dumps(result_obj, indent=2))
        
        # Save the result to a file
        output_file = f"{os.path.basename(function_path).replace('.py', '')}_response.json"
        with open(output_file, 'w') as f:
            json.dump(result_obj, f, indent=2)
        print(f"Response saved to {output_file}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Mock server for Agent.ai serverless functions")
    parser.add_argument("function_path", help="Path to the serverless function file")
    parser.add_argument("--context", "-c", help="Path to a JSON file with context data")
    
    args = parser.parse_args()
    run_function(args.function_path, args.context)

if __name__ == "__main__":
    main() 