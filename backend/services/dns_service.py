from typing import Dict
from .ton_api import tonapi_get

def get_detail_dns(domain_name:str)-> Dict:
    return tonapi_get(f"/v2/dns/{domain_name}")


def get_resolve_dns(domain_name: str)->Dict:
    return tonapi_get(f"/v2/dns/{domain_name}/resolve")

def get_dns_bids(domain_name: str)-> Dict:
    return tonapi_get(f"/v2/dns/{domain_name}/bids")

def get_dns_auctions()->Dict:
    return tonapi_get(f"/v2/dns/auctions")

def get_account_info(address:str):
    return tonapi_get(f"/v2/accounts/{address}")


def get_account_events(address:str):
    return tonapi_get(f"/v2/accounts/{address}/events")

def get_account_jettons(address:str):
    return tonapi_get(f"/v2/accounts/{address}/jettons")

def get_account_nfts(address:str):
    return tonapi_get(f"/v2/accounts/{address}/nfts")

