from enum import Enum, auto
from dataclasses import dataclass

class CardColor(Enum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    WILD = auto()

class CardValue(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    # ... all numbers
    SKIP = auto()
    REVERSE = auto()
    DRAW_TWO = auto()
    WILD = auto()
    WILD_DRAW_FOUR = auto()

@dataclass
class Card:
    color: CardColor
    value: CardValue
    
    def __str__(self):
        return f"{self.color.name} {self.value.name}"
    
    def matches(self, other: 'Card') -> bool:
        """Check if this card can be played on another card."""
        return (self.color == other.color or 
                self.value == other.value or 
                self.color == CardColor.WILD)
