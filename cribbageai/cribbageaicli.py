import cribbageengine 
import logging

#logging.basicConfig(filename='cribbageapp.log', level=logging.DEBUG, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

logging.basicConfig(filename='cribbageapp.log', level=logging.DEBUG,
  format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Cribbage Cli Started")
cribbage_engine = cribbageengine.CribbageEngine()

menu_selection = -1
while menu_selection != "0":
    print("  ----- Main Menu -----")
    print("  Please make a choice:")
    print("  0. Quit")
    print("  1. Start Game")
    print("")
    print('  > ', end='')
    menu_selection = input()
    
    if menu_selection == "1":
        print("menu")

cribbage_engine.new_game()