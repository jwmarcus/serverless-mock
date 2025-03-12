#!/usr/bin/env python3
"""
Script to run the LinkedIn profile parser Lambda function.
"""
import sys
import json
import os
from serverless_mock import LambdaRunner
from examples.linkedin_parser import execute

def load_example_profile():
    """Load the example LinkedIn profile data."""
    try:
        file_path = os.path.join('example_data', 'example_linkedin_profile.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading example profile: {e}")
        return None

def main():
    # Load the example profile
    profile_data = load_example_profile()
    
    if not profile_data:
        print("Failed to load example profile data.")
        return 1
    
    # Create a runner instance
    runner = LambdaRunner()
    
    # Set context variables if needed
    runner.context.set_variables({
        'run_id': 'linkedin-parser-test'
    })
    
    # Add the profile data to the event body
    additional_body = {
        "profile_data": profile_data
    }
    
    # Run the Lambda function
    response = runner.run(execute, additional_body)
    
    # Pretty print the response
    print("\n=== LinkedIn Profile Parser Response ===\n")
    
    # Extract and parse the body if it exists
    if 'body' in response:
        try:
            body = json.loads(response['body'])
            print(f"Status Code: {response['statusCode']}")
            
            if 'formatted_text' in body:
                print("\nFormatted Text for LLM:")
                print("------------------------")
                print(body['formatted_text'])
            else:
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