#!/usr/bin/env python3
"""
Simple script to run the example Lambda function.
"""
import sys
import json
from serverless_mock import LambdaRunner
from examples.hello_world import execute

def main():
    # Create a runner instance
    runner = LambdaRunner()
    
    # Set context variables
    runner.context.set_variables({
        'out_agent_name': 'test_agent',
        '_hubspot_company': 'Acme Corp',
        'run_id': 'local-test-123'
    })
    
    # Run the Lambda function
    response = runner.run(execute)
    
    # Pretty print the response
    print("\n=== Lambda Function Response ===\n")
    
    # Extract and parse the body if it exists
    if 'body' in response:
        try:
            body = json.loads(response['body'])
            print(f"Status Code: {response['statusCode']}")
            print("\nBody:")
            print(json.dumps(body, indent=2))
        except json.JSONDecodeError:
            print(response)
    else:
        print(response)
    
    print("\n=== End of Response ===\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 