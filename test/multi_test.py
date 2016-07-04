import os, sys
src_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(src_path)

import multiprocess as mp
from time import sleep
from os import getpid
from multiprocess.managers import BaseManager
from copy import deepcopy
from fireplace.game import Game
from interface import *
from time import time


class AIManager(BaseManager): pass

AIManager.register('Game', Game)


class ThisError(Exception):
    def __init__(self, message):
        super(ThisError, self).__init__("An exception of This Error")
        self.message = message

def function(a, game, fail):
    if fail:
        raise ThisError("Child process %s failed!" % mp.current_process().name)
    else:
        return gamecopy.current_player

def callb(result):
    print("Process %d with %s" % (mp.current_process().name, str(result)))

def err_callb(exception):
    print(exception.message)
    print(type(exception))

def main():

    initialize()
    game = setup_game()

    manager = AIManager()
    
    with AIManager() as manager:

        t0 = time()
        gamecopy = manager.Game(game.player1, game.player2)
        t1 = time()
    
        print("Time to create manager Game: ", (t1-t0))
    
        arg_list = []
        for i in range(0, 3):
            arg_list.append( ((i, i+3), gamecopy, False ))
    
        with mp.Pool() as pool:
            result2 = pool.starmap_async(function, arg_list, callback=callb, error_callback=err_callb)
            result1 = pool.starmap_async(function, ( ((5,5), gamecopy, True)), error_callback=err_callb)
            
            while(not (result2.ready() and result1.ready())):
                sleep(1)

if __name__ == "__main__":
    main()
