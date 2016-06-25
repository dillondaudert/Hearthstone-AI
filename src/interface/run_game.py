"""
run-game.py
-basic UI between the NN and simulation
-utilities to initialize and run games
"""

from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft
from fireplace import cards
from fireplace.exceptions import GameOver
from hearthstone.enums import CardClass, CardType
import random
import numpy as np


def initialize():
    """
    Initializes the environment. All basic initialization goes here.
    """
    cards.db.initialize()

def setup_game():
    """
    initializes a game between two players
    """

    #choose classes (no warrior, paladin, mage, or hunter)
    while True:
        p1 = random.randint(1, 11)
        p2 = random.randint(1, 11)
        if all((p1, p2)) not in (3, 4, 5, 10):
            print ("hero indexes: p1 "+str(p1)+"\n p2 "+str(p2))
            p1 = CardClass(p1)
            p2 = CardClass(p2)
            break
    #initialize players and randomly draft decks
    deck1 = random_draft(p1)
    deck2 = random_draft(p2)
    player1 = Player("Player1", deck1, p1.default_hero)
    player2 = Player("Player2", deck2, p2.default_hero)
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

    p1 = game.current_player
    p2 = game.current_player.opponent
    s = np.zeros(263, dtype=np.int32)

    #0-9 player1 class, we subtract 1 here because the classes are from 1 to 10
    s[p1.hero.card_class-1] = 1
    #10-19 player2 class
    s[10 + p2.hero.card_class-1] = 1
    i = 20
    # 20-21: current health of current player, then opponent
    s[i] = p1.hero.health
    s[i + 1] = p2.hero.health

    # 22: hero power usable y/n
    s[i + 2] = p1.hero.power.is_usable()*1
    # 23-24: # of mana crystals for you opponent
    s[i + 3] = p1.max_mana
    s[i + 4] = p2.max_mana
    # 25: # of crystals still avalible
    s[i + 5] = p1.mana
    #26-31: weapon equipped y/n, pow., dur. for you, then opponent
    s[i + 6] = 0 if p1.weapon is None else 1
    s[i + 7] = 0 if p1.weapon is None else p1.weapon.damage
    s[i + 8] = 0 if p1.weapon is None else p1.weapon.durability

    s[i + 9] = 0 if p2.weapon is None else 1
    s[i + 10] = 0 if p2.weapon is None else p2.weapon.damage
    s[i + 11] = 0 if p2.weapon is None else p2.weapon.durability

    # 32: number of cards in opponents hand
    s[i + 12] = len(p2.hand)
    #in play minions

    i = 33
    #33-102, your monsters on the field
    p1_minions = len(p1.field)
    for j in range(0, 7):
        if j < p1_minions:
            # filled y/n, pow, tough, current health, can attack
            s[i] = 1
            s[i + 1] = p1.field[j].atk
            s[i + 2] = p1.field[j].max_health
            s[i + 3] = p1.field[j].health
            s[i + 4] = p1.field[j].can_attack()*1
            # deathrattle, div shield, taunt, stealth y/n
            s[i + 5] = p1.field[j].has_deathrattle*1
            s[i + 6] = p1.field[j].divine_shield*1
            s[i + 7] = p1.field[j].taunt*1
            s[i + 8] = p1.field[j].stealthed*1
            s[i + 9] = p1.field[j].silenced*1
        i += 10

    #103-172, enemy monsters on the field
    p2_minions = len(p2.field)
    for j in range(0, 7):
        if j < p2_minions:
            # filled y/n, pow, tough, current health, can attack
            s[i] = 1
            s[i + 1] = p2.field[j].atk
            s[i + 2] = p2.field[j].max_health
            s[i + 3] = p2.field[j].health
            s[i + 4] = p2.field[j].can_attack()*1
            # deathrattle, div shield, taunt, stealth y/n
            s[i + 5] = p2.field[j].has_deathrattle*1
            s[i + 6] = p2.field[j].divine_shield*1
            s[i + 7] = p2.field[j].taunt*1
            s[i + 8] = p2.field[j].stealthed*1
            s[i + 9] = p2.field[j].silenced*1
        i += 10


    #in hand

    #173-262, your cards in hand
    p1_hand = len(p1.hand)
    for j in range(0, 10):
        if j < p1_hand:
            #card y/n
            s[i] = 1
            # minion y/n, attk, hp, battlecry, div shield, deathrattle, taunt
            s[i + 1] = 1 if p1.hand[j].type == 4 else 0
            s[i + 2] = p1.hand[j].atk if s[i + 1] == 1 else 0
            s[i + 2] = p1.hand[j].health if s[i + 1] == 1 else 0
            s[i + 3] = p1.hand[j].divine_shield*1 if s[i + 1] == 1 else 0
            s[i + 4] = p1.hand[j].has_deathrattle*1 if s[i + 1] == 1 else 0
            s[i + 5] = p1.hand[j].taunt*1 if s[i + 1] == 1 else 0
            # weapon y/n, spell y/n, cost
            s[i + 6] = 1 if p1.hand[j].type == 7 else 0
            s[i + 7] = 1 if p1.hand[j].type == 5 else 0
            s[i + 8] = p1.hand[j].cost
        i += 9

    return s


            
