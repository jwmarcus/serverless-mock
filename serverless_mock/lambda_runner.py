from typing import Any, Callable, Dict, Optional
from .lambda_context import LambdaContext

class LambdaRunner:
    def __init__(self):
        self.context = LambdaContext()
        
    def run(self, handler: Callable, additional_body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run a Lambda function handler with the current context.
        
        Args:
            handler: The Lambda function handler to execute
            additional_body: Additional body parameters to include in the event
            
        Returns:
            The response from the Lambda function
        """
        # Generate the event with current context
        event = self.context.generate_event(additional_body)
        
        # Create a minimal context object that mimics AWS Lambda
        lambda_context = type('LambdaContext', (), {
            'function_name': 'local-test',
            'function_version': '$LATEST',
            'invoked_function_arn': 'arn:aws:lambda:local:000000000000:function:local-test',
            'memory_limit_in_mb': 128,
            'aws_request_id': 'local-test',
            'log_group_name': '/aws/lambda/local-test',
            'log_stream_name': 'local-test',
        })()
        
        # Execute the handler
        return handler(event, lambda_context) 