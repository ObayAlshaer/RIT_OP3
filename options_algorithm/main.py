import signal
import requests
from time import sleep
from strategy import maximize_profit
from utils import get_tick, get_option_premiums
from exceptions import ApiException 
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = {"X-API-Key": "YEX15AVL"}
shutdown = False
BASE_URL = "http://rit.telfer.uottawa.ca:10019/v1"
SECURITY_TICKER = "RTM"

def initialize_sentiment_model():
    token = os.getenv("HF_TOKEN")  
    tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone', use_auth_token=token)
    model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3, use_auth_token=token)
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return nlp

def signal_handler(signum, frame):
    global shutdown
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    shutdown = True

signal.signal(signal.SIGINT, signal_handler)

news_text = "Stock market shows bullish sentiment as tech stocks continue to rise."

def main():
    nlp = initialize_sentiment_model()

    sentiment_result = nlp(news_text)
    print(f"Sentiment Analysis Result: {sentiment_result}")


    sentiment_label = sentiment_result[0]['label']
    print(f"Sentiment label: {sentiment_label}")  

    try:
        current_price = get_tick()
        print(f"Current Market Price: {current_price}")
    except Exception as e:
        print(f"Error fetching market price: {e}")
        return

    options = maximize_profit(current_price, news_text)
    
    call_option = options["call"]
    put_option = options["put"]
    
    try:
        place_order(
            ticker=SECURITY_TICKER,
            order_type="BUY",
            quantity=call_option.quantity,
            price=call_option.premium
        )

        place_order(
            ticker=SECURITY_TICKER,
            order_type="BUY",
            quantity=put_option.quantity,
            price=put_option.premium
        )
    except ApiException as e:
        print(f"Error placing trades: {e}")
        return

    print("Trades executed successfully!")

if __name__ == "__main__":
    main()
