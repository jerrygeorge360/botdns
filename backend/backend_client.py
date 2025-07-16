# backend_client.py
import requests
from config import INSIGHT_API_BASE

def fetch_dns_detail(domain):
    return requests.get(f"{INSIGHT_API_BASE}/dns/{domain}").json()

def fetch_dns_bids(domain):
    return requests.get(f"{INSIGHT_API_BASE}/dns/{domain}/bids").json()
