class Room:
    def __init__(self,description):
        self.description=description
    
    def examine(self):
        print(self.description)

class Item:
    def __init__(self,description,item_type):
        self.description=description
        self.type=item_type
    
    def examine(self):
        print(self.description)

class Weapon(Item):
    def __init__(self,description,item_type,damage,hit):
        Item.__init__(self,description,item_type)
        self.damage=damage
        self.hit=hit

class Armor(Item):
    def __init__(self,description,item_type,armor_value,dodge):
        Item.__init__(self,description,item_type)
        self.armor_value=armor_value
        self.dodge=dodge

class Potion(Item):
    def __init__(self,description,item_type,stat,bonus):
        Item.__init__(self,description,item_type)
        self.stat=stat
        self.bonus=bonus

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