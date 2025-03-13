"""
Agent.ai Serverless Mock Runner

A simple script to run Agent.ai serverless functions locally.
"""
import os
import sys
from mock_server import run_function

def print_usage():
    print("Usage:")
    print("  python run.py <function_file> [context_file]")
    print("")
    print("Examples:")
    print("  python run.py example_function.py")
    print("  python run.py example_function.py sample_context.json")
    print("")
    print("If no context file is provided, an empty context will be used.")

def main():
    # Check arguments
    if len(sys.argv) < 2:
        print_usage()
        return
    
    # Get function path
    function_path = sys.argv[1]
    if not os.path.exists(function_path):
        print(f"Error: Function file '{function_path}' not found.")
        return
    
    # Get context path (optional)
    context_path = None
    if len(sys.argv) > 2:
        context_path = sys.argv[2]
        if not os.path.exists(context_path):
            print(f"Warning: Context file '{context_path}' not found. Using empty context.")
            context_path = None
    
    # Run the function
    run_function(function_path, context_path)

if __name__ == "__main__":
    main() 