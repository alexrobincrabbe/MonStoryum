import random as rnd
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
class Room:
    def __init__(self,description,player,monsters,items):
        self.description=description
        self.player=player
        self.monsters=monsters
        self.items=items
        self.battle_started=False
        self.monster_action=False

    def examine(self):
        print(self.description)
        print("You see:")
        for monster in self.monsters:
            print(monster.description)
        for item in self.items:
            print(item.description)

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

class Monster:
    def __init__(self,description,details,hp,strength,agility,armor,weapon):
        self.description=description
        self.details=details
        self.hp=int( (hp*rnd.random() + 2)/3 )
        self.start_hp=self.hp
        self.strength=strength
        self.agility=agility
        self.armor=armor
        self.weapon=weapon
    
    def attack(self,target):
        print(f'{self.description} attacks {target.description}...')
        hit=self.agility+self.weapon.hit + (rnd.random()*10)
        dodge=target.agility + target.armor.dodge + (rnd.random()*10)
        if hit > dodge:
            damage=self.strength + rnd.randrange(self.weapon.damage[0],self.weapon.damage[1]) - target.armor.armor_value
            damage = 1 if damage < 1 else damage
            print(f'{self.description} hits for {damage} points of damage')
            target.hp-=damage
            target.hp = 0 if target.hp < 0 else target.hp
        else:
            print(f'{self.description} misses')


def enter_room(rooms,room_number):
    '''
    initiate game state when the player enters a room
    '''
    clear_console()
    rooms[room_number].examine()
    start_turn(rooms, room_number)

def start_turn(rooms,room_number):
    room=rooms[room_number]
    if room.battle_started == True and room.monster_action == True:
        for monster in room.monsters:
            monster.attack(room.player)
    action=input('choose an action:')
    clear_console()
    options=["examine","inventory"]
    if len(room.monsters) == 0:
        options.append("forwards","backwards")
        if len(room.items) > 0:
            options.append("take")
    else:
        options.append("attack")
    if action == "help":
        for option in options:
            print(option)
        room.monster_action=False
    elif action == "attack":
        choose_target(room)
    elif action == "forwards":
        if len(room.monsters) == 0:
            room_number+=1
            enter_room(rooms,room_number)
        else:
            print("You must clear the path first")
            room.monster_action=False
    elif action == "backwards":
        if len(room.monsters) == 0:
            room_number-=1
            enter_room(room(room_number))
        else:
            print("You don't run away from a fight!")
            room.monster_action=False
    else:
        print("Please choose a valid option")
        for option in options:
            print(option)
        room.monster_action=False
    start_turn(rooms, room_number)
    
def choose_target(room):
    index=1
    
    for monster in room.monsters:
        print(f'{index}: {monster.description} HP - {monster.hp}/{monster.start_hp  }')
        index+=1
    
    target_number = input('Enter a number to choose a target: ')
    try:
        target_number=int(target_number)
    except:
        print('Please enter a number')
        choose_target(room)

    if target_number > 0 and target_number <= len (room.monsters):
        room.player.attack(room.monsters[target_number-1])
        room.battle_started=True
        room.monster_action=True
    else:
        print("Please pick a valid number")
        room.monster_action=False

def main ():
    no_armor=Armor("none", "none", 0, 0)
    fists=Weapon("fists", "none", [1,2], 0)
    dagger=Weapon("a dagger", "weapon", [3,6], 1)
    player=Monster("Alex", "A warrior", 25, 5, 5, no_armor, fists)
    drunk_goblin=Monster("a goblin","a drunk goblin", 10, 1, -5, no_armor,dagger)
    monsters=[drunk_goblin]
    items=[]
    rooms=[]
    rooms.append (Room("This is the first room",player,monsters,items))
    room_number=0
    enter_room(rooms,room_number)

main()