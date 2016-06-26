"""
run-game.py
-basic UI between the NN and simulation
-utilities to initialize and run games
"""

from fireplace import cards
from fireplace.utils import random_draft
from fireplace.game import BaseGame
from fireplace.player import Player
from hearthstone.enums import CardClass, CardType
import random
import pdb


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
    game = BaseGame(players=(player1, player2))
    game.start()
    #pdb.set_trace()

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

    cards.db.initialize()
    game = setup_game()
    for _ in range(1000):
        actions = get_actions(game.current_player)
        index = random.randint(0, len(actions)-1)
        perform_action(actions[index], game.current_player, game)

if __name__ == "__main__":
    main()
