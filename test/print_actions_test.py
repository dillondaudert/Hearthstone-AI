#Simple test function to play a turn of a game, printing out all actions the player has.

from run_game import *
import random

def main():

    a_out = open("action_list.txt", "w")

    initialize()
    game = setup_game()

    num_actions = 0    

    while True:
        actions = get_actions(game.current_player)
        for item in actions:
            a_out.write('%s ' % str(item))
        a_out.write('\n')

        index = random.randint(0, len(actions)-1)
        a_out.write('Chose: %s\n' % str(actions[index]))
        perform_action(actions[index], game.current_player, game)
        num_actions += 1
        if actions[index][0] == 'end_turn':
            a_out.write('End of turn\n')
            if(num_actions > 6):
                a_out.close()
                break

if __name__ == '__main__':
    main()
