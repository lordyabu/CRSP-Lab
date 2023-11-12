from dataclasses import dataclass

@dataclass
class Unit:
    pos_type: str
    enter_price: float
    start_date: str
    start_time: int