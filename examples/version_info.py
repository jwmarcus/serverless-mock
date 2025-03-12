import json
import sys
import platform
import os


def execute(event, context):
    """
    Simple serverless function that returns Python version and environment details.
    This can be used to debug the execution environment.
    """
    try:
        # Collect basic Python version info
        python_info = {
            "python_version": sys.version,
            "python_version_info": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro,
            },
            "platform": platform.platform(),
            "implementation": platform.python_implementation(),
        }
        
        # Collect environment variables (excluding sensitive ones)
        env_vars = {}
        for key, value in os.environ.items():
            # Skip potentially sensitive environment variables
            if not any(sensitive in key.lower() for sensitive in 
                      ["key", "secret", "token", "password", "credential"]):
                env_vars[key] = value
        
        # Get available modules
        try:
            import pkg_resources
            installed_packages = [
                {"name": pkg.key, "version": pkg.version}
                for pkg in pkg_resources.working_set
            ]
        except ImportError:
            installed_packages = ["pkg_resources not available"]
        
        # Return all collected information
        return {
            "statusCode": 200,
            "body": json.dumps({
                "python_info": python_info,
                "environment_variables": env_vars,
                "installed_packages": installed_packages,
                "sys_path": sys.path,
            }, default=str)  # default=str handles any non-serializable objects
        }
    except Exception as e:
        # Return a valid response even on error
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Error getting version info: {str(e)}",
                "error_type": str(type(e).__name__),
            })
        } 