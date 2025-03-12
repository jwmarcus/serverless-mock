import json
from typing import Any, Dict, Optional

class LambdaContext:
    def __init__(self):
        self._context: Dict[str, Any] = {}
        
    def set_variable(self, key: str, value: Any) -> None:
        """Set a context variable."""
        self._context[key] = value
        
    def set_variables(self, variables: Dict[str, Any]) -> None:
        """Set multiple context variables at once."""
        self._context.update(variables)
        
    def get_variable(self, key: str, default: Any = None) -> Any:
        """Get a context variable."""
        return self._context.get(key, default)
        
    def clear(self) -> None:
        """Clear all context variables."""
        self._context.clear()
        
    def generate_event(self, additional_body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a Lambda event with the current context."""
        event_body = {
            "context": self._context
        }
        
        if additional_body:
            event_body.update(additional_body)
            
        return {
            "body": json.dumps(event_body),
            "headers": {
                "content-type": "application/json",
                "user-agent": "Serverless-Mock-Local-Test"
            },
            "requestContext": {
                "http": {
                    "method": "POST",
                    "path": "/",
                }
            },
            "isBase64Encoded": False,
            "rawPath": "/",
            "version": "2.0"
        } 