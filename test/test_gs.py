import os, sys
src_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(src_path)

from interface import *

import unittest
import numpy as np
from hearthstone.enums import CardClass

class GetStateTestCase(unittest.TestCase):
    """
    Assert that the states of two turns where both players have taken
    no actions between them produce the same state vector,
    after accounting for drawing a card and receiving a new mana crystal
    """
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

    def test_player1(self):
        #Assert that player 1's class is in the correct location 
        self.assertEqual(self.s1_1[self.p1.hero.card_class-1], 1, msg="Player 1 class not in array!")

    def test_player2(self):
        #Assert that player 2's class is in the correct location 
        self.assertEqual(self.s1_1[10+self.p1.opponent.hero.card_class-1], 1, msg="Player 2 class not in array!!")

    def test_draw_card(self):
        
        #Assert that the enemy has a different # of cards
        self.assertNotEqual(self.s1_1[32], self.s1_2[32], 
                msg="Opponent should have drawn a card.")

    def test_mana_crystal(self):
        
        self.assertNotEqual(self.s1_1[24], self.s1_2[24], 
                msg="Opponent should have an additional mana crystal.")

    def test_turn1(self):
        
        s1_2_mod = np.copy(self.s1_2)
        s1_2_mod[32] = self.s1_1[32]
        s1_2_mod[24] = self.s1_1[24]
        #Assert that changing # of cards and mana crystals means states are equiv.
        
        self.assertTrue(np.array_equal(self.s1_1, s1_2_mod), 
                msg="Game state changed in areas other than number of opponent cards and number of mana crystals!")


    def test_hand(self):
        
        #Assert that on the first turn, the first player has no more than 4 cards
        c1 = self.s1_1[173]
        c2 = self.s1_1[182]
        c3 = self.s1_1[191]
        c4 = self.s1_1[200]
        c5 = self.s1_1[209]
        c5_2 = self.s2_1[209]
        self.assertTrue(c1 and c2 and c3 and c4 and not c5 and c5_2, msg="Player 1 should have only 4 cards on turn 1, and 5 cards on turn 2.")

