import sys
import os

# Add the parent directory to the path so we can import serverless_mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from serverless_mock import LambdaRunner
from hello_world import execute

def test_basic_execution():
    """Test basic Lambda function execution with context variables."""
    # Create runner
    runner = LambdaRunner()
    
    # Set context variables
    runner.context.set_variables({
        'out_agent_name': 'test_agent',
        '_hubspot_company': 'Acme Corp'
    })
    
    # Run the function
    response = runner.run(execute)
    
    # Print the response
    print("\nTest Basic Execution:")
    print("--------------------")
    print(response)

def test_with_additional_body():
    """Test Lambda function with additional body parameters."""
    runner = LambdaRunner()
    
    # Set context variables
    runner.context.set_variable('out_agent_name', 'test_agent')
    
    # Add additional body parameters
    additional_body = {
        'timestamp': '2024-03-11T18:24:35Z',
        'request_id': 'test-123'
    }
    
    # Run the function
    response = runner.run(execute, additional_body=additional_body)
    
    # Print the response
    print("\nTest With Additional Body:")
    print("-------------------------")
    print(response)

if __name__ == "__main__":
    test_basic_execution()
    test_with_additional_body() 