"""
Centralized helper class for calling Azure GPT-4o and returning an
incident analysis report

from .azure_openai import generate_incident_report
md = generate_incident_report(incidents, kpi)
"""

from __future__ import __annotations__

import json
import logging
from typing import Any, Dict, List

from backoff import on_exception, expo
from openai import AzureOpenAI, RateLimitError

from .config import (
    AZURE_OAI_ENDPOINT,
    AZURE_OAI_KEY,
    AZURE_OAI_DEPLOYMENT
)

logger = loggin.getLogger(__name__)
CHAT_API_VERSION = "2024-05-01-preview"
MODEL_ROLE_SYSTEM = (
    "Blah Blah Stub for now"
)

def _get_client() -> AzureOpenAI:
    global _CLIENT
    try:
        return _CLIENT
    except NameError:
        _CLIENT = AzureOpenAI(
            azure_endpoint=AZURE_OAI_ENDPOINT,
            api_key=AZURE_OAI_KEY,
            api_version=CHAT_API_VERSION,
            timeout=60,
        )
        return _CLIENT
    
def _build_prompt(incidents: List[Dict[str, Any]], kpi: Dict[str, Any]) -> str:
    """
    Serialise the minimal fields we need; keep context small (< 6 k tokens).
    """
    slimmed = [
        {
            "number": i["number"],
            "short_description": i["short_description"],
            "priority": i["priority"],
            "state": i["state"],
        }
        for i in incidents
    ][:200]  # hard-cap to avoid context overflow

    prompt = (
        f"KPI = {json.dumps(kpi, ensure_ascii=False)}\n"
        f"INCIDENTS = {json.dumps(slimmed, ensure_ascii=False)}\n\n"
        "Write a Markdown report with:\n"
        "1. A short executive summary (<80 words)\n"
        "2. A table of KPI values (Total, P1, P2, Median Priority)\n"
        "3. Bullet list of any Priority-1 incidents (number – 10-word summary)\n"
    )
    return prompt


@on_exception(expo, RateLimitError, max_tries=4, logger=logger)
def generate_incident_report(
    incidents: List[Dict[str, Any]],
    kpi: Dict[str, Any],
) -> str:
    """Call GPT-4o and return a Markdown report string."""
    client = _get_client()
    prompt = _build_prompt(incidents, kpi)

    logger.debug("Sending %s incidents to GPT-4o (len=%s chars)",
                 len(incidents), len(prompt))

    response = client.chat.completions.create(
        deployment_id=AZURE_OAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": MODEL_ROLE_SYSTEM},
            {"role": "user", "content": prompt},
        ],
        max_tokens=800,
    )

    report_md = response.choices[0].message.content
    usage = response.usage
    logger.info(
        "GPT-4o tokens — prompt: %s, completion: %s, total: %s",
        usage.prompt_tokens,
        usage.completion_tokens,
        usage.total_tokens,
    )
    return report_md
