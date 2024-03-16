from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, RSI, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    
    @property
    def assets(self):
        """
        Assets involved in the strategy. Here, we're only trading QQQ.
        """
        return ["QQQ"]

    @property
    def interval(self):
        """
        Data interval used for the indicators. Using '1day' for daily analysis.
        """
        return "1day"

    def run(self, data):
        """
        Executes the trading logic at each interval to determine allocation.
        """
        # Fetch the closing prices, and calculate EMA, RSI, and MACD for QQQ
        qqq_ema = EMA("QQQ", data["ohlcv"], length=26)  # Long-term EMA
        qqq_rsi = RSI("QQQ", data["ohlcv"], length=14)  # Standard RSI period
        qqq_macd = MACD("QQQ", data["ohlcv"], fast=12, slow=26)  # MACD and signal line
        
        # Initialize the QQQ stake to 0
        qqq_stake = 0
        
        # Check if we have enough data points for our indicators
        if qqq_ema is not None and qqq_rsi is not None and qqq_macd is not None:
            # Logic to determine when to buy
            # Buy if EMA is trending upwards, RSI is below 70 (not overbought),
            # and the MACD line crossed above the signal line recently.
            if qqq_ema[-1] > qqq_ema[-2] and qqq_rsi[-1] < 70 and qqq_macd["MACD"][-1] > qqq_macd["signal"][-1]:
                qqq_stake = 1  # Full allocation to QQQ
            
            # You might add additional conditions for selling or reducing stake
            
        # Log the decision for debugging
        log(f"QQQ Allocation: {qqq_stake}")
        
        # Create and return TargetAllocation object with the decided allocation
        return TargetAllocation({"QQQ": qqq_stake})