from typing import List
from .cards import Card

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: List[Card] = []
        
    def add_card(self, card: Card):
        """Add a card to the player's hand."""
        self.hand.append(card)
        
    def play_card(self, card_index: int) -> Card:
        """Play a card from the player's hand."""
        if card_index < 0 or card_index >= len(self.hand):
            raise IndexError("Invalid card index")
        return self.hand.pop(card_index)
        
    def has_playable_card(self, top_card: Card) -> bool:
        """Check if player has any card that can be played."""
        return any(card.matches(top_card) for card in self.hand)
        
    def __str__(self):
        return f"{self.name} ({len(self.hand)} cards)"
