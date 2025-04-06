import random
from typing import List
from .cards import Card, CardColor, CardValue

class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.discard_pile: List[Card] = []
        self._initialize_deck()
        
    def _initialize_deck(self):
        """Create a standard UNO deck with 108 cards."""
        # Add number cards
        for color in CardColor:
            if color == CardColor.WILD:
                continue
                
            # Add one zero per color
            self.cards.append(Card(color, CardValue.ZERO))
            
            # Add two of each number 1-9 per color
            for value in range(1, 10):
                self.cards.append(Card(color, CardValue(value)))
                self.cards.append(Card(color, CardValue(value)))
                
            # Add action cards (2 of each per color)
            for action in [CardValue.SKIP, CardValue.REVERSE, CardValue.DRAW_TWO]:
                self.cards.append(Card(color, action))
                self.cards.append(Card(color, action))
                
        # Add wild cards (4 of each)
        for _ in range(4):
            self.cards.append(Card(CardColor.WILD, CardValue.WILD))
            self.cards.append(Card(CardColor.WILD, CardValue.WILD_DRAW_FOUR))
            
        self.shuffle()
        
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
        
    def draw(self, count: int = 1) -> List[Card]:
        """Draw cards from the deck."""
        drawn = []
        for _ in range(count):
            if not self.cards:
                self._replenish_deck()
            drawn.append(self.cards.pop())
        return drawn
        
    def _replenish_deck(self):
        """Replenish deck from discard pile when empty."""
        if not self.discard_pile:
            raise ValueError("Cannot replenish deck - no cards left")
            
        # Keep the top card
        top_card = self.discard_pile.pop()
        self.cards = self.discard_pile
        self.discard_pile = [top_card]
        self.shuffle()
        
    def play_card(self, card: Card):
        """Place a card on the discard pile."""
        self.discard_pile.append(card)
        
    def top_card(self) -> Card:
        """Get the current top card on the discard pile."""
        return self.discard_pile[-1]
