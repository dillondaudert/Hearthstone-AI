import os, sys
src_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(src_path)

from interface import *

import unittest
import numpy as np

class InterfaceTestCase(unittest.TestCase):
    def setUp(self):
        self.game = setup_game()

    def tearDown(self):
        return

    def test_get_state(self):
        
