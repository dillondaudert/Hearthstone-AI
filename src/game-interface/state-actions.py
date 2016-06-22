# Add imports here later when testing is to be done

### 6-16-16 ###

# Variable may be set up to contain a game for state extraction
# Does not need to be started, can assume state can still be extracted

#TheGame = Game(MulliganRules, CoinRules, BaseGame)
# BaseGame is initialized on an Entity object. The __init__ method
# itself works on "self", and the players

# Reminders from the wiki:
#   All game objects are subclasses of type Entity (may be useful later)
#   A game has two player objects
#     These keep track of their zones (deck, hand, play, graveyard)

# The __init__ method of the players, and, in players.py, the can_pay_cost()
# will be looked at later and this comment will be moved downward when used

### 6-20-16 ###

# Base actions in hearthstone
# - play a card
# - use hero ability
# - direct minion to attack
# - direct hero to attack
# - use weapon
# - end turn

coinFlip = CoinRules() 
# Needing to actually select player and play the game is unknown at this point

selCards = MulliganRules()

# Python inheritance in subclass definitions has the superclass in parentheses
# This can be confusing when trying to find the arguments to initialization

# Need to declare players for BaseGame beforehand
# Apparently can assume it has the class type that matches the file
# players.py and can use those functions/attributes

# This resulting file has been written backwards in terms of declarations as
# API understanding increases
botName = "bot"
otherName = "other"

# Decks can be initialized without any cards due to the fact that the default
# value for their "cards" attribute is an empty list
botDeck = Deck()
otherDeck = Deck()

# Players are initialized with a hero of "None" (equivalent to null)
botHero = None
otherHero = None

botPlayer = (botName, botDeck, botHero)

# Preference to keep variable names unique expressed here
# Program is likely to end up being for proof-of-concept as opposed to
# containing a robust function
otherPlayer = (otherName, otherDeck, otherHero)

### Get hero.power here ###

bothPlayers = [botPlayer, otherPlayer]

# Within the __init__() function of a class, the "self" keyword can be
# confusing if mistaken as another argument that needs to provided
gameBase = BaseGame(bothPlayers)

TheGame = Game(selCards, coinFlip, gameBase)
# The pass keyword creates an unknown in the implementation that
# creates the actual game instance. Assuming baseGame's __init handles it

# From game.py to cards.py, a method is found in cards.py called is_playable().
# Understanding of a card's "controller", but this is a huge stumbling block
# out of the way (in contrast to needing to find all
# the possible invalid actions from the possible types of errors).
#   [InvalidAction raise in card.py]

### From class ###

# controller note: check player.py, returns self
# actionable_entities in player.py...is this useful?

# Might also be able to get the hands (and cards respectively...)
# through chain returns, but then comes the problem of only getting the cards
# of just one player. Test each one's controller?

# Note: Apparently there are two different declarations of is_summonable(), the
# first one with weird syntax just returns true, but the second 
# Note: In cards.py there is a has_target() function

# The play_turn() function in utils.py is even better than the is_playable
# function, and may be everything that is needed
# This led to the finding of the hero.power property and needing to understand
# Python yield statement (and generators)

# After this new understanding of the API, did an actual game need to be
# declared at all?
