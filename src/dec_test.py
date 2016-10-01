#Script to test the decision tree evaluation process
import numpy as np
from dqn import DQN
from dec_process import look_ahead
from exceptions import GetStateError
from fireplace import cards
from fireplace.exceptions import GameOver
from interface import *
from fireplace.utils import play_turn





def main():

    #Set up the network for the first time
    features = 263
    h1 = 50
    h2 = 50

    dqn = DQN(features, h1, h2, "models/test_1")

    #Initialize the game
    initialize()
    game = setup_game()
    ai_player = game.current_player

    try:
        while True:
            if game.current_player == ai_player:
                action_choice = look_ahead(game, dqn)
                print("Action chosen was: ", action_choice)
                import pdb; pdb.set_trace()
                perform_action(action_choice, ai_player, game)
            else:
                actions = get_actions(game.current_player)
                index = random.randint(0, len(actions)-1)
                perform_action(actions[index], game.current_player, game)


    except GetStateError:
        print("Error with get_state function")
    except GameOver:
        print("Game ended normally")
    
if __name__ == "__main__":
    main()
