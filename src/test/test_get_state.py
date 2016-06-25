#Test the get_state function over the course of an entire game
from util.exceptions import GetStateError
from fireplace import cards
from fireplace.exceptions import GameOver
from interface import *

def test_full_game():
    try:
        play_full_game()
    except GameOver:
        print("Game completed normally.")

def main():
    

if __name__ == "__main__":
    main()
