import requests
import os
from backend.utils.logger import logger

BASE_URL = os.getenv("TON_API_BASE", "https://tonapi.io")
TOKEN = os.getenv("TON_API_TOKEN")


def tonapi_get(endpoint: str, params=None):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }
    print(TOKEN)
    url = f"{BASE_URL}{endpoint}"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"[TON API] Non-200 response for {url}: {response.status_code} {response.text}")
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }

    except requests.exceptions.Timeout:
        logger.error(f"[TON API] Timeout occurred when accessing {url}")
        return {"error": True, "message": "Timeout"}

    except requests.exceptions.RequestException as e:
        logger.error(f"[TON API] Request failed: {e}")
        return {"error": True, "message": str(e)}
