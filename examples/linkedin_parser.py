import json
from typing import Dict, Any, List, Optional


def safe_get(obj: Any, *keys, default=None) -> Any:
    """Safely get a nested value from a dictionary without raising exceptions."""
    if not isinstance(obj, dict):
        return default
    
    current = obj
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current.get(key)
    
    return current


def extract_field(data: Dict[str, Any], field_names: List[str], default: Any = "") -> Any:
    """Extract a field from data using multiple possible field names."""
    for name in field_names:
        value = safe_get(data, name)
        if value:
            return value
    return default


def parse_date(position: Dict[str, Any], is_start_date: bool = True) -> str:
    """Parse date information from position data."""
    # Default values
    date_str = ""
    
    # Try standard nested structure first
    date_type = "start" if is_start_date else "end"
    year = safe_get(position, "date", date_type, "year")
    
    if year:
        month = safe_get(position, "date", date_type, "month", default="")
        date_str = f"{month}/{year}" if month else str(year)
    else:
        # Try alternative date fields
        if is_start_date:
            date_str = extract_field(position, ["start_date", "from_date"])
        else:
            date_str = extract_field(position, ["end_date", "to_date"])
            if not date_str:
                date_str = "Present"  # Default for end date
                
    return date_str


def parse_single_position(position: Dict[str, Any], default_company: str = "Unknown Company") -> Optional[Dict[str, Any]]:
    """Parse a single position entry from LinkedIn data."""
    if not isinstance(position, dict):
        return None
        
    # Extract basic position details
    title = extract_field(position, ["title", "position", "role"], "Unknown Title")
    description = extract_field(position, ["description", "summary"])
    company = extract_field(position, ["company", "company_name", "organization"], default_company)
    
    # Parse dates
    start_date = parse_date(position, is_start_date=True)
    end_date = parse_date(position, is_start_date=False)
    
    # Format date range
    date_range = f"{start_date} - {end_date}" if start_date else end_date
    
    return {
        "company": company,
        "title": title,
        "date_range": date_range,
        "description": description
    }


def parse_linkedin_profile(profile_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse LinkedIn profile data to extract position information."""
    parsed_positions = []
    
    # Try different possible structures for position data
    
    # 1. Try position_groups structure
    position_groups = safe_get(profile_data, "position_groups", default=[])
    if isinstance(position_groups, list) and position_groups:
        for group in position_groups:
            company_name = safe_get(group, "company", "name", default="Unknown Company")
            positions = safe_get(group, "profile_positions", default=[])
            
            if isinstance(positions, list):
                for position in positions:
                    parsed_position = parse_single_position(position, default_company=company_name)
                    if parsed_position:
                        parsed_positions.append(parsed_position)
        
        if parsed_positions:
            return parsed_positions
    
    # 2. Try direct positions list
    for field_name in ["positions", "experience"]:
        positions = safe_get(profile_data, field_name, default=[])
        if isinstance(positions, list) and positions:
            for position in positions:
                parsed_position = parse_single_position(position)
                if parsed_position:
                    parsed_positions.append(parsed_position)
            
            if parsed_positions:
                return parsed_positions
    
    return parsed_positions


def format_for_llm(parsed_positions: List[Dict[str, Any]]) -> str:
    """Format parsed positions for LLM consumption."""
    if not parsed_positions:
        return "No position information available."
    
    formatted_text = ""
    
    for position in parsed_positions:
        company = position.get("company", "Unknown Company")
        title = position.get("title", "Unknown Title")
        date_range = position.get("date_range", "")
        description = position.get("description", "")
        
        formatted_text += f"{company}\n"
        formatted_text += f"{title} ({date_range})\n"
        formatted_text += f"{description}\n\n"
    
    return formatted_text


def find_profile_data(body: Dict[str, Any]) -> Dict[str, Any]:
    """Find profile data in various possible locations within the request body."""
    # Check if body itself contains profile data
    if any(key in body for key in ["profile_id", "positions", "experience"]):
        return body
    
    # Check if profile_data is directly in body
    if "profile_data" in body:
        return body.get("profile_data", {})
    
    # Check in context
    context = body.get("context", {})
    if not isinstance(context, dict):
        return {}
    
    # Check if profile_data is in context
    if "profile_data" in context:
        return context.get("profile_data", {})
    
    # Check in user.context
    user = context.get("user", {})
    if isinstance(user, dict) and "context" in user:
        user_context = user.get("context", {})
        if isinstance(user_context, dict) and "profile_data" in user_context:
            return user_context.get("profile_data", {})
    
    return {}


def execute(event, context):
    """Lambda function handler."""
    try:
        # Extract body content
        body = {}
        if isinstance(event, dict):
            if isinstance(event.get("body"), str):
                try:
                    body = json.loads(event.get("body", "{}"))
                except json.JSONDecodeError:
                    body = {}
            else:
                body = event.get("body", {})
        
        # Find profile data in the request
        profile_data = find_profile_data(body)
        
        # Debug information
        debug_info = {
            "found_profile_data": bool(profile_data),
            "profile_data_keys": list(profile_data.keys()) if isinstance(profile_data, dict) else None
        }
        
        if not profile_data:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "No profile data provided", 
                    "formatted_text": "", 
                    "parsed_positions": [],
                    "debug_info": debug_info
                })
            }
        
        # Parse the profile data
        parsed_positions = parse_linkedin_profile(profile_data)
        
        # Format for LLM
        formatted_text = format_for_llm(parsed_positions)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "formatted_text": formatted_text,
                "parsed_positions": parsed_positions,
                "debug_info": debug_info
            })
        }
    except Exception as e:
        # Return a valid response even on error
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Error processing request: {str(e)}",
                "formatted_text": "",
                "parsed_positions": [],
                "error_details": str(e)
            })
        } 