# RIT_OP3
This project is a Python-based options strategy calculator and automated trading bot that uses sentiment analysis, 
market data, option pricing, and real-time trading to help users determine and execute the most profitable options strategies 
based on current market conditions.

## Overview

The program employs two primary strategies for calculating profits: **Straddle** and **Strangle**. 
The strategy choice is influenced by sentiment analysis of a given news text, using a pre-trained **FinBERT** model 
to determine whether the sentiment is positive, neutral, or negative. Based on the sentiment, the program chooses 
whether to implement a **long** or **short** version of the strategies.

Additionally, the program can **automatically execute trades** in the RIT trading simulator, enabling seamless integration 
from analysis to execution.

### Key Features:
1. **Sentiment Analysis with FinBERT** - Utilizes FinBERT, a model fine-tuned for financial text sentiment analysis.
2. **Straddle and Strangle Option Strategies** - Calculates profit for different option strategies based on market moves.
3. **Market Data Integration** - Retrieves market data such as the current price and option premiums from the RIT API.
4. **Automated Trading Execution** - Places orders directly in the RIT trading simulator based on calculated strategies.
5. **Profit Calculation** - Calculates and prints the profit for both call and put options, for long and short strategies.

## Components of the Project

### 1. `main.py`

The entry point of the program. It fetches the current market price and applies the option strategies based on the news sentiment. It calculates the potential profit for each strategy, determines the best strategy, and optionally executes trades.

- Fetches the current market price.
- Analyzes news sentiment using FinBERT.
- Chooses the best strategy (Straddle or Strangle) based on sentiment and profitability.
- Displays the profit for both call and put options.
- Automatically places orders in the RIT trading simulator.

### 2. `option.py`

Defines the `Option` class that represents both call and put options. It includes a method `calculate_profit` that calculates the profit for an option based on whether it is a long or short position.

- `Option` class initializes with type (CALL or PUT), strike price, premium, and quantity.
- The `calculate_profit` method computes the profit for either a call or put option based on the market price.

### 3. `sentiment.py`

Handles the sentiment analysis by using the **FinBERT** model to classify the sentiment of a given news text as positive, negative, or neutral. This sentiment influences the option strategy selection.

- Loads the **FinBERT** model from the `yiyanghkust/finbert-tone` pretrained model.
- The `get_sentiment` function classifies the sentiment into one of three categories: positive, negative, or neutral.

### 4. `strategy.py`

Contains the main logic for the two option strategies: **Straddle** and **Strangle**. Each strategy has methods for calculating the profit based on market moves and whether the position is long or short.

- **Straddle Strategy**: Buys a call and put option with the same strike price.
- **Strangle Strategy**: Buys a call and put option with different strike prices, typically 5 points apart.
- Both strategies have methods for `long` (buying options) and `short` (selling options) positions.
- `maximize_profit` function uses sentiment analysis and profitability calculations to determine which strategy to choose.

### 5. `utils.py`

Contains utility functions for interacting with the RIT trading simulator API to fetch market data, retrieve option premiums, and execute trades. New functionality includes the ability to place orders and fetch current positions.

- `get_tick`: Fetches the current market price (tick) from the RIT API.
- `get_option_premiums`: Fetches the current call and put premiums for a given ticker.
- `place_order`: Places market or limit orders for a specified ticker in the RIT trading simulator.
- `get_position`: Retrieves the current position for a specific ticker.

### 6. `exceptions.py`

Defines custom exceptions for handling API-related errors in the program.

## Automated Trading Integration

The program can now directly execute trades in the RIT trading simulator based on the calculated strategies. 
Using the `place_order` and `get_position` functions, it can:

1. Fetch current market conditions and option premiums.
2. Choose the optimal strategy based on sentiment and profitability.
3. Execute trades automatically for both long and short positions.

### Example Workflow:

- Fetch the current tick and option premiums.
- Analyze news sentiment.
- Select the best strategy (e.g., Long Straddle).
- Place orders for the call and put options at the calculated strike prices.

### Example Trade Execution Code:

# Example usage of automated trading:
from utils import place_order, get_position

# Placing a market order for 10 CALL options
place_order("RTM", "BUY", quantity=10)

# Checking the current position for RTM
position = get_position("RTM")
print(f"Current Position for RTM: {position}")

### Straddle Strategy
In the **Straddle** strategy, the trader buys a call option and a put option with the same strike price and expiration date. The goal is to profit from large price movements, either up or down.

- If the stock price moves significantly in either direction, the trader profits from one of the options (either the call or the put).
- The `Straddle` class defines both long and short versions of this strategy. A long straddle profits when the stock price moves significantly in either direction. A short straddle profits when the price stays near the strike price.

### Strangle Strategy
The **Strangle** strategy is similar to the straddle but uses different strike prices for the call and put options. A typical strangle strategy might involve buying a call option with a strike price above the current stock price and a put option with a strike price below the current stock price.

- The aim is to profit from large price movements in either direction, but the options are cheaper than a straddle since they are out of the money.
- The `Strangle` class also defines long and short positions for the strategy.

### Sentiment Analysis with FinBERT
The **FinBERT** model is used to determine the sentiment of a given news text. The sentiment influences whether the strategy will be long or short.

- If the sentiment is **positive**, the program opts for long positions on the best strategy (either long straddle or long strangle).
- If the sentiment is **negative**, the program opts for short positions (either short straddle or short strangle).
- If the sentiment is **neutral**, no adjustments are made to the strategy.

### Maximizing Profit
The `maximize_profit` function calculates the profit for both straddle and strangle strategies and selects the best-performing one. It then applies the sentiment analysis results to determine whether to go long or short on the selected strategy.

## How to Run the Program

### Requirements

Before running the program, ensure the following dependencies are installed:

- Python 3.x
- `requests` for API interaction.
- `torch` and `transformers` for sentiment analysis with FinBERT.

You can install the required dependencies using pip:

```bash
pip install requests torch transformers
```

### Running the Program

1. Make sure the external API that provides the market data is running at `http://localhost:9999`.
2. Save the files (`main.py`, `option.py`, `sentiment.py`, `strategy.py`, `utils.py`, `exceptions.py`) in the same directory.
3. Run the `main.py` file:

```bash
python main.py
```

### Example Output

```bash
Current Market Price: 100
Sentiment Analysis Result: positive
Call Option Profit: $200.00
Put Option Profit: $50.00
Total Strategy Profit: $250.00
```

## Conclusion

This program helps to determine the best options strategy (Straddle or Strangle) based on market data and sentiment analysis, maximizing the potential profit. It can be extended with more advanced strategies, more complex sentiment analysis, or integration with other market data sources.

