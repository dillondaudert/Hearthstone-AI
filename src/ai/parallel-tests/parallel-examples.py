import multiprocessing as mp
import numpy as np

if __name__ = '__main__':

    #Get the current game state from the simulator
    #(trainer) If state is beginning of turn, save state vector in transition
    #Generate a list of actions, and build into parsable list of tuples (shuffle?)
    #Initialize array of Q values, q_vals, that corresponds to list of actions
    #For each action:
    #   (local) copy game object, perform action, get state feature vector, evaluate
    #   (global) Update root action with evaluation if larger
    #   (global) Hash state vectors
    #   (global) Add all nonduplicate post-action game objects to Queue
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
