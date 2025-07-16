from datetime import datetime
from typing import Dict
def format_dns_detail_insight_input(data: dict) -> str:
    item = data.get("item", {})
    metadata = item.get("metadata", {})
    owner = item.get("owner", {})
    collection = item.get("collection", {})
    sale = item.get("sale", {})
    sale_owner = sale.get("owner", {})
    market = sale.get("market", {})
    price = sale.get("price", {})
    approved_by = item.get("approved_by", [])
    trust = item.get("trust", "unknown")
    previews = item.get("previews", [])
    expiring_at = data.get("expiring_at")

    def format_price():
        try:
            value = int(price.get("value", 0)) / 10**price.get("decimals", 9)
            return f"{value:.2f} {price.get('token_name', 'TON')}"
        except:
            return "Unknown"

    def format_expiry():
        if expiring_at:
            return datetime.utcfromtimestamp(expiring_at).strftime("%Y-%m-%d")
        return "Unknown"

    def get_preview():
        if previews:
            return previews[-1].get("url")
        return "No preview image"

    return f"""
Domain Name: {data.get("name")}
Expiry Date: {format_expiry()}
Verified: {item.get("verified", False)}
DNS Trust Level: {trust}
Collection: {collection.get("name", "N/A")} - {collection.get("description", "")}
Owner Address: {owner.get("address", "Unknown")}
Sale Status: {"Yes" if sale else "No"}
Market: {market.get("name", "Unknown")}
Price: {format_price()}
Sale Listed By: {sale_owner.get("name", "Unknown")}
Approved By: {', '.join(approved_by) if approved_by else 'None'}
Preview Image: {get_preview()}
Manage Link: {metadata.get("buttons", [{}])[0].get("uri", "None")}
"""

def format_dns_resolve_input(data: dict) -> str:
    wallet = data.get("wallet", {})
    account = wallet.get("account", {})
    address = wallet.get("address")
    account_name = account.get("name", "Unknown")
    is_wallet = account.get("is_wallet", False)
    is_scam = account.get("is_scam", False)
    names = wallet.get("names", [])
    sites = data.get("sites", [])

    return f"""
Resolved Wallet Address: {address}
Account Name: {account_name}
Is Wallet: {is_wallet}
Scam Flag: {"Yes" if is_scam else "No"}
Linked Names: {', '.join(names) if names else 'None'}
Linked Sites: {', '.join(sites) if sites else 'None'}
"""

def format_dns_resolve_input_1(data: dict) -> Dict:
    wallet = data.get("wallet", {})
    account = wallet.get("account", {})
    return {'wallet_account':account}

def format_dns_bids_input(data: dict) -> str:
    bids = data.get("data", [])

    if not bids:
        return "No bids were found for this domain."

    lines = []
    for bid in bids:
        value = int(bid.get("value", 0)) / 1e9  # Convert nanotons to TON
        tx_time = datetime.utcfromtimestamp(bid.get("txTime", 0)).strftime("%Y-%m-%d %H:%M:%S")
        bidder = bid.get("bidder", {})
        bidder_name = bidder.get("name", "Unknown")
        scam_flag = "⚠️ Scam suspected" if bidder.get("is_scam") else "✅ Clean"
        wallet_flag = "Wallet" if bidder.get("is_wallet") else "Contract"

        lines.append(
            f"- 🧑 Bidder: {bidder_name} ({wallet_flag})\n"
            f"  🔗 Address: {bidder.get('address')}\n"
            f"  💰 Bid Amount: {value:.2f} TON\n"
            f"  🕒 Time: {tx_time}\n"
            f"  ✅ Successful: {bid.get('success')}\n"
            f"  {scam_flag}"
        )

    return "\n\n".join(lines)


def format_dns_data_for_ai(data: dict) -> str:
    item = data.get("item", {})
    sale = item.get("sale", {})
    owner = sale.get("owner", {})
    market = sale.get("market", {})
    price = sale.get("price", {})

    return f"""
Domain Name: {data.get("name")}
Verified: {item.get("verified")}
DNS Address: {item.get("address")}
Owner: {owner.get("name", "Unknown")}
Marketplace: {market.get("name", "Unknown")}
Price: {int(price.get("value", "0")) / 10**price.get("decimals", 9)} {price.get("token_name", "TON")}
Trust Level: {item.get("trust")}
Collection: {item.get("collection", {}).get("name")}
Approved by: {', '.join(item.get("approved_by", []))}
Preview Image: {item.get("previews", [{}])[-1].get("url")}
Description: {item.get("collection", {}).get("description")}
"""


import json


def extract_nft_info(json_data):
    nft_info = []

    # Loop through each NFT item
    for item in json_data.get('nft_items', []):
        nft_details = {}

        # Extract the basic information of the NFT
        nft_details['nft_address'] = item.get('address')
        nft_details['nft_index'] = item.get('index')

        # Extract owner details
        owner = item.get('owner', {})
        nft_details['owner_name'] = owner.get('name')
        nft_details['owner_address'] = owner.get('address')
        nft_details['owner_is_scam'] = owner.get('is_scam')
        nft_details['owner_icon'] = owner.get('icon')

        # Extract collection details
        collection = item.get('collection', {})
        nft_details['collection_name'] = collection.get('name')
        nft_details['collection_address'] = collection.get('address')
        nft_details['collection_description'] = collection.get('description')

        # Extract sale details
        sale = item.get('sale', {})
        nft_details['sale_price_value'] = sale.get('price', {}).get('value')
        nft_details['sale_price_currency'] = sale.get('price', {}).get('currency_type')
        nft_details['sale_price_token_name'] = sale.get('price', {}).get('token_name')
        nft_details['sale_price_decimals'] = sale.get('price', {}).get('decimals')

        # Extract market details
        market = sale.get('market', {})
        nft_details['market_name'] = market.get('name')
        nft_details['market_is_scam'] = market.get('is_scam')

        # Extract previews
        previews = item.get('previews', [])
        nft_details['previews'] = [{'resolution': p.get('resolution'), 'url': p.get('url')} for p in previews]

        # Add the extracted details to the list
        nft_info.append(nft_details)

    return nft_info

#
# # Convert JSON string to dictionary
# json_data = json.loads(data)
#
# # Extract information
# extracted_info = extract_nft_info(json_data)
#
# # Print the extracted information
# for info in extracted_info:
#     print(json.dumps(info, indent=4))
