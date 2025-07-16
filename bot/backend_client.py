# backend_client.py
import os
import json
import requests

INSIGHT_API_BASE = os.getenv("INSIGHT_API_BASE", "http://localhost:5000")


def fetch_domain_analysis(domain: str) -> dict | None:
    try:
        res = requests.get(f"{INSIGHT_API_BASE}/api/analyze/{domain}", timeout=60)
        res.raise_for_status()
        return res.json()
    except:
        return None

def fetch_account_info(address: str) -> dict | None:
    try:
        res = requests.get(f"{INSIGHT_API_BASE}/api/accounts/{address}", timeout=30)
        res.raise_for_status()
        return res.json()
    except:
        return None

def resolve_domain_to_address(domain: str) -> str | None:
    try:
        res = requests.get(f"{INSIGHT_API_BASE}/api/resolve/{domain}", timeout=10)
        return res.json().get("address")
    except:
        return None

def fetch_recent_transactions(address: str) -> list:
    try:
        resolved_dns = requests.get(f"{INSIGHT_API_BASE}/api/resolve/{address}", timeout=10)
        return resolved_dns.json().get("wallet_account", [])
    except:
        return []

def subscribe_user(user_id: int, address: str) -> bool:
    try:
        filepath = "wallet_subs.json"
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump({}, f)

        with open(filepath, "r+") as f:
            data = json.load(f)
            data.setdefault(str(user_id), [])
            if address not in data[str(user_id)]:
                data[str(user_id)].append(address)
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=2)
        return True
    except:
        return False
