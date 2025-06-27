#!/usr/bin/env python3
"""
Mock Server for Agent.ai Serverless Functions

This module provides a mock server to test Agent.ai serverless functions locally.
It simulates the event structure and execution environment that would be provided
by the Agent.ai platform.

Usage:
    python mock_server.py <function_path> [--context <context_file>]

Example:
    python mock_server.py my_function.py --context test_context.json
"""

import json
import os
import importlib.util
import argparse

def load_function(file_path):
    """
    Load a Python function from a file path.
    
    Args:
        file_path (str): Path to the Python file containing the serverless function
        
    Returns:
        module: The loaded Python module containing the execute function
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ImportError: If the module cannot be loaded
    """
    module_name = os.path.basename(file_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def create_mock_event(context_data):
    """
    Create a mock event object similar to what Agent.ai would send.
    
    This function creates an AWS Lambda-style event object that mimics
    the structure and format of events sent by the Agent.ai platform.
    
    Args:
        context_data (dict): Context data to include in the event body
        
    Returns:
        dict: Mock event object with Agent.ai-compatible structure
    """
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
    """
    Run a serverless function with mock data.
    
    This function orchestrates the entire mock execution process:
    1. Loads the specified serverless function
    2. Loads optional context data from a JSON file
    3. Creates a mock event object
    4. Executes the function with the mock event
    5. Processes and saves the response
    
    Args:
        function_path (str): Path to the Python file containing the serverless function
        context_file (str, optional): Path to JSON file with context data
        
    Raises:
        FileNotFoundError: If the function file doesn't exist
        json.JSONDecodeError: If the context file contains invalid JSON
        AttributeError: If the function module doesn't have an 'execute' method
    """
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
    """
    Main entry point for the mock server.
    
    Parses command line arguments and executes the specified serverless function
    with optional context data.
    """
    parser = argparse.ArgumentParser(description="Mock server for Agent.ai serverless functions")
    parser.add_argument("function_path", help="Path to the serverless function file")
    parser.add_argument("--context", "-c", help="Path to a JSON file with context data")
    
    args = parser.parse_args()
    run_function(args.function_path, args.context)

if __name__ == "__main__":
    main() 