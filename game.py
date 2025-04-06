from typing import List
from .deck import Deck
from .player import Player
from .cards import Card, CardColor
from .exceptions import InvalidMoveException

class UNOGame:
    def __init__(self, player_names: List[str]):
        self.deck = Deck()
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0
        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise
        self.game_over = False
        
        # Deal initial cards
        for _ in range(7):
            for player in self.players:
                player.add_card(self.deck.draw()[0])
                
        # Start with a non-wild card
        while True:
            top_card = self.deck.draw()[0]
            if top_card.color != CardColor.WILD:
                self.deck.play_card(top_card)
                break
    
    def next_player(self):
        """Move to the next player based on game direction."""
        self.current_player_index = (
            self.current_player_index + self.direction) % len(self.players)
    
    def play_turn(self, player_index: int, card_index: int, new_color: CardColor = None):
        """Execute a player's turn."""
        if self.game_over:
            raise InvalidMoveException("Game is already over")
            
        if player_index != self.current_player_index:
            raise InvalidMoveException("Not your turn")
            
        player = self.players[player_index]
        top_card = self.deck.top_card()
        played_card = player.hand[card_index]
        
        if not played_card.matches(top_card):
            raise InvalidMoveException("Card doesn't match the top card")
            
        # Handle special cards
        if played_card.value == CardValue.SKIP:
            self.next_player()
        elif played_card.value == CardValue.REVERSE:
            self.direction *= -1
        elif played_card.value == CardValue.DRAW_TWO:
            next_player = self.players[self.current_player_index]
            next_player.add_cards(self.deck.draw(2))
            self.next_player()
            
        # Handle wild cards
        if played_card.color == CardColor.WILD:
            if not new_color:
                raise InvalidMoveException("Must choose a color for wild card")
            played_card.color = new_color
            
        # Play the card and move to next player
        self.deck.play_card(player.play_card(card_index))
        self.next_player()
        
        # Check for winner
        if len(player.hand) == 0:
            self.game_over = True
            return f"{player.name} wins!"
            
        return "Turn completed successfully"
    
    def draw_card(self, player_index: int):
        """Handle a player drawing a card."""
        if player_index != self.current_player_index:
            raise InvalidMoveException("Not your turn")
            
        player = self.players[player_index]
        card = self.deck.draw()[0]
        player.add_card(card)
        
        # If the drawn card is playable, player can choose to play it
        if card.matches(self.deck.top_card()):
            return card
        else:
            self.next_player()
            return None
    
    def get_game_state(self, for_player: int = None):
        """Return the current game state."""
        return {
            "current_player": self.current_player_index,
            "top_card": str(self.deck.top_card()),
            "direction": "clockwise" if self.direction == 1 else "counter-clockwise",
            "player_hand": [
                str(card) for card in self.players[for_player].hand
            ] if for_player is not None else None,
            "players": [str(player) for player in self.players],
            "game_over": self.game_over
        }
