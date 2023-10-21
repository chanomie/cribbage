"""This is the main engine that handles running the game of cribbage.

A command line, REST, or other interface can be built on top of the main engine.

  cribbage_engine = CribbageEngine()
  cribbage_engine.new_game();
  
"""

__author__ = 'Jordan Reed'

from enum import Enum
import logging

class Suit(Enum):
    """Provides the four suits of cards"""
    CLUB = 1
    DIAMOND = 2
    SPADE = 3
    HEART = 4


class Face(Enum):
    """Provides the thirteen card faces."""
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class PlayingCard:
    """
    A playing card has a Suit, Face, and Value.
    The Value is specific to cribbage where face cards are worth 10 points.
    """
    def __init__(self, suit: Suit, face: Face, value: int):
        self.suit = suit
        self.face = face
        self.value = value


class CribbageEngine:
    """
    Represents the main engine for storage and manipulation of the state of the game.
  
    Attributes
    ----------
    _base_deck : internal immutable representation of the 52 card deck
    deck : representation of a deck that may be shuffled and used for play
  
    Methods
    -------
    new_game:
        re-initializes the game and deck
    """
    def __init__(self):
        init_deck = set()
        for suit in Suit:
            init_deck.add(PlayingCard(suit, Face.ACE, 1))
            init_deck.add(PlayingCard(suit, Face.TWO, 2))
            init_deck.add(PlayingCard(suit, Face.THREE, 3))
            init_deck.add(PlayingCard(suit, Face.FOUR, 4))
            init_deck.add(PlayingCard(suit, Face.FIVE, 5))
            init_deck.add(PlayingCard(suit, Face.SIX, 6))
            init_deck.add(PlayingCard(suit, Face.SEVEN, 7))
            init_deck.add(PlayingCard(suit, Face.EIGHT, 8))
            init_deck.add(PlayingCard(suit, Face.NINE, 9))
            init_deck.add(PlayingCard(suit, Face.TEN, 10))
            init_deck.add(PlayingCard(suit, Face.JACK, 10))
            init_deck.add(PlayingCard(suit, Face.QUEEN, 10))
            init_deck.add(PlayingCard(suit, Face.KING, 10))
      
        self._base_deck = frozenset(init_deck)
        logging.info("CribbageEngine initialized")
    
        
    def new_game(self):
        self.deck = set(self._base_deck)
