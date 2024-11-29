import signal
import requests
from time import sleep
from strategy import maximize_profit
from utils import get_tick, get_option_premiums
from exceptions import ApiException 

API_KEY = {"X-API-Key": "K5X4BO4C"}
shutdown = False
BASE_URL = "http://localhost:9999/v1"
SECURITY_TICKER = "RTM"


def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True

signal.signal(signal.SIGINT, signal_handler)


news_text = "Stock market shows bullish sentiment as tech stocks continue to rise."


def main():
    try:
        current_price = get_tick()  
        print(f"Current Market Price: {current_price}")
    except Exception as e:
        print(f"Error fetching market price: {e}")
        return


    options = maximize_profit(current_price, news_text)


    call_profit = options["call"].calculate_profit(current_price)
    put_profit = options["put"].calculate_profit(current_price)

    print(f"Call Option Profit: ${call_profit:.2f}")
    print(f"Put Option Profit: ${put_profit:.2f}")

    # Total profit
    total_profit = call_profit + put_profit
    print(f"Total Strategy Profit: ${total_profit:.2f}")

if __name__ == "__main__":
    main()

