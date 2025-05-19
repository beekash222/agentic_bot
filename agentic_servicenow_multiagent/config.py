from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access environment variables
SERVICENOW_INSTANCE = os.getenv("SERVICENOW_INSTANCE")
SERVICENOW_USERNAME = os.getenv("SERVICENOW_USERNAME")
SERVICENOW_PASSWORD = os.getenv("SERVICENOW_PASSWORD")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
