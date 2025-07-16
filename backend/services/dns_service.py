from backend.services.ton_api import tonapi_get
from typing import Dict


def get_detail_dns(domain_name:str)-> Dict:
    return tonapi_get(f"/v2/dns/{domain_name}")


def get_resolve_dns(domain_name: str)->Dict:
    return tonapi_get(f"/v2/dns/{domain_name}/resolve")

def get_dns_bids(domain_name: str)-> Dict:
    return tonapi_get(f"/v2/dns/{domain_name}/bids")

def get_dns_auctions()->Dict:
    return tonapi_get(f"/v2/dns/auctions")

