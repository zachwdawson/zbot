# -*- coding: utf-8 -*-

from enum import Enum
from typing import NamedTuple
import numpy as np
import pandas as pd


class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

class Card_Value(Enum):
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
    ACE = 14
    
    


class Card (NamedTuple('Card', [('value', Card_Value), ('suit', Suit)])):
        value: Card_Value
        suit: Suit
    
        def __eq__(self, other):
            return isinstance(other, Card) and (self.value == other.value) and (self.suit == other.suit)

class Board (NamedTuple(
    'Board', [('card1', Card), ('card2', Card), ('card3', Card), ('card4', Card), ('card5', Card)])):
        card1: Card
        card2: Card
        card3: Card
        card4: Card
        card5: Card
    

class Deck(object):
    
    def __init__(self, cards=None):
        self.cards = tuple(([Card(value, suit) for value in Card_Value for suit in Suit]) if cards is None else set(cards))

    def remove_card(self, remove):
        new_cards = [card for card in self.cards if card != remove]
        self.cards = tuple(new_cards)
    
    def get_next(self):
        next_card = self.cards[0]
        new_cards = [card for i, card in enumerate(self.cards) if i != 0]
        self.cards = tuple(new_cards)
        return next_card
    
    def get_random_next(self):
        card_chosen = np.random.randint(0,high=51)
        next_card = self.cards[card_chosen]
        new_cards = [card for i, card in enumerate(self.cards) if i != next_card]
        self.cards = tuple(new_cards)
        return next_card

    
        



