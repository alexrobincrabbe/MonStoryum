import random as rnd
import os
from rich import print
from rich import pretty
pretty.install()
from prettytable import PrettyTable
import time

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
class Room:
    def __init__(self,details,details_visited,player,monsters,items,features):
        self.details=details
        self.details_visited=details_visited
        self.player=player
        self.monsters=monsters
        self.items=items
        self.features=features
        self.battle_started=False
        self.monster_action=False
        self.door="open"
        self.key_name=""
        self.visited=False

    def examine(self):
        if self.visited == False:
            print(self.details)
        else:
            print(self.details_visited)
        print("You see:")
        for monster in self.monsters:
            print(f'a {monster.description}')
        for item in self.items:
            print(f'a {item.description}')
        for feature in self.features:
            print(f'a {feature.description}')
    
class Item:
    def __init__(self,description,details):
        self.description=description
        self.details=details
    
    def examine(self):
        print(self.description)

class Weapon(Item):
    def __init__(self,description,details,damage,hit):
        Item.__init__(self,description,details)
        self.damage=damage
        self.hit=hit
        self.type="weapon"

class Armor(Item):
    def __init__(self,description,details,armor_value,dodge):
        Item.__init__(self,description,details)
        self.armor_value=armor_value
        self.dodge=dodge
        self.type="armor"

class Potion(Item):
    def __init__(self,description,details,stat,effect):
        Item.__init__(self,description,details)
        self.stat=stat
        self.effect=effect
        self.type="potion"

class Key(Item):
    def __init__(self,description,details,key_name):
        Item.__init__(self,description,details)
        self.key_name=key_name
        self.type="key"
class Monster:
    def __init__(self,description,details,hp,strength,agility,armor,weapon,loot):
        self.description=description
        self.details=details
        self.hp=int( (rnd.random()*hp + 2*hp)/3 )
        self.start_hp=self.hp
        self.strength=strength
        self.agility=agility
        self.armor=armor
        self.weapon=weapon
        self.loot=loot
        if self.armor.description != "none":
            self.loot.append(self.armor)
        if self.weapon.description != "none":
            self.loot.append(self.weapon)
    
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
        
class Player(Monster):
    def __init__(self,description,details,hp,strength,agility,armor,weapon,loot):
        Monster.__init__(self,description,details,hp,strength,agility,armor,weapon,loot)
        self.inventory=[]
        
    def display_inventory(self):
        self.weapons=[]
        self.armors=[]
        self.potions=[]
        for item in self.inventory:
            if item.type=="weapon":
                self.weapons.append(item)
            if item.type=="armor":
                self.armors.append(item)
            if item.type=="potion":
                self.potions.append(item)
        
        self.print_weapons()
        self.print_armor()
        self.print_potions()

    def print_weapons(self):
        table = PrettyTable()
        weapon_data=([weapon.description for weapon in self.weapons])
        damage_data=([f'{weapon.damage[0]}-{weapon.damage[1]}' for weapon in self.weapons])
        hit_data=(['{0:+}'.format(weapon.hit) for weapon in self.weapons])
        table.add_column("Weapons",weapon_data)
        table.add_column("Damage",damage_data)
        table.add_column("Hit bonus",hit_data)
        print(table)

    def print_armor(self):
        table = PrettyTable()
        armor_data=([armor.description for armor in self.armors])
        armor_value_data=([f'{armor.armor_value}' for armor in self.armors])
        dodge_data=(['{0:+}'.format(armor.dodge) for armor in self.armors])
        table.add_column("Armor",armor_data)
        table.add_column("Damage reduction",armor_value_data)
        table.add_column("Dodge Bonus/Penalty",dodge_data)
        print(table)

    def print_potions(self):
        table = PrettyTable()
        potion_data=([potion.description for potion in self.potions])
        stat_data=([f'{potion.stat}' for potion in self.potions])
        effect_data=(['{0:+}'.format(potion.effect) for potion in self.potions])
        table.add_column("Potion",potion_data)
        table.add_column("Stat",stat_data)
        table.add_column("Effect",effect_data)
        print(table)
    
    def inventory_options(self):
        exit_inventory = False
        while exit_inventory == False:
            inv_action=input("what would you like to do?(help for options): ")
            if inv_action == "help":
                print("list of available commands:")
                options=["examine","equip","use","inventory","exit"]
                for option in options:
                    print(option)
            elif inv_action.startswith("examine"):
                self.inv_examine(inv_action)
            elif inv_action.startswith("equip"):
                self.inv_equip(inv_action)
            elif inv_action.startswith("use"):
                self.inv_use(inv_action)
            elif inv_action == "exit":
                clear_console()
                exit_inventory=True
                print("exiting inventory")
            elif inv_action == "inventory":
                clear_console()
                exit_inventory=True
                self.display_inventory()
            else:
                print("please enter a valid option")


    def inv_examine(self,inv_action):
        examine_string=inv_action.split(" ", 1)
        if len(examine_string) > 1:
            examine_object=examine_string[1]
            item_list=[]
            for item in self.inventory:
                if item.description in item_list:
                    continue
                item_list.append(item.description)
                if examine_object == item.description:
                    print(item.details) 
            if examine_object not in item_list:
                print("You don't have one of those")

        else:
            print("choose an object to examine")
    
    def inv_equip(self, inv_action):
        equip_string=inv_action.split(" ", 1)
        if len(equip_string) > 1:
            equip_object=equip_string[1]
            item_list=[]
            for item in self.inventory:
                if item.description in item_list:
                    continue
                if equip_object == item.description:
                    if item.type == "weapon":
                        self.weapon=item
                        print(f'equipped {item.description}')
                    elif item.type == "armor":
                        self.armor=item
                        print(f'equipped {item.description}')
                    else:
                        print("you cant equip that")
                item_list.append(item.description)
            if equip_object not in item_list:
                print("You don't have one of those")
        else:
            print("choose an object to equip")

    def inv_use(self, inv_action):
        use_string=inv_action.split(" ", 1)
        if len(use_string) > 1:
            use_object=use_string[1]
            item_list=[]
            inventory_index=0
            for item in self.inventory:
                if item.description in item_list:
                    inventory_index+=1
                    continue
                if use_object == item.description:
                    if item.type == "potion":
                        self.inventory.pop(inventory_index)
                        self.potion_use(item)
                    else:
                        print("you cant use that right now")
                item_list.append(item.description)
                inventory_index+=1
            if use_object not in item_list:
                print("You don't have one of those")
        else:
            print("choose an object to use")
    
    def potion_use(self,potion):
        print(f'used {potion.description}')
        if potion.stat == "strength":
            self.strength+=potion.effect
            print(f"increased strength by {potion.effect}")
        if potion.stat == "agility":
            self.agility+=potion.effect
            print(f"increased agility by {potion.effect}")
        if potion.stat == "hp":
            self.hp+=potion.effect
            if self.hp > self.start_hp:
                self.hp = self.start_hp
            print("Restored hp")

    def status(self):
        weapon_table = PrettyTable()      
        print("Hit increases chance to hit an enemy") 
        weapon_table.add_column("Weapon",[self.weapon.description])
        weapon_table.add_column("Damage",[f'{self.weapon.damage[0]}-{self.weapon.damage[1]}'])
        weapon_table.add_column("Hit",['{0:+}'.format(self.weapon.hit)])
        print(weapon_table)
        print("Armor value reduces damage taken, Dodge reduces the chance to be hit")
        armor_table = PrettyTable()      
        armor_table.add_column("Armor",[self.armor.description])
        armor_table.add_column("Armor Value",[self.armor.armor_value])
        armor_table.add_column("Dodge",[self.armor.dodge])
        print(armor_table)
        stats_table = PrettyTable()      
        print("Strength increase damage, Agility increases hit and dodge")
        stats_table.add_column("HP",[f'{self.hp}/{self.start_hp}'])
        stats_table.add_column("Strength",[self.strength])
        stats_table.add_column("Strength",[self.agility])
        print(stats_table)

class Feature:
    def __init__(self, description,details, loot, locked):
        self.description=description
        self.details=details
        self.loot=loot
        self.locked=locked
    
    def examine(self,player):
        if self.locked == False:
            if len(self.loot) > 0:
                print("You find:")
                for items in self.loot:
                    print(items.description)
                take_items = input("take items?(yes/no)")
                if take_items == "yes":
                    for item in self.loot:
                        player.inventory.append(item)
                    self.loot=[]
                    print("you take the items")

            else:
                print("You find nothing")

def enter_room(rooms,room_number):
    '''
    initiate game state when the player enters a room
    '''
    clear_console()
    rooms[room_number].examine()
    rooms[room_number].visited=True
    start_turn(rooms, room_number)

def start_turn(rooms,room_number):
    room=rooms[room_number]
    monsters_attack(room)
    action=input('choose an action:')
    clear_console()
    choose_action(room,rooms, room_number,action)
    start_turn(rooms, room_number)
    
def monsters_attack(room):
    if room.battle_started == True and room.monster_action == True:
        for monster in room.monsters:
            monster.attack(room.player)

def choose_action(room,rooms,room_number,action):
    options=["examine","inventory","forwards","backwards","status","attack"]
    if action == "help":
        print("list of available commands:")
        for option in options:
            print(option)
        room.monster_action=False
    elif action.startswith("examine"):
        examine(room,action)
        room.monster_action=False
    elif action == "attack":
        if len(room.monsters) > 0:
            choose_target(room)
        else:
            print("There is nothing to attack")
    elif action == "forwards":
        if len(room.monsters) == 0:
            if room.door == "open":
                room_number+=1
                enter_room(rooms,room_number)
            else:
                check_door(rooms,room_number)
        else:
            print("You must clear the path first")
            room.monster_action=False
    elif action == "backwards":
        if room_number > 0:
            if len(room.monsters) == 0:
                room_number-=1
                enter_room(rooms,room_number)
            else:
                print("You don't run away from a fight!")
                room.monster_action=False
        else:
            print("You can only go forwards from here")
    elif action == "inventory":
        room.player.display_inventory()
        room.player.inventory_options()
    elif action == "status":
        room.player.status()
    else:
        print("Please choose a valid option (type 'help' for list of commands)")
        room.monster_action=False

def check_door(rooms,room_number):
    room=rooms[room_number]
    key_name=room.key_name
    items=[item for item in room.player.inventory]
    for item in items:
        if item.type == "key":
            if item.key_name == key_name:
                print(f"you unlock the door with the {item.description}")
                room.door="open"
                time.sleep(3)
                room_number += 1
                enter_room(rooms, room_number)
    print("The door is locked")

def examine(room,action):
    examine_options=["room"]
    examine_string=action.split(" ", 1)
    if len(examine_string) > 1:
        examine_object=examine_string[1]
        for monster in room.monsters:
            examine_options.append(monster.description)
            if examine_object==monster.description:
                print(monster.details)
        for item in room.items:
            examine_options.append(item.description)
            if examine_object==item.description:
                print(item.details)
        for feature in room.features:
            examine_options.append(feature.description)
            if examine_object==feature.description:
                print(feature.details)
                feature.examine(room.player)
        if examine_object=="room":
                room.examine()
        if examine_object not in examine_options:  
            print("You don't see that here(hint: try 'examine room')")   
    else:
        print("examine what?(hint: try 'examine room')")

def choose_target(room):
    target_index=1
    for monster in room.monsters:
        print(f'{target_index}: {monster.description} HP - {monster.hp}/{monster.start_hp  }')
        target_index+=1
    target_number = input('Enter a number to choose a target: ')
    try:
        target_number=int(target_number)
    except:
        clear_console()
        print('Please enter a number')
        return
    if target_number > 0 and target_number <= len (room.monsters):
        room.player.attack(room.monsters[target_number-1])
        room.battle_started=True
        room.monster_action=True
        kill_monster(room, target_number)   
    else:
        clear_console()
        print('Please pick a valid number')

def kill_monster(room, target_number):
    if room.monsters[target_number-1].hp == 0:
        print(f'{room.monsters[target_number-1].description} dies')
        dead_monster=room.monsters.pop(target_number-1)
        description=f'dead {dead_monster.description}'
        details="you examine the corpse"
        loot=dead_monster.loot
        corpse=Feature(description,details,loot,False)
        room.features.append(corpse)

def main ():
    #create items
    #armor
    no_armor = Armor("none","none", 0, 0)
    #weapons
    fists = Weapon("fists", "none", [1,2], 0)
    dagger = Weapon("dagger", "a small stabby weapon", [3,6], 1)
    club = Weapon("club", "a large blunt weapon", [10,12], -1)
    sword = Weapon("sword","a fine steel sword",[6,10],2)
    #potions
    healing_potion=Potion("healing potion","it is red and smells fruity", "hp",10)
    Super_healing_potion=Potion("super healing potion","really potent stuff", "hp",20)
    #keys
    rusty_key=Key("rusty key","It smells of goblin brew","prison_door")
    items=[]
    #initialise player
    player=Player("Alex", "A warrior", 25, 5, 5, no_armor, fists,[])
    #creat monsters
    drunk_goblin=Monster("goblin","The goblin looks very drunk", 10, 1, -5, no_armor,dagger,[rusty_key])
    troll=Monster("troll","Looks big, stupid and angry. It is carrying a big club.", 25, 5, -2, no_armor,club,[])
    monsters=[[drunk_goblin],[troll]]
    #create features
    chest=Feature("chest","the chest is made out of wood", [healing_potion],False)
    features=[[],[chest],[]]
    #create rooms
    room_descriptions = [
        "You have are in a underground jailcell, deep beneath the citadel." 
        "You hear footsteps outside, the door swings open and a drunk goblin"
        "stumbles into the cell. He is yelling something at you, but it is in goblin",
        "You stumble out of the cell, into the guard quarters, you are confronted with"
        "a large angry looking troll. "
    ]
    room_descriptions_visited = [
        "You are in a dark wet cell. There is a door to the east.",
        "You are in a dimly lit cave. It smells like trolls have been living here for a long time"
        ]
    rooms=[]
    rooms.append (Room(room_descriptions[0],room_descriptions_visited[0],player,monsters[0],items,features[0]))
    rooms[0].door="locked"
    rooms[0].key_name="prison_door"
    rooms.append (Room(room_descriptions[1],room_descriptions_visited[1],player,monsters[1],items,features[1]))
    room_number=0
    enter_room(rooms,room_number)

main()