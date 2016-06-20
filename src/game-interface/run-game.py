"""
run-game.py
"""


def run_game(p1, p2, train):
    """
    initializes a game between two AI opponents, p1 and p2
        -pick 2 classes (no warriors)
        -build 2 decks
        -begin the game
        -skip the mulligan
    give the player whos turn it is control, looping over
    get_state, get actions, building the game tree to select
    the best action(using the weights in the network to select
    the first action in the tree sequence with the highest precieved value)
    continue to select actions until end turn is selected, if training,
    based on reward of this end state vs. precieved
    reward of the action sequence, update the weights accordingly
    (this probably requires storing the state info for each
    selected action)
        -break out of the above loop when a player loses
    """

def build_decks():
    """
    randomly select 30 cards for each players 
    deck including class cards, with the following restrictions:
    -no secrets
    """

def get_state():
    """
    """

def get_actions():
    """
    returns a single list of actions avalible to a player,
    including all possible targets for things like minion attacks and spells
    format: (action, target)
    """
    actions = []

    # add hero power if useable
    if player.hero.power.is_useable():
        # if targeting involved, add an instance of the hero power for all avalible targets
        actions.append(player.hero.power)

    # add in play 

def select_action(action):
    """
    """