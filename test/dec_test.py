import os, sys
src_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(src_path)

from interface import *

import unittest
import numpy as np
import multiprocessing as mp
from dqn import DQN
from dec_process import *
from hearthstone.enums import CardClass
from exceptions import GameTreeFailure

class DecTreeTestCase(unittest.TestCase):
    """
    Test the game tree functionality.
    """
    features = 263
    h1 = 50
    h2 = 50
    model_path = "models/dec_test"
    dqn = DQN(features, h1, h2, model_path)

    @classmethod
    def setUpClass(self):
        initialize()
        self.game = setup_basic_game()

        self.p1 = self.game.current_player        

        self.s1_1 = get_state(self.game, self.p1)
        self.game.end_turn()

        self.s1_2 = get_state(self.game, self.p1)
        self.game.end_turn()

        self.s2_1 = get_state(self.game, self.p1)

    def setUp(self):
        return
    def tearDown(self):
        return

    def test_look_ahead(self):
        return

    def test_tf_worker(self):
        
        return

    def test_tf_worker_except(self):
        q_vals = mp.Array('f', 1)
        q_vals[0] = 0.0
 
        s_queue = mp.Queue()
        with self.assertRaises(GameTreeFailure):
            try:
                worker = mp.Process(target=tf_worker, args=(self.dqn, s_queue, q_vals))
                worker.start()
                worker.join()
            except:
                raise
            


    def test_eval_game(self):
        return

