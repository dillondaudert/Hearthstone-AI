import os, sys
src_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(src_path)

import multiprocess as mp
from time import sleep
from os import getpid
from copy import deepcopy
from fireplace.game import Game
from interface import *
from time import time

class ThisError(Exception):
    def __init__(self, message):
        super(ThisError, self).__init__("An exception of This Error")
        self.message = message

def function(a, game, fail, exc):
    try:
        if fail:
            raise ThisError("Child process %s failed!" % mp.current_process().name)
        else:       
            game.end_turn()
            print("Child process %s current player: " % mp.current_process().name)
    except:
        exc.put(ThisError("Child process %s failed!" % mp.current_process().name))

def main():

    initialize()
    game = setup_game()
    
    with mp.Manager() as manager:
    

        exc = manager.Queue() 

        arg_list = []
        for i in range(0, 3):
            arg_list.append( ((i, i+3), game, False, exc))
        arg_list.append( ((5, 5), game, True, exc))
        
        proc_list = []

        for arg in arg_list:
            proc_list.append(mp.Process(target=function, args=arg))
            proc_list[-1].start()
            
        print("Number of active children post start: %d" % len(mp.active_children()))
        for p in proc_list:
            p.join()
        if(not exc.empty()):
            e = exc.get()
            print(e.message)

    print("Number active children post join: %d " % len(mp.active_children()))
    print(mp.active_children())
    print(mp.current_process())

if __name__ == "__main__":
    main()
