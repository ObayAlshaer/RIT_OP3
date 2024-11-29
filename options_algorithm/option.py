class Option:
    def __init__(self, option_type, strike_price, premium, quantity=100, is_short=False):
        self.option_type = option_type
        self.strike_price = strike_price
        self.premium = premium
        self.quantity = quantity
        self.is_short = is_short  

    def calculate_profit(self, market_price):
        if self.option_type == "CALL":
            if self.is_short:
                return self.premium * self.quantity - max(market_price - self.strike_price, 0) * self.quantity
            else:
                return max(market_price - self.strike_price, 0) * self.quantity - self.premium * self.quantity

        elif self.option_type == "PUT":
            if self.is_short:
                return self.premium * self.quantity - max(self.strike_price - market_price, 0) * self.quantity
            else:
                return max(self.strike_price - market_price, 0) * self.quantity - self.premium * self.quantity

        return 0

