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
    (using simplified BaseGame class from game.py)
    """

    #choose classes (priest, rogue, shaman, warlock)
    p1 = random.randint(6, 9)
    p2 = random.randint(6, 9)
    #initialize players and randomly draft decks
    #pdb.set_trace()
    deck1 = random_draft(CardClass(p1))
    deck2 = random_draft(CardClass(p2))
    player1 = Player("Player1", deck1, CardClass(p1).default_hero)
    player2 = Player("Player2", deck2, CardClass(p2).default_hero)
    #begin the game
    game = Game(players=(player1, player2))
    game.start()

    #Skip mulligan for now
    for player in game.players:
        cards_to_mulligan = random.sample(player.choice.cards, 0)
        player.choice.choose(*cards_to_mulligan)

    return game


def get_actions(player):
    """
    generate a list of tuples representing all valid targets
    format:
    (actiontype, index, target)
    """

    actions = []

    # add cards in hand
    for index, card in enumerate(player.hand):
        if card.is_playable():
            # summonable minions (note some require a target on play)
            if card.type == 4:
                if card.has_target():
                    for target in card.targets:
                        actions.append(("summon", index, target))
                else:
                    actions.append(("summon", index, None, None))
            # playable spells and weapons
            elif card.has_target():
                for target in card.targets:
                    actions.append(("spell", index, target))
            else:
                actions.append(("spell", index, None))
    # add targets avalible to minions that can attack
    for position, minion in enumerate(player.field):
        if minion.can_attack():
            for target in minion.attack_targets:
                actions.append(("attack", position, target))
    # add hero power and targets if applicable
    if player.hero.power.is_usable():
        if player.hero.power.has_target():
            for target in player.hero.power.targets:
                actions.append(("hero_power", None, target))
        else:
            actions.append(("hero_power", None, None))
    # add hero attacking if applicable
    if player.hero.can_attack():
        for target in player.hero.attack_targets:
            actions.append(("hero_attack", None, target))
    # add end turn
    actions.append(("end_turn", None, None))

    return actions


def perform_action(a, player, game):
    """
    utilty to convert an action tuple
    into an action input
    """

    if a[0] == "summon":
        if a[2] is None:
            player.hand[a[1]].play()
        else:
            player.hand[a[1]].play(a[2])
    elif a[0] == "spell":
        if a[2] is None:
            player.hand[a[1]].play()
        else:
            player.hand[a[1]].play(a[2])
    elif a[0] == "attack":
        player.field[a[1]].attack(a[2])
    elif a[0] == "hero_power":
        if a[2] is None:
            player.hero.power.use()
        else:
            player.hero.power.use(a[2])
    elif a[0] == "hero_attack":
        player.hero.attack(a[2])
    elif a[0] == "end_turn":
        game.end_turn()


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


def main():

    cards.db.initialize()
    game = setup_game()
    for _ in range(1000):
        actions = get_actions(game.current_player)
        index = random.randint(0, len(actions)-1)
        perform_action(actions[index], game.current_player, game)

if __name__ == "__main__":
    main()
