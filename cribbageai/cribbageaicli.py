import cribbageengine
import cribbagerandomplayer
import logging

#logging.basicConfig(filename='cribbageapp.log', level=logging.DEBUG, filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def setup():
    logging.basicConfig(filename='cribbageapp.log', level=logging.DEBUG,
      format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Cribbage Cli Started")
    
def main():
    cribbage_engine = cribbageengine.CribbageEngine()
    main_menu(cribbage_engine)
    
def main_menu(cribbage_engine):
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
        print("Run Turn: %i" % cribbage_game.run_turn)
        cribbage_game.play_next_run_card()
        print_all_cards(cribbage_game)
        print("Run Total: %i" % cribbage_game.get_run_total())

def print_all_cards(cribbage_game):
    print("")
    print("Deck: ", end='')
    print_cards(cribbage_game.game_deck)
    print("One : ", end='')
    print_cards(cribbage_game.player_one_hand)
    print("OneR: ", end='')
    print_cards(cribbage_game.player_one_run_hand)
    print("OneS: %i" % cribbage_game.player_one_score)
    print("Two : ", end='')
    print_cards(cribbage_game.player_two_hand)
    print("TwoR: ", end='')
    print_cards(cribbage_game.player_two_run_hand)
    print("TwoS: %i" % cribbage_game.player_two_score)
    print("Crib: ", end='')
    print_cards(cribbage_game.crib)
    print("Start: ", end='')
    print_cards(cribbage_game.start_card)
    print("Run: ", end='')
    print_cards(cribbage_game.run)
    


def print_cards(cards):
    print(cribbageengine.cards_as_string(cards))

if __name__ == '__main__':
    setup()
    main()