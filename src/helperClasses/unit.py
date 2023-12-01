from dataclasses import dataclass

@dataclass
class Unit:
    """
    Represents a trading unit(used in turtle terminology) with specific attributes related to a trading operation.

    This class is a data structure used to store information about a single trading unit, including its position type,
    entry price, start date and time, and optionally a list of previous prices.

    Attributes:
        pos_type (str): The position type of the trade ('long' or 'short').
        enter_price (float): The price at which the trade was entered.
        start_date (str): The start date of the trade.
        start_time (int): The start time of the trade.
        previous_prices (list, optional): A list of previous prices associated with the trade, defaults to None.
    """
    pos_type: str  # 'long' or 'short'
    enter_price: float
    enter_price_open: float
    start_date: str
    start_time: int
    previous_prices: list = None
