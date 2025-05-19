import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute
from langchain_experimental.plan_and_execute.planners.chat_planner import load_chat_planner
from langchain_experimental.plan_and_execute.executors.agent_executor import load_agent_executor
from servicenow.incident_tools import (
    create_incident_tool,
    update_incident_tool,
    delete_incident_tool
)
from config import GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
import os


# --- TITLE ---
st.set_page_config(page_title="🧠 ServiceNow AI Agent", layout="wide")
st.title("🤖 Agentic ServiceNow Assistant")

# --- SIDEBAR LOGGING ---
if "logs" not in st.session_state:
    st.session_state.logs = []

st.sidebar.title("🪵 Action Trace")
for log in st.session_state.logs:
    st.sidebar.markdown(f"- {log}")

# --- USER INPUT ---
user_input = st.text_area("📝 Describe what you want to do (e.g., create/update/delete an incident):")

if st.button("🚀 Run Agent"):
    if not user_input.strip():
        st.warning("Please enter a valid request.")
    else:
        with st.spinner("Running planner and executing agent..."):

            # Set up planner + executor
            llm = ChatGoogleGenerativeAI(
                model='gemini-2.0-flash',
                google_api_key=GOOGLE_API_KEY,
                temperature=0.2)
            tools = [create_incident_tool, update_incident_tool, delete_incident_tool]

            planner = load_chat_planner(llm)
            executor = load_agent_executor(llm, tools, verbose=True)
            agent = PlanAndExecute(planner=planner, executor=executor)

            try:
                result = agent.run(user_input)
                st.success("✅ Done")
                st.markdown("### 🧾 Result:")
                st.code(result)

                # Log trace
                st.session_state.logs.append(f"🧠 Input: {user_input}")
                st.session_state.logs.append(f"✅ Output: {result}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.session_state.logs.append(f"❌ Error: {e}")
