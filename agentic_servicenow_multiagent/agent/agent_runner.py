from langchain.agents import initialize_agent
from agent.tools import tools
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY

def run_agent(prompt):
    llm = ChatGoogleGenerativeAI(
                model='gemini-2.0-flash',
                google_api_key=GOOGLE_API_KEY,
                temperature=0.2
    )
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True
    )
    return agent.run(prompt)
