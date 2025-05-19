from langchain.agents import Tool
from servicenow.incident_api import ServiceNowClient

client = ServiceNowClient()

create_incident_tool = Tool(
    name="CreateServiceNowIncident",
    func=lambda query: (
        f"✅ Created: {result['incident_number']}" 
        if (result := client.create_incident(short_description=query))["success"] 
        else f"❌ Failed: {result['error']}"
    ),
    description="Use this tool to create an incident in ServiceNow. Input should be a short description of the issue."
)

tools = [create_incident_tool]
