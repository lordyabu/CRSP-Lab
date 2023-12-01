from dataclasses import dataclass

@dataclass
class Trade:
    """
    Represents a trade with various details such as identifiers, strategy, dates, prices, and trade type.

    This class uses the dataclass decorator for simplified attribute management and includes methods for
    calculating profit and loss and its percentage. It also performs type validation for each attribute.

    Attributes:
        identifier (str): Unique identifier for the trade.
        time_period (str): Time period of the trade.
        strategy (str): Trading strategy used.
        symbol (str): Stock symbol.
        start_date (str): Start date of the trade.
        end_date (str): End date of the trade.
        start_time (int): Start time of the trade.
        end_time (int): End time of the trade.
        enter_price (float): Price at which the trade was entered.
        exit_price (float): Price at which the trade was exited.
        trade_type (str): Type of trade - 'long' or 'short'.
        leverage (float): Leverage used in the trade, defaults to 1.
        previous_prices (list): Previous 50 prices, optional.

    Properties:
        datetime: Returns a string representation combining start and end dates with times.
        pnl: Calculates the profit or loss of the trade.
        pnl_percent: Calculates the profit or loss percentage relative to the enter or exit price.

    Methods:
        __repr__: Returns a formatted string representation of the Trade instance.
        __post_init__: Validates the types of the attributes and raises appropriate errors.
    """
    identifier: str
    time_period: str
    strategy: str
    symbol: str
    start_date: str
    end_date: str
    start_time: int
    end_time: int
    enter_price: float
    exit_price: float
    enter_price_open: float
    exit_price_open: float
    trade_type: str  # 'long' or 'short'
    transaction_cost_pct: float
    transaction_cost_dollar: float
    leverage: float = 1
    previous_prices: list = None

    @property
    def datetime(self):
        # Concatenating start_date and start_time for a datetime representation
        return f"{self.start_date} {self.start_time}-{self.end_date} {self.end_time}"

    @property
    def pnl(self):
        if self.trade_type == 'long':
            return (self.exit_price - self.enter_price) * self.leverage
        elif self.trade_type == 'short':
            # As shorts exit_price is basically a long entry
            return (self.enter_price - self.exit_price) * self.leverage
        else:
            raise ValueError("Trade type must be either 'long' or 'short'")


    @property
    def pnl_percent(self):
        # PnL as a percentage of the enter price
        if self.trade_type == 'long':
            return (self.pnl / self.enter_price) * 100
        elif self.trade_type == 'short':
            return (self.pnl / self.exit_price) * 100
        else:
            raise ValueError("Trade type must be either 'long' or 'short'")

    def __repr__(self):
        return (f"Trade(identifier={self.identifier}, time_period={self.time_period}, strategy={self.strategy}, symbol={self.symbol}, start_date={self.start_date}, "
                f"end_date={self.end_date}, start_time={self.start_time}, end_time={self.end_time}, "
                f"enter_price={self.enter_price}, exit_price={self.exit_price}, trade_type={self.trade_type}, "
                f"leverage={self.leverage}, pnl={self.pnl}, pnl_percent={self.pnl_percent:.2f}%)")

    def __post_init__(self):
        if not isinstance(self.identifier, str):
            raise TypeError("Identifier must be a string")
        if not isinstance(self.time_period, str):
            raise TypeError("Time Period must be a string")
        if not isinstance(self.symbol, str):
            raise TypeError("symbol must be a string")
        if not isinstance(self.start_date, str):
            raise TypeError("start_date must be a string")
        if not isinstance(self.end_date, str):
            raise TypeError("end_date must be a string")
        if not isinstance(self.start_time, int):
            raise TypeError("start_time must be an integer")
        if not isinstance(self.end_time, int):
            raise TypeError("end_time must be an integer")
        if not isinstance(self.enter_price, (int, float)):
            raise TypeError("enter_price must be a number")
        if not isinstance(self.exit_price, (int, float)):
            raise TypeError(f"exit_price must be a number: {self.exit_price}")
        if not isinstance(self.enter_price_open, (int, float)):
            raise TypeError("enter_price_open must be a number")
        if not isinstance(self.exit_price_open, (int, float)):
            raise TypeError(f"exit_price_open must be a number: {self.exit_price_open}")
        if not isinstance(self.trade_type, str):
            raise TypeError("trade_type must be a string")
        if not isinstance(self.transaction_cost_pct, (int, float)):
            raise TypeError(f"transaction_cost_pct must be a number: {self.transaction_cost_dollar}")
        if not isinstance(self.transaction_cost_dollar, (int, float)):
            raise TypeError(f"transaction_cost_dollar must be a number: {self.transaction_cost_dollar}")
        if not isinstance(self.leverage, (int, float)):
            raise TypeError("leverage must be a number")
        if not isinstance(self.strategy, str):
            raise TypeError("Strategy must be a string")

        if self.trade_type not in ['long', 'short']:
            raise ValueError("Trade type must be either 'long' or 'short'")

        if self.previous_prices is not None:
            if not isinstance(self.previous_prices, list):
                raise TypeError("previous_prices must be a list")