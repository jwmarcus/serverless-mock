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
    
    # Create a response
    response = {
        "message": "Function executed successfully!",
        # "input": event,  # Uncomment for debugging
        "data": {
            "run_id": run_id,
            "user_input": user_input
        }
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(response)
    } 