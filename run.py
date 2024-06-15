'''
Runs Monstoryum game
'''

from rich.prompt import Prompt

# my function imports
from game.create import create_rooms
from game.turn import enter_room


def main():
    '''
    main function
    '''
    # create the game
    rooms = create_rooms()
    # start the game
    room_number = 0
    enter_room(rooms, room_number)
    # end the game or restart
    while True:
        play_again = Prompt.ask(
            "[chartreuse4]play again?[/chartreuse4] (yes/no)")
        if play_again == "yes" or play_again == "y":
            main()
        elif play_again == "no" or play_again == "n":
            print('goodbye')
            return


if __name__ == "__main__":
    main()
