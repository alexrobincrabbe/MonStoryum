import random as rnd

class Room:
    def __init__(self,description,player,monsters,items):
        self.description=description
        self.player=player
        self.monsters=monsters
        self.items=items

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
            damage=self.strength + rnd.randrange[self.weapon.damage[0],self.weapon.damage[1]] - target.armor.armor_value
            damage = 1 if damage < 1 else None
            print(f'{self.description} hits for {damage} points of damage')
            target.hp-=damage
            target.hp = 0 if target.hp < 0 else None
        else:
            print(f'{self.description} misses')


def enter_room(room):
    '''
    initiate game state when the player enters a room
    '''
    room.examine()

def main ():
    no_armor=Armor("none", "none", 0, 0)
    fists=Weapon("fists", "none", [1,2], 0)
    dagger=Weapon("a dagger", "weapon", [3,6], 1)
    player=Monster("Alex", "A warrior", 25, 5, 5, no_armor, fists)
    drunk_goblin=Monster("a goblin","a drunk goblin", 10, 1, -5, no_armor,dagger)
    monsters=[drunk_goblin]
    items=[]
    room=[]
    room.append (Room("This is the first room",player,monsters,items))
    room_number=0
    enter_room(room[room_number])

main()