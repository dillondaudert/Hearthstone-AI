import os, sys
src_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(src_path)

import unittest
from gs_test import GetStateTestCase

full_test = unittest.TestSuite()
full_test.addTest(GetStateTestCase("test_player1"))
full_test.addTest(GetStateTestCase("test_player2"))
full_test.addTest(GetStateTestCase("test_draw_card"))
full_test.addTest(GetStateTestCase("test_mana_crystal"))
full_test.addTest(GetStateTestCase("test_turn1"))
full_test.addTest(GetStateTestCase("test_hand"))

if __name__ == "__main__":
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
    runner.run(full_test)
