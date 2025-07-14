import requests, datetime
from requests.auth import HTTPBasicAuth
from .config import SN_INSTANCE, SN_USER, SN_PASSWORD

def fetch_incidents(hours_back: int = 24, limit: int = 1000):
    since = (datetime.datetime.utcnow() - datetime.timedelta(hours=hours_back)).strftime("%Y-%m-%d %H:%M:%S")
    url = f"{SN_INSTANCE}/api/now/table/incident"
    params = {
        "sysparm_query": f"sys_created_on>={since}",
        "sysparm_limit": limit,
        "sysparm_display_value": "true",
    }
    resp = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(SN_USER, SN_PASSWORD),
        headers={"Accept": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["result"]