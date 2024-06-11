import random as rnd
import os
from rich import print
from rich import pretty
pretty.install()
from prettytable import PrettyTable

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
class Room:
    def __init__(self,details,player,monsters,items,features):
        self.details=details
        self.player=player
        self.monsters=monsters
        self.items=items
        self.features=features
        self.battle_started=False
        self.monster_action=False

    def examine(self):
        print(self.details)
        print("You see:")
        for monster in self.monsters:
            print(f'a {monster.description}')
        for item in self.items:
            print(f'a {item.description}')
        for feature in self.features:
            print(f'a {feature.description}')

class Item:
    def __init__(self,description,details,item_type):
        self.description=description
        self.details=details
        self.type=item_type
    
    def examine(self):
        print(self.description)

class Weapon(Item):
    def __init__(self,description,details,item_type,damage,hit):
        Item.__init__(self,description,details,item_type)
        self.damage=damage
        self.hit=hit

class Armor(Item):
    def __init__(self,description,details,item_type,armor_value,dodge):
        Item.__init__(self,description,details,item_type)
        self.armor_value=armor_value
        self.dodge=dodge

class Potion(Item):
    def __init__(self,description,details,item_type,stat,effect):
        Item.__init__(self,description,details,item_type)
        self.stat=stat
        self.effect=effect
class Monster:
    def __init__(self,description,details,hp,strength,agility,armor,weapon):
        self.description=description
        self.details=details
        self.hp=int( (rnd.random()*hp + 2*hp)/3 )
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

    def loot(self):
        lootables=[]
        if self.armor.type != "none":
            lootables.append(self.armor)
        if self.weapon.type != "none":
            lootables.append(self.weapon)
        return lootables

class Player(Monster):
    def __init__(self,description,details,hp,strength,agility,armor,weapon):
        Monster.__init__(self,description,details,hp,strength,agility,armor,weapon)
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
            inv_action=input("examine/equip/use/exit: ")
            if inv_action.startswith("examine"):
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
                    if item.type == "armor":
                        self.armor=item
                        print(f'equipped {item.description}')
                    if item.type == "potion":
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
                        print("you cant use that")
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

class Feature:
    def __init__(self, description,details, loot, locked):
        self.description=description
        self.details=details
        self.loot=loot
        self.locked=locked
    
    def examine(self):
        if self.locked == False:
            if len(self.loot) > 0:
                print("You find:")
                for items in self.loot:
                    print(items.description)
                take_items = input("take items?(yes/no)")
                if take_items == "yes":
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
    start_turn(rooms, room_number)

def start_turn(rooms,room_number):
    room=rooms[room_number]
    monsters_attack(room)
    action=input('choose an action:')
    clear_console()
    options = check_options(room)
    choose_action(room,rooms, room_number,action,options)
    start_turn(rooms, room_number)
    
def monsters_attack(room):
    if room.battle_started == True and room.monster_action == True:
        for monster in room.monsters:
            monster.attack(room.player)

def check_options(room):
    options=["examine","inventory"]
    if len(room.monsters) == 0:
        options.append(["forwards","backwards"])
        if len(room.items) > 0:
            options.append("take")
    else:
        options.append("attack")
    return options

def choose_action(room,rooms,room_number,action,options):
    if action == "help":
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
            room_number+=1
            enter_room(rooms,room_number)
        else:
            print("You must clear the path first")
            room.monster_action=False
    elif action == "backwards":
        if len(room.monsters) == 0:
            room_number-=1
            enter_room(rooms,room_number)
        else:
            print("You don't run away from a fight!")
            room.monster_action=False
    elif action == "inventory":
        room.player.display_inventory()
        room.player.inventory_options()
    else:
        print("Please choose a valid option")
        for option in options:
            print(option)
        room.monster_action=False

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
                feature.examine()
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
        loot=dead_monster.loot()
        corpse=Feature(description,details,loot,False)
        room.features.append(corpse)

def main ():
    no_armor=Armor("none","none", "none", 0, 0)
    fists=Weapon("fists", "none", "none", [1,2], 0)
    dagger=Weapon("dagger", "a small stabby weapon", "weapon", [3,6], 1)
    club=Weapon("club", "a large blunt weapon", "weapon", [10,12], -1)
    healing_potion=Potion("healing potion","potion that restores hp", "potion", "hp",50)
    player=Player("Alex", "A warrior", 25, 5, 5, no_armor, fists)
    player.inventory=[dagger,dagger,healing_potion]
    drunk_goblin=Monster("goblin","a drunk goblin", 10, 1, -5, no_armor,dagger)
    drunk_goblin2=Monster("goblin","a drunk goblin", 10, 1, -5, no_armor,dagger)
    troll=Monster("troll","a large stupid oaf", 25, 5, -2, no_armor,club)
    chest=Feature("chest","a wooden chest", [dagger],False)
    features=[
        [chest],
        [],
        [chest]
    ]
    print(features)
    monsters=[]
    monsters=[
        [drunk_goblin,drunk_goblin2],
        [troll],
        []
    ]
    items=[]
    rooms=[]
    rooms.append (Room("This is the first room",player,monsters[0],items,features[0]))
    rooms.append (Room("This is the second room",player,monsters[1],items,features[1]))
    room_number=0
    enter_room(rooms,room_number)

main()