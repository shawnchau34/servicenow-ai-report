from openai import AzureOpenAI
from .config import AZURE_OAI_ENDPOINT, AZURE_OAI_KEY, AZURE_OAI_DEPLOYMENT
import statistics, textwrap
from typing import List, Dict

def local_summary(incidents: List[Dict]) -> str:
    """Return a markdown summary with simple KPIs."""
    if not incidents:
        return "_No incidents in the period — all quiet!_"

    priorities = [int(i["priority"]) for i in incidents if i["priority"].isdigit()]
    kpi = {
        "total": len(incidents),
        "p1": priorities.count(1),
        "p2": priorities.count(2),
        "median_priority": statistics.median(priorities) if priorities else "n/a",
    }
    top5 = "\n".join(f"- {i['number']}: {i['short_description']}"
                     for i in incidents[:5])

    md = textwrap.dedent(f"""
    ## Daily Incident Summary

    **Total incidents:** {kpi['total']}  
    **P1:** {kpi['p1']}   **P2:** {kpi['p2']}   **Median priority:** {kpi['median_priority']}

    **First five incidents**
    {top5}

    ---
    _Replace this section by calling GPT-4o once your Azure endpoint is ready._
    """)
    return md

#Azure endpoint#
client = AzureOpenAI(
    azure_endpoint = AZURE_OAI_ENDPOINT,
    api_key        = AZURE_OAI_KEY,
    api_version    = "2024-05-01-preview"
)

completion = client.chat.completions.create(
    deployment_id = AZURE_OAI_DEPLOYMENT,
    messages = [
        {"role": "system", "content": "You are an ITSM report generator."}, # type: ignore
        {"role": "user",
         "content": f"Here is today's incident JSON:\n\n{json_payload}\n\n"
                    "Return a bullet summary, KPI table, and any P1 details."}
    ],
    max_tokens = 800
)
report_md = completion.choices[0].message.content
