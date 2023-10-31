"""Provides a command line implementation of the Cribbage Engine.

Runs the primary Cribbage Engine and outputs to the command line the
state of the game as it progress.

"""

import logging

import cribbageengine
import cribbageplayers

def setup():
    """Performs initial environment setup.

    Sets the logging configuration.
    """
    logging.basicConfig(filename='cribbageapp.log', level=logging.WARN,
      format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Cribbage Cli Started")

def main():
    """Initializes the engine and starts the menu system."""

    main_menu()

def main_menu():
    """Displays the main menu.

    """
    menu_selection = -1
    cribbage_engine = cribbageengine.CribbageEngine()
    while menu_selection != "0":
        print("  ----- Main Menu -----")
        print("  Please make a choice:")
        print("  0. Quit")
        print("  1. Play Random Game")
        print("  2. Play 1000 Games - Randon v. Random")
        print("  3. Play 100 Games - Randon v. Best")
        print("")
        print('  > ', end='')
        menu_selection = input()

        if menu_selection == "1":
            cribbage_game = cribbage_engine.new_game(
              cribbageplayers.RandomPlayer(), cribbageplayers.OptimizedPlayer())

            run_game(cribbage_game, True)

        elif menu_selection == "2":
            player_one_victory = 0
            player_two_victory = 0
            for i in range(0, 1000):
                cribbage_game = cribbage_engine.new_game(
                  cribbageplayers.RandomPlayer(), cribbageplayers.RandomPlayer())

                player_one_score, player_two_score = run_game(
                  cribbage_game, False)

                if player_one_score > player_two_score:
                    player_one_victory += 1
                else:
                    player_two_victory += 1

            print(f"Results is Player 1 {player_one_victory} to Player 2 {player_two_victory}")

        elif menu_selection == "3":
            player_one_victory = 0
            player_two_victory = 0
            for i in range(0, 100):
                cribbage_game = cribbage_engine.new_game(
                  cribbageplayers.RandomPlayer(), cribbageplayers.OptimizedPlayer())

                player_one_score, player_two_score = run_game(
                  cribbage_game, False)

                if player_one_score > player_two_score:
                    player_one_victory += 1
                else:
                    player_two_victory += 1

            print(f"Results is Player 1 {player_one_victory} to Player 2 {player_two_victory}")


def run_game(cribbage_game, is_print_on):
    """Runs a new game.

    Args:
        cribbage_game: reference the cribbageengine.CribbageGame to use.
    """

    if is_print_on:
        print("# Fresh Game")

    game_round = 1
    while cribbage_game.player_one_score < 121 and cribbage_game.player_two_score < 121:
        cribbage_game.deal_cards()
        if is_print_on:
            print(f"## Dealing Cards - Dealer is Player #{cribbage_game.crib_turn}")

        cribbage_game.discard_to_crib()
        if is_print_on:
            print("## Discard to Crib")

        cribbage_game.cut_start_card()
        if is_print_on:
            print(f"## Cut Start Card: " \
              f"{cribbageengine.cards_as_string([cribbage_game.start_card])}")

        ## Play the Run
        while cribbage_game.is_more_run_cards():
            run_result = cribbage_game.play_next_run_card()

            if run_result["is_go"] and is_print_on:
                print(f'  Player #{run_result["run_turn"]} calls a go')
            elif is_print_on:
                print(f"  Player #{run_result['run_turn']} plays " \
                  f"{cribbageengine.cards_as_string([run_result['card_played']])} " \
                  f"total {run_result['run_total']} for {run_result['points_earned']}")


            # print_all_cards(cribbage_game)

        ## Reveal Hands:
        if is_print_on:
            print(f"## Player 1 Hand: " \
              f"{cribbageengine.cards_as_string(cribbage_game.player_one_hand)}")
            print(f"## Player 2 Hand: " \
              f"{cribbageengine.cards_as_string(cribbage_game.player_two_hand)}")
            print(f"## Crib     Hand: " \
              f"{cribbageengine.cards_as_string(cribbage_game.crib)}")


        ## Score the Pone
        pone_hand_score = cribbage_game.score_pone_hand()
        if is_print_on:
            print(f"## Score Pone Hand: {pone_hand_score}")

        dealer_score = cribbage_game.score_dealer_hand()
        if is_print_on:
            print(f"## Score Dealer Hand: {dealer_score}")

        crib_score = cribbage_game.score_dealer_crib()
        if is_print_on:
            print(f"## Score Dealer Crib: {crib_score}")

        if is_print_on:
            print(f"## End of Round {game_round}")
            print(f"  Player #1 Score: {cribbage_game.player_one_score}")
            print(f"  Player #2 Score: {cribbage_game.player_two_score}")

        game_round += 1

    return cribbage_game.player_one_score, cribbage_game.player_two_score

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
    print_cards([cribbage_game.start_card])
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
    main()
    # new_game(cribbageengine.CribbageEngine())
