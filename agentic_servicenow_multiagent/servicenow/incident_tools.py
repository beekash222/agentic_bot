# incident_tools.py

from langchain.tools import tool
from servicenow.incident_api import ServiceNowClient

@tool
def create_incident_tool(description: str) -> str:
    """Create a ServiceNow incident."""
    client = ServiceNowClient()
    result = client.create_incident(description)
    return f"✅ Created: {result['incident_number']}" if result["success"] else f"❌ Failed: {result['error']}"

@tool
def update_incident_tool(number: str, description: str) -> str:
    """Update an existing ServiceNow incident by number."""
    client = ServiceNowClient()
    result = client.update_incident(number, {"short_description": description})
    return "✅ Updated successfully" if result["success"] else f"❌ Failed: {result['error']}"

@tool
def delete_incident_tool(number: str) -> str:
    """Delete an incident by number."""
    client = ServiceNowClient()
    result = client.delete_incident(number)
    return "🗑️ Deleted successfully" if result["success"] else f"❌ Failed: {result['error']}"
