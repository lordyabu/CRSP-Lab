from dataclasses import dataclass

@dataclass
class Trade:
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

    @property
    def datetime(self):
        # Concatenating start_date and start_time for a datetime representation
        return f"{self.start_date} {self.start_time}-{self.end_date} {self.end_time}"

    @property
    def pnl(self):
        if self.trade_type == 'long':
            return (self.exit_price - self.enter_price) * self.leverage
        elif self.trade_type == 'short':
            return (self.enter_price - self.exit_price) * self.leverage
        else:
            raise ValueError("Trade type must be either 'long' or 'short'")


    @property
    def pnl_percent(self):
        # PnL as a percentage of the enter price
        return (self.pnl / self.enter_price) * 100

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
        if not isinstance(self.trade_type, str):
            raise TypeError("trade_type must be a string")
        if not isinstance(self.leverage, (int, float)):
            raise TypeError("leverage must be a number")
        if not isinstance(self.strategy, str):
            raise TypeError("Strategy must be a string")

        if self.trade_type not in ['long', 'short']:
            raise ValueError("Trade type must be either 'long' or 'short'")
