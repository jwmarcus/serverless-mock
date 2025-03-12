import json
from typing import Dict, Any

def execute(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Example Lambda function that uses context variables.
    
    Args:
        event: AWS Lambda event object
        context: AWS Lambda context object
        
    Returns:
        Dict containing the response with status code and body
    """
    # Parse the body from the event
    body = json.loads(event['body'])
    agent_context = body.get('context', {})
    
    # Access context variables
    agent_name = agent_context.get('out_agent_name', 'unknown')
    company = agent_context.get('_hubspot_company', 'unknown')
    
    # Create response
    response_body = {
        "message": f"Hello from your Lambda function!",
        "agent_name": agent_name,
        "company": company,
        "event": event
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(response_body, indent=2)
    } 