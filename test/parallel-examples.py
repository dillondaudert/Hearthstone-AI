import multiprocessing as mp
import numpy as np
import random
from dqn import DQN
from interface import get_actions, get_state, perform_action
from fireplace.game import Game
from fireplace.Player import Player
from fireplace.exceptions import GameOver, InvalidAction


    #(global) If we aren't over hard limit of evaluations:
    #   (global) Iterate over action Queue, keep track of # evals: 
    #       Pass game, a_index, q_vals, lock to worker process
    #       (local) Generate list of actions, build into parsable list of tuples (shuffle?)
    #       For each action:
    #           (local) copy game object, perform action, get state feature vector, evaluate
    #           (global) Update root action with evaluation if larger
    #           (global) Hash state vectors
    #           (global) Add all nonduplicate post-action game objects to Queue
    #(global) Hard limit for # evaluations is reached
    #Return action associated with the highest Q value in q_vals  
    #(trainer) If action is end turn, save state vector and reward in transition
def look_ahead(game: Game, dqn: DQN):
    """
    From a given game state, return an action to be performed.
    Args:
        game, a Game object for the current state
    Returns:
        action, a tuple representing an action and its optional target
    """
    #Get the current game state from the simulator
    #(trainer) If state is beginning of turn, save state vector in transition
    
    #Generate a list of actions, and build into parsable list of tuples (shuffle?)
    actions = random.shuffle(get_actions(game.current_player)) 

    #Initialize array of Q values, q_vals, that corresponds to list of actions
    q_vals = mp.Array('f', len(actions))
    for i in range(len(q_vals)):
        q_vals[i] = 0.0
    #A queue of (game, root_index) pairs representing leaves of the game tree
    queue = mp.Queue()

    #For each action:

def eval_game(game: Game, dqn: DQN, action, q_vals, queue, root_index, root=True):
    """
    Called by look_ahead function. Used to evaluate a state, update Q value,
    enumerate and enqueue possible child actions.
    By default, this treats the root actions first.
    Args:
        game, A Game object to be evaluated
        dqn, A deep Q learning network object to evaluate state
        action, A tuple representing an action and its optional target
        q_vals, A shared mem array for the global Q vales
        queue, A Queue to store child actions
        root_index, The index of the root action in q_vals
        root(=True), Whether or not these are the root actions
    Returns:
        self
    """

    #   (local) copy game object, perform action, get state feature vector, evaluate
    perform_action(action, game.current_player, game)
    state = get_state(game)
    
    #Pass to Tensorflow here to evaluate
    s_val = dqn.get_q_value(state, "dqn")

    print("Action:", action)
    print("Q value: %f", s_val)

    """
    #   (global) Update root action with evaluation if larger
    if s_val > q_vals[root_index]:
        q_vals[root_index] = s_val

    #   (global) Hash state vectors

    #   (global) Add all nonduplicate post-action game objects to Queue
    queue.put((game, root_index, s_val))
    """
