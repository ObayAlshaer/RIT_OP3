import requests
from exceptions import ApiException  

BASE_URL = "http://localhost:9999/v1"
API_KEY = {"X-API-Key": "K5X4BO4C"}

session = requests.Session()
session.headers.update(API_KEY)

def get_tick():
    try:
        resp = session.get(f"{BASE_URL}/case")
        resp.raise_for_status()
        case = resp.json()
        return case["tick"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get tick: {e}")

def get_option_premiums():
    try:
        resp = session.get(f"{BASE_URL}/option_premiums/RTM")
        resp.raise_for_status()
        premiums = resp.json()
        call_premium = premiums["call"]
        put_premium = premiums["put"]
        return call_premium, put_premium
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get option premiums: {e}")

