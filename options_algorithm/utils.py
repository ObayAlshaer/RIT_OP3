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

def place_order(ticker, order_type, quantity, price=None):
    url = f"{BASE_URL}/securities/{ticker}/orders"
    order_data = {
        "ticker": ticker,
        "type": order_type,
        "quantity": quantity,
    }
    if price is not None:
        order_data["price"] = price
        order_data["action"] = "LIMIT"
    else:
        order_data["action"] = "MARKET"

    try:
        response = session.post(url, json=order_data)
        response.raise_for_status()
        print(f"Order placed: {order_type} {quantity} {ticker} @ {price if price else 'MARKET'}")
    except requests.exceptions.RequestException as e:
        raise ApiException(f"Failed to place order: {e}")

def get_position(ticker):
    try:
        url = f"{BASE_URL}/securities/{ticker}/position"
        response = session.get(url)
        response.raise_for_status()
        position = response.json()
        return position.get("quantity", 0)
    except requests.exceptions.RequestException as e:
        raise ApiException(f"Failed to fetch position: {e}")