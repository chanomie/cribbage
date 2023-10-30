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

        return {
            Face.ACE: "A",
            Face.TWO: "2",
            Face.THREE: "3",
            Face.FOUR: "4",
            Face.FIVE: "5",
            Face.SIX: "6",
            Face.SEVEN: "7",
            Face.EIGHT: "8",
            Face.NINE: "9",
            Face.TEN: "10",
            Face.JACK: "J",
            Face.QUEEN: "Q",
            Face.KING: "K",
          }.get(self.face)

    def get_display(self):
        """Gets a display that combines the face value and the suit."""
        return f"{self.get_face_display()}{self.get_suit_display()}"


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

        if self.face.value > other.face.value:
            return False

        if self.suit.value < other.suit.value:
            return True

        return False

    def __hash__(self):
        return hash(str(self.suit) + str(self.face))



class CribbageGame:
    """Holds the state information for a game of cribbage.

    Attributes:
        game_deck: A set of PlayingCards still in the deck for the game.
    """
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
        self.start_card = None
        self.crib_turn = 0
        self.run_turn = 0

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
        self.game_deck = set(self._base_deck)

        if self.crib_turn in (0, 2):
            self.crib_turn = 1
            self.run_turn = 2
        else:
            self.crib_turn = 2
            self.run_turn = 1


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
        logging.info("P1 Hand: %s", cards_as_string(self.player_one_hand))
        logging.info("P2 Hand: %s", cards_as_string(self.player_two_hand))

    def discard_to_crib(self):
        """Allows both players to pick two cards to put into the crib."""
        crib_cards = self.player_one.discard_to_crib(set(self.player_one_hand))
        for crib_card in crib_cards:
            self.crib.add(crib_card)
            self.player_one_hand.remove(crib_card)

        crib_cards = self.player_two.discard_to_crib(set(self.player_two_hand))
        for crib_card in crib_cards:
            self.crib.add(crib_card)
            self.player_two_hand.remove(crib_card)

        logging.info("Discarded to Crib --")
        logging.info("P1 Hand: %s", cards_as_string(self.player_one_hand))
        logging.info("P2 Hand: %s", cards_as_string(self.player_two_hand))
        logging.info("Crib: %s", cards_as_string(self.crib))

    def cut_start_card(self):
        """Picks a random start card and check for his heels (2 points to dealer)"""
        card = random.sample(sorted(self.game_deck), 1)[0]
        self.game_deck.remove(card)
        self.start_card = card
        logging.info("Start Card: %s", card.get_display())

        ## If it's a jack, dealer gets 2 points
        if card.face == Face.JACK:
            if self.run_turn == 2:
                self.player_one_score += 1
                logging.info("Dealer Gets His Heels for +2: %s", self.player_one_score)
            else:
                self.player_two_score += 1
                logging.info("Dealer Gets His Heels for +2: %s", self.player_two_score)

        self.player_one_run_hand = set(self.player_one_hand)
        self.player_two_run_hand = set(self.player_two_hand)

    def is_more_run_cards(self):
        """Checks if either player has more cards in their run hand to play.
        Returns:
          (boolean): If there are cards left to play
        """
        if not self.player_one_run_hand and not self.player_two_run_hand:
            return False

        return True

    def play_next_run_card(self):
        """Plays the next run card on the current game.

        This method will execute the next run card and update the state of the game.
        If there is no way to play a run card, then it will exit.

        Returns:
            (map): results of the play
              run_turn: player number
              is_go: is it a "go"
              card_played: the card played
              run_total: the run total
              points_earned: the points earned.
       Raises:
            RuntimeError: if there are no more cards to play.  Check first using
              the is_more_run_cards method.
        """
        if not self.is_more_run_cards():
            raise RuntimeError("Cannot play if there are no more cards.")

        # Tracks the result of the play
        run_play_result = {}

        # Set the following method variables for the run
        # active_run_player - the AI for the active player
        # active_run_hand - the active player's hand
        run_play_result["run_turn"] = self.run_turn
        run_play_result["points_earned"] = 0
        if self.run_turn == 1:
            active_run_player = self.player_one
            active_run_hand = self.player_one_run_hand
        else:
            active_run_player = self.player_two
            active_run_hand = self.player_two_run_hand

        ## Test if the player can play a card and stay under 31
        run_total = CribbageGame.get_cards_total_value(self.run)
        logging.info("Checking if player #%i can play against run %i",
          self.run_turn, run_total)

        if self._can_play_card(active_run_hand):
            result = self._play_run_card(active_run_player, active_run_hand)
            run_play_result["is_go"] = False
            run_play_result["card_played"] = result[0]
            run_play_result["points_earned"] += result[1]
        else:
            run_play_result["is_go"] = True
            self._play_call_go()


        # The last card gets one more point
        if not self.is_more_run_cards():
            if self.run_turn == 1:
                self.player_one_score += 1
                logging.info("Player #1 plays last card scores to total %i",
                  (self.player_one_score))
            else:
                self.player_two_score += 1
                logging.info("Player #2 plays last card scores to total %i",
                  (self.player_two_score))


        self.run_turn = 2 if self.run_turn == 1 else 1
        run_play_result["run_total"] = CribbageGame.get_cards_total_value(self.run)
        return run_play_result

    def _can_play_card(self, active_run_hand):
        """Checks if the hand has a card it is able to play.
        It must stay under the maximum of 31.
        """
        can_play_card = False
        run_total = CribbageGame.get_cards_total_value(self.run)
        logging.info("Checking if player #%i can play against run %i",
          self.run_turn, run_total)

        for card in active_run_hand:
            logging.debug("Player #%i run total [%i] + card %s [%i]",
              self.run_turn, run_total, card.get_display(), card.value)

            if run_total + card.value <= HIGHEST_RUN_ALLOWED:
                can_play_card = True

        return can_play_card

    def _play_run_card(self, active_run_player, active_run_hand):
        """Plays a card from the player onto the run.

        Args:
            active_run_player: the CribbagePlayer who plays
            active_run_hand: the hand of cards the player has left
        Returns:
            (PlayingCard) the card played
            (int) The points earned for the card
        """
        run_total = CribbageGame.get_cards_total_value(self.run)
        logging.info("Player #%i can play against run %i",
          self.run_turn, run_total)

        run_card = active_run_player.get_run_card(
                     active_run_hand, self.run, run_total)

        points_for_card = calculate_score_for_run_play(self.run, run_card)
        logging.info("Player #%i played %s for %i points against the run %s",
          self.run_turn, run_card.get_display(), points_for_card,
          cards_as_string(self.run))

        if self.run_turn == 1:
            self.player_two_score += points_for_card
            logging.info("Player #2 scores to total %i", self.player_two_score)
        else:
            self.player_one_score += points_for_card
            logging.info("Player #1 scores to total %i", self.player_one_score)

        active_run_hand.remove(run_card)
        self.run.append(run_card)

        logging.info("Player #%i played %s, the run is now %s",
          self.run_turn, run_card.get_display(), cards_as_string(self.run))

        return run_card, points_for_card

    def _play_call_go(self):
        run_total = CribbageGame.get_cards_total_value(self.run)
        logging.info("Player #%i cannot play against run %i",
          self.run_turn, run_total)

        # The active player cannot play.
        # If no one has said "Go" - the active player says "Go"
        if self.go_player == 0:
            self.go_player = self.run_turn
            logging.info("Player #%i call a Go", self.run_turn)
            # The other player gets one point when Go happens.
            if self.run_turn == 1:
                self.player_two_score += 1
                logging.info("Player #2 scores to total %i", self.player_two_score)
            else:
                self.player_one_score += 1
                logging.info("Player #1 scores to total %i", self.player_one_score)

        # If someone has said "Go" and it was the other player
        # then reset the run
        elif self.go_player != self.run_turn:
            self.run = []
            self.go_player = 0


    def score_pone_hand(self):
        """Sums up the score for the pone player."""
        hand_score = 0
        if self.crib_turn == 1:
            hand_score = calculate_score_for_hand(list(self.player_two_hand), self.start_card)

            self.player_two_score += hand_score
        else:
            hand_score = calculate_score_for_hand(list(self.player_two_hand), self.start_card)

            self.player_one_score += hand_score

        return hand_score

    def score_dealer_hand(self):
        """Sums up the score for the dealer player."""
        hand_score = 0
        if self.crib_turn == 2:
            hand_score = calculate_score_for_hand(list(self.player_two_hand), self.start_card)

            self.player_two_score += hand_score
        else:
            hand_score = calculate_score_for_hand(list(self.player_two_hand), self.start_card)

            self.player_one_score += hand_score

        return hand_score

    def score_dealer_crib(self):
        """Sums up the score for the dealer player."""
        hand_score = 0
        if self.crib_turn == 2:
            hand_score = calculate_score_for_hand(list(self.crib), self.start_card)

            self.player_two_score += hand_score
        else:
            hand_score = calculate_score_for_hand(list(self.crib), self.start_card)

            self.player_one_score += hand_score

        return hand_score


class CribbageEngine:
    """
    Represents the main engine for storage and manipulation of the state of the game.

    Attributes
    ----------
    _base_deck : internal immutable representation of the 52 card deck
    deck : representation of a deck that may be shuffled and used for play

    Methods
    -------
    new_game: re-initializes the game and deck
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
        """Creates and returns a new game with the given players.

        Args:
            player_one: a CribbagePlayer AI for player one
            player_two: a CribbagePlayer AI for player two
        Returns:
            (CribbageGame) a new instance of a game
        """
        return CribbageGame(self._base_deck, player_one, player_two)


## Static Helper Methods
def cards_as_string(cards):
    """Converts a list of PlayingCards into a comma-separated string.

    Args:
        cards - the list of PlayingCards
    Returns:
        (String) a comma-separated list of cards
    """
    card_display_list = []
    for card in cards:
        if card is not None:
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
    """Calculates the score of points for the current hand.
    Args:
        player_hand - a list of PlayingCard that represents the player's hand
        start_card - a single PlayingCard that represents the start card

    Returns:
        (int) the score for the hand
    """

    logging.info("Calculating score for player hand [%s] with start card [%s]",
      cards_as_string(player_hand), start_card.get_display())

    hand_play_score = 0
    player_full_hand = player_hand.copy()

    ## Check for His Nob Before Appending the Start Card
    his_nob_score = _calculate_score_for_hand_his_nob(player_hand, start_card)
    hand_play_score += his_nob_score
    logging.info("His nob score [%s] gives total hand score [%s]",
      his_nob_score, hand_play_score)

    ## Check for a flush and full flush before appending the start card
    ## Todo: the crib must be a full flush
    is_flush = True
    flush_play_score = 0
    temp_flush_suit = player_hand[0].suit
    for card in player_full_hand:
        if card.suit != temp_flush_suit:
            is_flush = False

    if is_flush:
        if temp_flush_suit == start_card.suit:
            flush_play_score = 5
        else:
            flush_play_score = 4

    hand_play_score += flush_play_score
    logging.info("Flush score [%s] gives total hand score [%s]",
      flush_play_score, hand_play_score)

    player_full_hand.append(start_card)

    ## Find all combinations of cards that add up to 15
    for combination_size in range(2, len(player_full_hand)+1):
        combinations_set = list(combinations(player_full_hand, combination_size))
        for combo in combinations_set:
            cards_total_value = CribbageGame.get_cards_total_value(combo)
            if cards_total_value == 15:
                hand_play_score += 2
                logging.info("Found 15 [%s] for 2 gives total hand score [%s]",
                  cards_as_string(combo), hand_play_score)


    ## Find all pairs, they each are 2 points
    ## Triples, Quadruples can be ignored, they are just combinations of pairs
    combinations_set = list(combinations(player_full_hand, 2))
    for combo in combinations_set:
        if combo[0].face == combo[1].face:
            hand_play_score += 2
            logging.info("Found pair [%s] for 2 gives total hand score [%s]",
              cards_as_string(combo), hand_play_score)

    ## Find the runs, but don't count sub-runs.  Runs are between 3-5 cards. If the
    ## larger run of 4-5 is scored, subruns should be ignored.
    found_sequences = set()
    for combination_size in reversed(range(3, len(player_full_hand)+1)):
        combinations_set = list(combinations(player_full_hand, combination_size))
        for combo in combinations_set:
            if _can_sort_cards_to_sequence(combo):
                # Test if this newly found sequence is a subset of an existing sequence
                is_subsequence = False
                for found_sequence in found_sequences:
                    if set(combo) <= set(found_sequence):
                        is_subsequence = True
                        logging.info("Sequence [%s] is sub-sequence of [%s]",
                          cards_as_string(combo), cards_as_string(found_sequence))

                if not is_subsequence:
                    sequence_play_score = len(combo)
                    hand_play_score += sequence_play_score
                    logging.info("Found sequence [%s] for [%s] gives total [%s]",
                      cards_as_string(combo), sequence_play_score, hand_play_score)
                    found_sequences.add(combo)



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
