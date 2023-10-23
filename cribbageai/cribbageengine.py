"""This is the main engine that handles running the game of cribbage.

A command line, REST, or other interface can be built on top of the main engine.

  cribbage_engine = CribbageEngine()
  cribbage_engine.new_game();

"""

__author__ = 'Jordan Reed'

from enum import Enum
from itertools import combinations
import logging
import random


CARDS_DEALT_IN_HAND = 6
HIGHEST_RUN_ALLOWED = 31


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

    def get_suit_display(self):
        """Gets the unicode character for the suite for display purposes."""
        suit_display = ""
        if self.suit == Suit.CLUB:
          suit_display = "♣"
        elif self.suit == Suit.DIAMOND:
          suit_display = "♦"
        elif self.suit == Suit.SPADE:
          suit_display = "♠"
        elif self.suit == Suit.HEART:
          suit_display = "♥"

        return suit_display

    def get_face_display(self):
        """Gets a character for the face value for display purposes."""
        face_display = ""
        if self.face == Face.ACE:
          face_display = "A"
        if self.face == Face.TWO:
          face_display = "2"
        if self.face == Face.THREE:
          face_display = "3"
        if self.face == Face.FOUR:
          face_display = "4"
        if self.face == Face.FIVE:
          face_display = "5"
        if self.face == Face.SIX:
          face_display = "6"
        if self.face == Face.SEVEN:
          face_display = "7"
        if self.face == Face.EIGHT:
          face_display = "8"
        if self.face == Face.NINE:
          face_display = "9"
        if self.face == Face.TEN:
          face_display = "10"
        if self.face == Face.JACK:
          face_display = "J"
        if self.face == Face.QUEEN:
          face_display = "Q"
        if self.face == Face.KING:
          face_display = "K"

        return face_display

    def get_display(self):
        """Gets a display that combines the face value and the suit."""
        return "%s%s" % (self.get_face_display(),self.get_suit_display())


    def __eq__(self, other):
        if not isinstance(other, PlayingCard):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.suit == other.suit and self.face == other.face

    def __lt__(self, other):
        if not isinstance(other, PlayingCard):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.face.value < other.face.value:
            return True
        elif self.face.value > other.face.value:
            return False
        elif self.suit.value < other.suit.value:
            return True
        else:
            return False

    def __hash__(self):
        return hash(str(self.suit) + str(self.face))

class CribbageGame:
    def __init__(self, base_deck, player_one, player_two):
        self._base_deck = base_deck
        self.game_deck = set(self._base_deck)
        self.player_one = player_one
        self.player_one_score = 0
        self.player_one_hand = set()
        self.player_one_run_hand = set()
        self.player_two = player_two
        self.player_two_score = 0
        self.player_two_hand = set()
        self.player_two_run_hand = set()
        self.crib = set()
        self.run = []
        self.go_player = 0
        self.start_card = set()
        self.crib_turn = 1 # player 1
        self.run_turn = 2 # player 2

    @staticmethod
    def get_cards_total_value(cards):
        """Get the total value of a set of cards. Most often used to calculate the
        runs total value.

        Args:
            run: a List of PlayingCard

        Returns:
            (int) the value of the list
        """

        cards_total = 0
        for card in cards:
            cards_total += card.value

        return cards_total

    def deal_cards(self):
        """Deals the two initial hands to the player.

        This will remove cards from game_deck and put them into player_one_hand
        and player_two_hand.
        """
        self.player_one_hand = set()
        self.player_two_hand = set()
        self.crib = set()

        for _ in range(CARDS_DEALT_IN_HAND):
            card = random.sample(sorted(self.game_deck), 1)[0]
            self.game_deck.remove(card)
            self.player_one_hand.add(card)

            card = random.sample(sorted(self.game_deck), 1)[0]
            self.game_deck.remove(card)
            self.player_two_hand.add(card)

        logging.info("Hands are dealt --")
        logging.info("P1 Hand: %s" % (cards_as_string(self.player_one_hand)))
        logging.info("P2 Hand: %s" % (cards_as_string(self.player_two_hand)))

    def discard_to_crib(self):
        self.player_one.discard_to_crib(self.player_one_hand, self.crib)
        self.player_two.discard_to_crib(self.player_two_hand, self.crib)
        logging.info("Discarded to Crib --")
        logging.info("P1 Hand: %s" % (cards_as_string(self.player_one_hand)))
        logging.info("P2 Hand: %s" % (cards_as_string(self.player_two_hand)))
        logging.info("Crib: %s" % (cards_as_string(self.crib)))

    def cut_start_card(self):
        card = random.sample(sorted(self.game_deck), 1)[0]
        self.game_deck.remove(card)
        self.start_card.add(card)
        logging.info("Start Card: %s" % (card.get_display()))

        ## If it's a jack, dealer gets 2 points
        if card.face == Face.JACK:
            if self.run_turn == 2:
                self.player_one_score += 1
                logging.info("Dealer Gets His Heels for +2: %s" % (self.player_one_score))
            else:
                self.player_two_score += 1
                logging.info("Dealer Gets His Heels for +2: %s" % (self.player_two_score))

        self.player_one_run_hand = set(self.player_one_hand)
        self.player_two_run_hand = set(self.player_two_hand)

    def is_more_run_cards(self):
        if not self.player_one_run_hand and not self.player_two_run_hand:
            return False
        else:
            return True

    def play_next_run_card(self):
        if self.is_more_run_cards():
            if self.run_turn == 1:
                active_run_player = self.player_one
                active_run_hand = self.player_one_run_hand
            else:
                active_run_player = self.player_two
                active_run_hand = self.player_two_run_hand

            ## Test if the player can play a card and stay under 31
            run_total = CribbageGame.get_cards_total_value(self.run);
            logging.info("Checking if player #%i can play against run %i"
              % (self.run_turn, run_total))

            can_play_card = False
            for card in active_run_hand:
                logging.debug("Player #%i run total [%i] + card %s [%i]"
                  % (self.run_turn, run_total, card.get_display(), card.value))

                if run_total + card.value <= HIGHEST_RUN_ALLOWED:
                    can_play_card = True

            if can_play_card:
                logging.info("Player #%i can play against run %i" % (self.run_turn, run_total))
                run_card = active_run_player.get_run_card(
                             active_run_hand, self.run, run_total)

                points_for_card = calculate_score_for_run_play(self.run, run_card)
                logging.info("Player #%i played %s for %i points against the run %s"
                  % (self.run_turn, run_card.get_display(), points_for_card,
                     cards_as_string(self.run)))


                active_run_hand.remove(run_card)
                self.run.append(run_card)

                logging.info("Player #%i played %s, the run is now %s"
                  % (self.run_turn, run_card.get_display(), cards_as_string(self.run)))

            else:
                logging.info("Player #%i cannot play against run %i" % (self.run_turn, run_total))
                # The active player cannot play.
                # If no one has said "Go" - the active player says "Go"
                if self.go_player == 0:
                    self.go_player = self.run_turn
                    logging.info("Player #%i call a Go" % (self.run_turn))
                    # The other player gets one point when Go happens.
                    if self.run_turn == 1:
                      self.player_two_score += 1
                      logging.info("Player #2 scores to total %i" % (self.player_two_score))
                    else:
                      self.player_one_score += 1
                      logging.info("Player #1 scores to total %i" % (self.player_one_score))

                # If someone has said "Go" and it was the other player
                # then reset the run
                elif self.go_player != self.run_turn:
                	self.run = []
                	self.go_player = 0

            # The last card gets one more point
            if not self.is_more_run_cards():
                if self.run_turn == 1:
                  self.player_one_score += 1
                  logging.info("Player #1 plays last card scores to total %i"
                    % (self.player_one_score))
                else:
                  self.player_two_score += 1
                  logging.info("Player #2 plays last card scores to total %i"
                    % (self.player_two_score))


            self.run_turn = 2 if self.run_turn == 1 else 1

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


    def new_game(self, player_one, player_two):
        return CribbageGame(self._base_deck, player_one, player_two)


## Static Helper Methods
def cards_as_string(cards):
    card_display_list = []
    for card in cards:
        card_display_list.append(card.get_display())

    return ','.join(card_display_list)

def calculate_score_for_run_play(run, run_card):
    """Calculates the score a player gets for playing a specific card onto the run.

    Args:
        run - a list of PlayingCard that represents the run
        run_card - a single PlayingCard that represents the players next play

    Returns:
    	(int) the score for the play

    Raises:
        TODO: Invalid Input errors
    """
    run_play_score = 0
    run_total = CribbageGame.get_cards_total_value(run)

    if run:
        # 2 points if you get 15 or 31 in the run
        if run_total + run_card.value == 15 or run_total + run_card.value == 31:
          run_play_score += 2

        # 2 points for every pair.  This is a combinatorial function
        total_pairs = 0
        pair_lookback = -1
        while len(run) >= abs(pair_lookback) and run[pair_lookback].face == run_card.face:
            total_pairs += 1
            pair_lookback -= 1

        # starting pythong 3.8 you can use math.comb
        if total_pairs == 1:
            run_play_score += 2
        elif total_pairs == 2:
            run_play_score += 6
        elif total_pairs == 3:
            run_play_score += 12

        # 1 point for each card in a sequence, even if it's out of order
        sequence_check_list = []
        for card in run:
            sequence_check_list.append(card.face.value)

        sequence_check_list.append(run_card.face.value)
        while len(sequence_check_list) >= 3:
            if _can_sort_values_to_sequence(sequence_check_list):
                run_play_score += len(sequence_check_list)
                del sequence_check_list[:]
            else:
                sequence_check_list.pop(0)

    return run_play_score

def calculate_score_for_hand(player_hand, start_card):
    hand_play_score = 0
    player_full_hand = player_hand.copy()

    ## Check for His Nob Before Appending the Start Card
    hand_play_score += _calculate_score_for_hand_his_nob(player_hand, start_card)

    ## Check for a flush and full flush before appending the start card
    is_flush = True
    temp_flush_suit = player_hand[0].suit
    for card in player_full_hand:
        if card.suit != temp_flush_suit:
            is_flush = False

    if is_flush:
        if temp_flush_suit == start_card.suit:
            hand_play_score += 5
        else:
            hand_play_score += 4

    player_full_hand.append(start_card)

    ## Find all combinations of cards that add up to 15
    for combination_size in range(2, len(player_full_hand)+1):
        combinations_set = list(combinations(player_full_hand, combination_size))
        for combo in combinations_set:
            cards_total_value = CribbageGame.get_cards_total_value(combo)
            if cards_total_value == 15:
              hand_play_score += 2

    ## Find all pairs, they each are 2 points
    ## Triples, Quadruples can be ignored, they are just combinations of pairs
    combinations_set = list(combinations(player_full_hand, 2))
    for combo in combinations_set:
      if combo[0].face == combo[1].face:
        hand_play_score += 2

    ## Find the runs, but don't count sub-runs.  Runs are between 3-5 cards. If the
    ## larger run of 4-5 is scored, subruns should be ignored.


    return hand_play_score

def _calculate_score_for_hand_his_nob(player_hand, start_card):
    """Calculates the amount of points a player earns for his nob

    Args:
      player_hand: a List of PlayerCard
      start_card: A single PlayerCard

    Returns:
      (int) value of points
    """
    hand_play_score = 0
    for card in player_hand:
      if card.face == Face.JACK and card.suit == start_card.suit:
        hand_play_score += 1

    return hand_play_score

def _can_sort_cards_to_sequence(cards):
    """Check if a list of values can be sorted into a sequence of cards
    Args:
        run: a List of Integer values

    Returns:
        (boolean) If the list can be uniquely sorted into a sequence

    """
    sequence_check_list = []
    for card in cards:
        sequence_check_list.append(card.face.value)

    sorted_nums = sorted(sequence_check_list)

    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] != sorted_nums[i - 1] + 1:
            return False

    return True

def _can_sort_values_to_sequence(nums):
    """Check if a list of values can be sorted into a sequence of cards
    Args:
        run: a List of Integer values

    Returns:
        (boolean) If the list can be uniquely sorted into a sequence

    """
    sorted_nums = sorted(nums)

    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] != sorted_nums[i - 1] + 1:
            return False

    return True