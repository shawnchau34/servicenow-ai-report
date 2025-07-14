from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

# ServiceNow
SN_INSTANCE   = os.getenv("SN_INSTANCE")
SN_USER       = os.getenv("SN_USER")
SN_PASSWORD   = os.getenv("SN_PASSWORD")

# Azure OpenAI (optional stub for now)
AZURE_OAI_ENDPOINT   = os.getenv("AZURE_OAI_ENDPOINT")
AZURE_OAI_KEY        = os.getenv("AZURE_OAI_KEY")
AZURE_OAI_DEPLOYMENT = os.getenv("AZURE_OAI_DEPLOYMENT")

# Graph (we’ll wire this later)
GRAPH_CLIENT_ID     = os.getenv("GRAPH_CLIENT_ID")
GRAPH_CLIENT_SECRET = os.getenv("GRAPH_CLIENT_SECRET")
GRAPH_TENANT_ID     = os.getenv("GRAPH_TENANT_ID")
MAIL_SENDER         = os.getenv("MAIL_SENDER")
MAIL_RECIPIENTS     = [m.strip() for m in os.getenv("MAIL_RECIPIENTS", "").split(",") if m]