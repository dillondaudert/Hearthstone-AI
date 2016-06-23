"""
run-game.py
-basic UI between the NN and simulation
-utilities to initialize and run games
"""

from fireplace.utils import random_draft
from hearthstone.enums import CardClass, CardType


def setup_game():
    """
    initializes a game between two players
    """

    #choose classes (no warrior, paladin, mage, or hunter)
    while True:
        p1 = random.randint(2, 10)
        p2 = random.randint(2, 10)
        if all((p1, p2)) not in (3, 4, 5, 10):
            print ("hero indexes: p1 "+str(p1)+"\n p2 "+str(p2))
            p1 = CardClass(p1)
            p2 = CardClass(p2)
            break
    #initialize players and randomly draft decks
    deck1 = random_draft(CardClass.p1)
    deck2 = random_draft(CardClass.p2)
    player1 = Player("Player1", deck1, CardClass.p1.default_hero)
    player2 = Player("Player2", deck2, CardClass.p2.default_hero)
    #begin the game
    game = Game(players=(player1, player2))
    game.start()

    return game


def get_actions(player, game):
    """
    return:
        a list of action tuples avalible for a player
        in the current game state
    format:
        (action, target)

    *if target is N/A, it will be None
    """

    a = []

    # add hero power if useable
        #if targetable, add a copy for each valid target
    # add cards in hand
        #if minion, add all possible play locations
        #if spell, add all possible targets, if applicable
    # add all minions that can attack and all targets avalible
    # add hero attacking, if weapon equipt

    #return this enumerated list


def get_state(game):
    """
    return:
        a list of features extracted from the
        supplied game.

    p1 = active player

    *only the cards in hand of the player who's
     turn it is are evaluated
    """

    s = []

    # 0-5:  for p1's class
    # 6-11: for p2's class
    # 12-13: current health of current player, then opponent
    # 14: hero power used y/n
    # 15-16: # of mana crystals for you opponent
    # 17: # of crystals still avalible
    # 18: hero attacked y/n for you
    # 19-21, 22-24: weapon equipt y/n, pow., dur. for you, opponent
    # 25: # of cards in opponents hand
    # 26-27: # of cards in your + opponents graveyard
    # 28-29: # of cards in your + oppponents deck

    #in play minions

    # 30-169: 2, 7x10 grids for you + oppnents monsters, in the following format
    # filled y/n, pow, tough, current health, can attack
    # deathrattle, div shield, taunt, stealth y/n

    #in hand

    # 170 - 279:
    # 10x11
    # minion y/n, attk, hp, battlecry, div shield, deathrattle, taunt, stealth
    # weapon y/n, spell y/n, cost


def main():
    """
    """

if __name__ == "__main__":
    main():
