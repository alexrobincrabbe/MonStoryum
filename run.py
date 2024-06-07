class Room:
    def __init__(self,description):
        self.description=description
    
    def examine(self):
        print(self.description)


def enter_room(room):
    '''
    initiate game state when the player enters a room
    '''
    room.examine()

def main ():
    room=[]
    room.append (Room("This is the first room"))
    room_number=0
    enter_room(room[room_number])

main()