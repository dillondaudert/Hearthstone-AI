#decision-process.py
# The decision process builds, executes and evaluates the game tree.
# The concise behavior of the DP is as follows:
#   1. Recieve a game state
#   2. Build game tree and evaluate
#   3. Return action to game

#class DecisionProcess(object):
#    def __init__(self):

import multiprocessing as mp
import numpy as np
import random
import tensorflow as tf
from math import isclose
from dqn import DQN
from interface import *
from exceptions import GameTreeFailure
from fireplace.game import Game
from fireplace.player import Player
from fireplace.exceptions import GameOver, InvalidAction
from queue import Empty
import sys


    #***NOT IMPLEMENTED YET***
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
    #***END NOT IMPLEMENTED SECTION***


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
    actions = get_actions(game.current_player)
    random.shuffle(actions) 

    #Initialize array of Q values, q_vals, that corresponds to list of actions
    q_vals = mp.Array('f', len(actions))
    for i in range(len(q_vals)):
        q_vals[i] = 0.0
    #A queue of (game, root_index) pairs representing leaves of the game tree
    queue = mp.Queue()
    #A queue of (index, numpy array) pairs to evaluate by tf_worker
    s_queue = mp.Queue()

    with mp.Pool() as pool:
        

    tf_proc = mp.Process(target=tf_worker, args=(dqn, s_queue, q_vals))
    tf_proc.start()

    #Evalute the game tree (to be expanded)
    processes = []

    for index in range(len(actions)):
        processes.append(mp.Process(target=eval_game, args=(game, dqn, actions[index], queue, s_queue, index)))
        processes[index].start()

    for index in range(len(actions)):
        processes[index].join()

    s_queue.put( (-1, 0) )
    tf_proc.join()
    
    #Play highest Q value
    q_list = list(q_vals)
    #import pdb; pdb.set_trace()
    print(q_list)
    best_action = actions[q_list.index(max(q_list))]
    return best_action

def tf_worker(dqn: DQN, s_queue, q_vals):
    """
    A single process that removes evaluation tasks from a queue.
    It constructs the TF network and uses it to evaluate board states sent to it.
    Args:
        dqn, an uninitialized TensorFlow object representing the DQN
        s_queue, the queue of board states.
    Returns:
        self
    """

   #Perform TensorFlow initialization 
    with tf.Graph().as_default() as dqn.tf_graph:
        dqn.build_model() 
        with tf.Session() as dqn.tf_session:
            dqn._init_tf()

    try:
        index, state = s_queue.get(True, 5)
        while index != -1:
            #Reshape to align with network input.
            state = state.reshape(1, 263)
            #Pass to Tensorflow here to evaluate
            s_val = dqn.get_q_value(state, "dqn")
            print("Got Q value %f for root %d" % (s_val, index))
            sys.stdout.flush()

            #   (global) Update root action with evaluation; average child values
            if not isclose(q_vals[index], 0.0, rel_tol=1e-6):
                q_vals[index] = (q_vals[index] + s_val)/2
            else:
                q_vals[index] = s_val
            index, state = s_queue.get(True, 5)
    except Empty as e:
        print("Exception! Waited to long for task in state queue.\n", e)
        sys.stdout.flush()
        raise GameTreeFailure
        
             




def eval_game(game: Game, dqn: DQN, action, queue, s_queue, root_index, root=True):
    """
    Called by look_ahead function. Used to evaluate a state, update Q value,
    enumerate and enqueue possible child actions.
    By default, this treats the root actions first.
    Args:
        game, A Game object to be evaluated
        dqn, A deep Q learning network object to evaluate state
        action, A tuple representing an action and its optional target
        queue, A Queue to save child actions
        s_queue, A Queue to send state evaluation tasks
        root_index, The index of the root action in q_vals
        root(=True), Whether or not these are the root actions
    Returns:
        self
    """

    #   (local) copy game object, perform action, get state feature vector, evaluate
    if action[0] != "end_turn":
        perform_action(action, game.current_player, game)
    state = get_state(game)
    
    s_queue.put( (root_index, state) )
    
    """

    #   (global) Hash state vectors

    #   (global) Add all nonduplicate post-action game objects to Queue
    queue.put((game, root_index, s_val))
    """
