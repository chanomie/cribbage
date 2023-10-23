"""Provides a command line implementation of the Cribbage Engine.

Runs the primary Cribbage Engine and outputs to the command line the
state of the game as it progress.

"""

import logging

import cribbageengine
import cribbagerandomplayer

def setup():
    """Performs initial environment setup.

    Sets the logging configuration.
    """
    logging.basicConfig(filename='cribbageapp.log', level=logging.INFO,
      format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Cribbage Cli Started")

def main():
    """Initializes the engine and starts the menu system."""

    cribbage_engine = cribbageengine.CribbageEngine()
    main_menu(cribbage_engine)

def main_menu(cribbage_engine):
    """Displays the main menu.

    Args:
        cribbage_engine: reference the engine to use.
    """
    menu_selection = -1
    while menu_selection != "0":
        print("  ----- Main Menu -----")
        print("  Please make a choice:")
        print("  0. Quit")
        print("  1. Play Random Game")
        print("")
        print('  > ', end='')
        menu_selection = input()

        if menu_selection == "1":
            new_game(cribbage_engine)

def new_game(cribbage_engine):
    """Creates and runs a new game.

    Args:
        cribbage_engine: reference the cribbageengine.CribbageEngine to use.
    """
    cribbage_game = cribbage_engine.new_game(
      cribbagerandomplayer.RandomPlayer(), cribbagerandomplayer.RandomPlayer())

    ## Deal Cards
    print("## Fresh Game:")
    print_all_cards(cribbage_game)

    print("## Dealing Cards:")
    cribbage_game.deal_cards()
    print_all_cards(cribbage_game)

    ## Discard to Crib
    print("## Discard to Crib:")
    cribbage_game.discard_to_crib()
    print_all_cards(cribbage_game)

    ## Pick Start Card
    print("## Cut Start Card:")
    cribbage_game.cut_start_card()
    print_all_cards(cribbage_game)

    ## Play the Run
    while cribbage_game.is_more_run_cards():
        print(f"Run Turn: {cribbage_game.run_turn}")
        cribbage_game.play_next_run_card()
        print_all_cards(cribbage_game)
        print(f"Run Total: {cribbageengine.CribbageGame.get_cards_total_value(cribbage_game.run)}")

def print_all_cards(cribbage_game):
    """Prints to the screen the state of the game.

    Args:
        cribbage_game: reference to a cribbageengine.CribbageGame .
    """

    print("")
    print("Deck: ", end='')
    print_cards(cribbage_game.game_deck)
    print("One : ", end='')
    print_cards(cribbage_game.player_one_hand)
    print("OneR: ", end='')
    print_cards(cribbage_game.player_one_run_hand)
    print(f"OneS: {cribbage_game.player_one_score}")
    print("Two : ", end='')
    print_cards(cribbage_game.player_two_hand)
    print("TwoR: ", end='')
    print_cards(cribbage_game.player_two_run_hand)
    print(f"TwoS: {cribbage_game.player_two_score}")
    print("Crib: ", end='')
    print_cards(cribbage_game.crib)
    print("Start: ", end='')
    print_cards(cribbage_game.start_card)
    print("Run: ", end='')
    print_cards(cribbage_game.run)


def print_cards(cards):
    """Prints a list of cards as a string to the screen

    Args:
        cards: reference to a List of ribbagengine.PlayingCard .
    """

    print(cribbageengine.cards_as_string(cards))

if __name__ == '__main__':
    setup()
    # main()
    new_game(cribbageengine.CribbageEngine())
