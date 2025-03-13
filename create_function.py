#!/usr/bin/env python3
"""
Agent.ai Function Creator

A simple script to create new Agent.ai serverless functions and context files.
"""
import os
import sys
import json

FUNCTION_TEMPLATE = '''#!/usr/bin/env python3
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
    
    # TODO: Add your function logic here
    
    # Create a response
    response = {
        "message": "Function executed successfully!",
        "data": {
            "run_id": run_id,
            "user_input": user_input,
            # Add your response data here
        }
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
'''

CONTEXT_TEMPLATE = {
    "run_id": "example_run_id",
    "user_input": "Example user input",
    "custom_variable": "Add your custom variables here"
}

def print_usage():
    print("Usage:")
    print("  python create_function.py <function_name>")
    print("")
    print("Example:")
    print("  python create_function.py my_function")
    print("")
    print("This will create:")
    print("  - my_function.py")
    print("  - my_function_context.json")

def create_function(function_name):
    # Create function file
    function_file = f"{function_name}.py"
    if os.path.exists(function_file):
        print(f"Warning: {function_file} already exists. Skipping.")
    else:
        with open(function_file, 'w') as f:
            f.write(FUNCTION_TEMPLATE)
        print(f"Created {function_file}")
    
    # Create context file
    context_file = f"{function_name}_context.json"
    if os.path.exists(context_file):
        print(f"Warning: {context_file} already exists. Skipping.")
    else:
        with open(context_file, 'w') as f:
            json.dump(CONTEXT_TEMPLATE, f, indent=2)
        print(f"Created {context_file}")
    
    print("\nTo run your function:")
    print(f"  python run.py {function_file} {context_file}")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    function_name = sys.argv[1]
    create_function(function_name)

if __name__ == "__main__":
    main() 