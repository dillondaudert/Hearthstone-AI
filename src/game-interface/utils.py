#Build game objects and player objects for testing
import sys; sys.path.append("..")
from fireplace import cards
from fireplace.exceptions import GameOver
from fireplace.utils import setup_game


def setup():
    cards.db.initialize()
    game = setup_game()
    return game

