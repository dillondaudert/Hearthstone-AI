#Test the get_state function over the course of an entire game
from util.exceptions import GetStateError
from fireplace import cards
from fireplace.exceptions import GameOver
from interface.run_game import *
from fireplace.utils import play_turn
import numpy as np

def test_full_game():
    try:
        play_full_game()
    except GameOver:
        print("Game completed normally.")

def main():
    initialize()
    game = setup_game()
    
    try:
        while True:
            game = play_turn(game)
            s = get_state(game)
    except GetStateError:
        print("Error with get_state function")
    

if __name__ == "__main__":
    main()
