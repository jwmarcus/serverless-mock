import json
import unittest
import sys
import os

# Add the parent directory to the path so we can import serverless_mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from serverless_mock import LambdaRunner

def example_handler(event, context):
    """Example handler for testing."""
    body = json.loads(event['body'])
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }

class TestLambdaMock(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.runner = LambdaRunner()
        
    def test_context_variables(self):
        """Test setting and getting context variables."""
        self.runner.context.set_variable('test_key', 'test_value')
        response = self.runner.run(example_handler)
        
        body = json.loads(response['body'])
        self.assertEqual(body['context']['test_key'], 'test_value')
        
    def test_multiple_variables(self):
        """Test setting multiple context variables at once."""
        variables = {
            'key1': 'value1',
            'key2': 'value2'
        }
        self.runner.context.set_variables(variables)
        response = self.runner.run(example_handler)
        
        body = json.loads(response['body'])
        self.assertEqual(body['context']['key1'], 'value1')
        self.assertEqual(body['context']['key2'], 'value2')
        
    def test_additional_body(self):
        """Test adding additional body parameters."""
        additional_body = {'extra': 'data'}
        response = self.runner.run(example_handler, additional_body=additional_body)
        
        body = json.loads(response['body'])
        self.assertEqual(body['extra'], 'data')
        
    def test_clear_context(self):
        """Test clearing context variables."""
        self.runner.context.set_variable('test_key', 'test_value')
        self.runner.context.clear()
        response = self.runner.run(example_handler)
        
        body = json.loads(response['body'])
        self.assertEqual(body['context'], {})
        
if __name__ == '__main__':
    unittest.main() 