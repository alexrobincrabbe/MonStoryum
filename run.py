'''
Runs Monstoryum game
'''

from rich.prompt import Prompt

# my function imports
from game.create_game import create_rooms
from game.play_turn import enter_room


def play_again_prompt():
    '''
    prompt the player to play again or exit the game
    '''
    while True:
        play_again = Prompt.ask(
            "[chartreuse4]play again?[/chartreuse4] (yes/no)")
        if play_again == "yes" or play_again == "y":
            return True
        elif play_again == "no" or play_again == "n":
            print('goodbye')
            return False


def main():
    '''
    main function to run the game
    '''
    play_again = True
    while play_again is True:
        # create the game
        rooms = create_rooms()
        # start the game
        room_number = 0
        enter_room(rooms, room_number)
        # end the game or restart
        play_again = play_again_prompt()


if __name__ == "__main__":
    main()
