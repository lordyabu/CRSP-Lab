from dataclasses import dataclass

@dataclass
class Unit:
    pos_type: str  # 'long' or 'short'
    enter_price: float
    start_date: str
    start_time: int
    previous_prices: list = None  # New attribute for storing previous prices
