from langchain.agents import load_tools
from langchain.agents import PlanAndExecute, load_agent_executor, load_agent_planner
from langchain_google_genai import ChatGoogleGenerativeAI
from servicenow.incident_tools import (
    create_incident_tool,
    update_incident_tool,
    delete_incident_tool
)
import os
from config import GOOGLE_API_KEY

def run_planner_executor(user_input: str):
    llm = ChatGoogleGenerativeAI(
                model='gemini-2.0-flash',
                google_api_key=GOOGLE_API_KEY,
                temperature=0.2)

    tools = [
        create_incident_tool,
        update_incident_tool,
        delete_incident_tool
    ]

    planner = load_agent_planner(llm)
    executor = load_agent_executor(llm, tools, verbose=True)

    agent = PlanAndExecute(planner=planner, executor=executor)
    result = agent.run(user_input)
    print(result)
