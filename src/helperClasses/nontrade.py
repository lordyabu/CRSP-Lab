from dataclasses import dataclass

@dataclass
class NonTrade:
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
    trade_type: str  # 'long' or 'short'
    leverage: float = 1
    previous_prices: list = None

    @property
    def datetime(self):
        # Concatenating start_date and start_time for a datetime representation
        return "NA"

    @property
    def pnl(self):
        return "NA"


    @property
    def pnl_percent(self):
        return "NA"

    def __repr__(self):
        return "NA"

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
        if not isinstance(self.start_time, str):
            raise TypeError("start_time must be a string")
        if not isinstance(self.end_time, str):
            raise TypeError("end_time must be a string")
        if not isinstance(self.enter_price, (int, float)):
            raise TypeError("enter_price must be a number")
        if not isinstance(self.exit_price, str):
            raise TypeError(f"exit_price must be a string: {self.exit_price}")
        if not isinstance(self.trade_type, str):
            raise TypeError("trade_type must be a string")
        if not isinstance(self.leverage, (int, float)):
            raise TypeError("leverage must be a number")
        if not isinstance(self.strategy, str):
            raise TypeError("Strategy must be a string")

        if self.trade_type not in ['NA']:
            raise ValueError("Trade type must be NA")

        if self.previous_prices is not None:
            if not isinstance(self.previous_prices, list):
                raise TypeError("previous_prices must be a list")