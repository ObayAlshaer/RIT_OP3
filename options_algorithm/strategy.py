from option import Option
from utils import get_option_premiums
from sentiment import get_sentiment

class Straddle:
    def __init__(self, current_price, call_premium, put_premium):
        self.strike_price = current_price
        self.call_option = Option(option_type="CALL", strike_price=self.strike_price, premium=call_premium)
        self.put_option = Option(option_type="PUT", strike_price=self.strike_price, premium=put_premium)

    def long(self):

        return {
            "call": self.call_option,
            "put": self.put_option
        }

    def short(self):
        return {
            "call": Option(option_type="CALL", strike_price=self.strike_price, premium=-self.call_option.premium),
            "put": Option(option_type="PUT", strike_price=self.strike_price, premium=-self.put_option.premium)
        }

    def calculate_profit(self, market_move, is_long=True):

        if is_long:
            return (self.call_option.calculate_profit(market_move) + self.put_option.calculate_profit(-market_move))
        else:
            return (self.call_option.calculate_profit(-market_move) + self.put_option.calculate_profit(market_move))


class Strangle:
    def __init__(self, current_price, call_premium, put_premium):
        self.call_strike = current_price + 5
        self.put_strike = current_price - 5
        self.call_option = Option(option_type="CALL", strike_price=self.call_strike, premium=call_premium)
        self.put_option = Option(option_type="PUT", strike_price=self.put_strike, premium=put_premium)

    def long(self):

        return {
            "call": self.call_option,
            "put": self.put_option
        }

    def short(self):
        return {
            "call": Option(option_type="CALL", strike_price=self.call_strike, premium=-self.call_option.premium),
            "put": Option(option_type="PUT", strike_price=self.put_strike, premium=-self.put_option.premium)
        }

    def calculate_profit(self, market_move, is_long=True):
 
        if is_long:
            return (self.call_option.calculate_profit(market_move) + self.put_option.calculate_profit(-market_move))
        else:
            return (self.call_option.calculate_profit(-market_move) + self.put_option.calculate_profit(market_move))


def maximize_profit(current_price, news_text):

    sentiment = get_sentiment(news_text)
    print(f"Sentiment Analysis Result: {sentiment}")

    call_premium, put_premium = get_option_premiums()

    straddle = Straddle(current_price, call_premium, put_premium)
    strangle = Strangle(current_price, call_premium, put_premium)

    upside_move = current_price + 10
    downside_move = current_price - 10

    long_straddle_profit = straddle.calculate_profit(upside_move, is_long=True) + straddle.calculate_profit(downside_move, is_long=True)
    short_straddle_profit = straddle.calculate_profit(upside_move, is_long=False) + straddle.calculate_profit(downside_move, is_long=False)

    long_strangle_profit = strangle.calculate_profit(upside_move, is_long=True) + strangle.calculate_profit(downside_move, is_long=True)
    short_strangle_profit = strangle.calculate_profit(upside_move, is_long=False) + strangle.calculate_profit(downside_move, is_long=False)

    strategies = {
        "long_straddle": long_straddle_profit,
        "short_straddle": short_straddle_profit,
        "long_strangle": long_strangle_profit,
        "short_strangle": short_strangle_profit
    }

    best_strategy = max(strategies, key=strategies.get)


    if sentiment == "positive":
        if best_strategy == "short_straddle" or best_strategy == "short_strangle":
            best_strategy = best_strategy.replace("short", "long")
    elif sentiment == "negative":
        if best_strategy == "long_straddle" or best_strategy == "long_strangle":
            best_strategy = best_strategy.replace("long", "short")

    if best_strategy == "long_straddle":
        return straddle.long()
    elif best_strategy == "short_straddle":
        return straddle.short()
    elif best_strategy == "long_strangle":
        return strangle.long()
    else:
        return strangle.short()
