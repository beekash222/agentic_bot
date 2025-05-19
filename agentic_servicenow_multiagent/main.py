from agent.agent_runner import run_agent

if __name__ == "__main__":
    user_input = input("Describe the issue to create an incident: ")
    response = run_agent(user_input)
    print(f"\n🛠️ Agent Response: {response}")
