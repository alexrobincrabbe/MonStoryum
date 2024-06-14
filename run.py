import gspread
from google.oauth2.service_account import Credentials

import random as rnd
import os
from rich import print
from rich import pretty
from rich.theme import Theme
from rich.prompt import Prompt
from rich.console import Console
pretty.install()
from prettytable import PrettyTable
import time
import math
from operator import itemgetter, attrgetter

#my function imports
from hangman import hangman

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Hall_of_fame')

custom_theme= Theme({
    "info" : "grey62",
    "features" : "green",
    "monsters" : "red",
    "stat" : "bright_green",
    "option" : "blue",
    "items" : "turquoise2"
})
console=Console(theme=custom_theme)

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
        self.description="room"
        self.password=False

    def examine(self, player):
        clear_console()
        if self.visited == False:
            console.print(f'{self.details}',style="info")
        else:
            console.print(f'{self.details_visited}',style="info")
        print("You see:")
        for monster in self.monsters:
            console.print(f'{monster.description}',style="monsters")
        for item in self.items:
            console.print(f'{item.description}', style = "items")
        for feature in self.features:
            console.print(f'{feature.alt_description}',style="features")
    
class Item:
    def __init__(self,description,details):
        self.description=description
        self.details=details
    
    def examine(self, player):
        console.print(f'{self.details}', style = "info")

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
    def __init__(self,description,details,hp,strength,agility,armor,weapon,loot,speak):
        self.description=description
        self.details=details
        self.hp=int( math.ceil(rnd.random()*hp + 2*hp)/3 )
        self.start_hp=self.hp
        self.strength=strength
        self.agility=agility
        self.armor=armor
        self.weapon=weapon
        self.loot=loot
        self.speak = speak
        if self.armor.details != "none":
            self.loot.append(self.armor)
        if self.weapon.details != "none":
            self.loot.append(self.weapon)
    
    def attack(self,target):
        time.sleep(0.7)
        print(f'[blue]{self.description}[/blue] attacks [blue]{target.description}[/blue]...')
        time.sleep(0.7)
        hit=self.agility+self.weapon.hit + (rnd.random()*15)
        dodge=target.agility + target.armor.dodge + (rnd.random()*15)
        if hit > dodge:
            damage=self.strength + rnd.randrange(self.weapon.damage[0],self.weapon.damage[1]+1) - target.armor.armor_value
            damage = 1 if damage < 1 else damage
            print(f'[blue]{self.description}[/blue] hits for [red1]{damage}[/red1] points of damage')
            target.hp-=damage
            target.hp = 0 if target.hp < 0 else target.hp
            print(f'[blue]{target.description}[/blue] has '
                  f'[green1]{target.hp}[/green1]/[chartreuse4]{target.start_hp}[/chartreuse4] remaining')
            

        else:
            print(f'[blue]{self.description}[/blue] misses')

    def examine(self,player):
        console.print(f'{self.details}', style = "info")
    
    def talk(self,room):
        console.print(f'{self.speak}', style = "info")
        
class Dragon(Monster):
    def __init__(self,description,details,hp,strength,agility,armor,weapon,loot,speak):
        Monster.__init__(self,description,details,hp,strength,agility,armor,weapon,loot,speak)

    def talk(self,room):
        print(
            "The dragon looks up at you, and raises it's enormous head."
            "'I will allow you to pass if you solve a riddle'"
            )
        while True:
            answer = Prompt.ask("[chartreuse4] 'would you like to play?'[/chartreuse4] (yes/no)")
            if answer == "yes" or answer == "y":
                print (" 'Very well, the rules of the game are simple:' \n"
                    " 'You must guess the letters of a word. For each"
                    "correct guess, I will reveal one letter."
                    "if you guess the word, I will allow you to pass.' \n"
                    " 'if you guess wrong 5 times, I will eat you' ")
                break
            if answer == "no" or answer == "n":
                print(" 'very well' ")
                print("the dragon returns to its slumber")
                return
        while True:
            answer_2 = Prompt.ask (" [chartreuse4]'are you you sure you want to play?'[/chartreuse4] (yes/no) ")
            if answer_2 == "yes" or answer_2 == "y":
                break
            if answer_2 == "no" or answer_2 == "n":
                print(" 'very well' ")
                print("the dragon returns to its slumber")
                return
        win = hangman()
        if win == False:
            print(" 'disappointing...' ")
            room.monster_action = True
            room.battle_started = True
        else:
            room.password = True
            print(" 'very well...I will allow you to pass' ")
            print("the dragon returns to its slumber")

            
class Player(Monster):
    def __init__(self,description,details,hp,strength,agility,armor,weapon,loot,speak):
        Monster.__init__(self,description,details,hp,strength,agility,armor,weapon,loot,speak)
        self.inventory=loot
        self.room_reached=0
        self.dragon_killed=False
        
    def display_inventory(self):
        self.weapons = []
        self.armors = []
        self.potions = []
        self.keys = []
        for item in self.inventory:
            if item.type == "weapon":
                self.weapons.append(item)
            if item.type == "armor":
                self.armors.append(item)
            if item.type == "potion":
                self.potions.append(item)
            if item.type == "key":
                self.keys.append(item)
        
        self.print_weapons()
        self.print_armor()
        self.print_potions()
        self.print_keys()

    def print_weapons(self):
        table = PrettyTable()
        weapon_data=([weapon.description for weapon in self.weapons])
        damage_data=([f'{weapon.damage[0]}-{weapon.damage[1]}' for weapon in self.weapons])
        hit_data=(['{0:+}'.format(weapon.hit) for weapon in self.weapons])
        table.add_column("Weapons",weapon_data)
        table.add_column("Damage",damage_data)
        table.add_column("Hit bonus",hit_data)
        console.print(table,style="purple")

    def print_armor(self):
        table = PrettyTable()
        armor_data=([armor.description for armor in self.armors])
        armor_value_data=([f'{armor.armor_value}' for armor in self.armors])
        dodge_data=(['{0:+}'.format(armor.dodge) for armor in self.armors])
        table.add_column("Armor",armor_data)
        table.add_column("Damage reduction",armor_value_data)
        table.add_column("Dodge Bonus/Penalty",dodge_data)
        console.print(table,style="blue")

    def print_potions(self):
        table = PrettyTable()
        potion_data=([potion.description for potion in self.potions])
        stat_data=([f'{potion.stat}' for potion in self.potions])
        effect_data=(['{0:+}'.format(potion.effect) for potion in self.potions])
        table.add_column("Potion",potion_data)
        table.add_column("Stat",stat_data)
        table.add_column("Effect",effect_data)
        console.print(table,style="green")

    def print_keys(self):
        key_string=""
        for key in self.keys:
            key_string+=f'{key.description}, '
        if len(key_string) >= 2:
            key_string = key_string[:-2]
        print(f'Keys : [turquoise2]{key_string}[/turquoise2]')

    
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
                        print(f'[blue]{self.description}[/blue] equipped [green]{item.description}[/green]')
                        return True
                    elif item.type == "armor":
                        self.armor=item
                        print(f'equipped {item.description}')
                        return True
                    else:
                        print("you cant equip that")
                        return False
                item_list.append(item.description)
            if equip_object not in item_list:
                print("You don't have one of those")
                return False
        else:
            print("choose an object to equip")
            return False

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
                        return True
                    else:
                        print("you cant use that right now")
                        return False
                item_list.append(item.description)
                inventory_index+=1
            if use_object not in item_list:
                print("You don't have one of those")
                return False
        else:
            print("choose an object to use")
            return False
    
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
        console.print(weapon_table,style="red")
        print("Armor value reduces damage taken, Dodge reduces the chance to be hit")
        armor_table = PrettyTable()      
        armor_table.add_column("Armor",[self.armor.description])
        armor_table.add_column("Armor Value",[self.armor.armor_value])
        armor_table.add_column("Dodge",[self.armor.dodge])
        console.print(armor_table,style="cyan")
        stats_table = PrettyTable()      
        print("Strength increase damage, Agility increases hit and dodge")
        stats_table.add_column("HP",[f'{self.hp}/{self.start_hp}'])
        stats_table.add_column("Strength",[self.strength])
        stats_table.add_column("Strength",[self.agility])
        console.print(stats_table,style="orange1")

class Feature:
    def __init__(self, description,details, loot, locked):
        self.description=description
        self.details=details
        self.loot=loot
        self.locked=locked
        self.alt_description = description
    
    def examine(self,player):
        console.print(f'{self.details}', style = "info")
        if self.locked == True:
            self.check_locked(player)
        if self.locked == False:
            if len(self.loot) > 0:
                print("You find:")
                for items in self.loot:
                    print(f'[turquoise2]{items.description}[/turquoise2]')
                while True:
                    take_items = Prompt.ask(f"[gold3]take items?(yes/no)[/gold3]")
                    if take_items == "yes" or take_items =="y":
                        for item in self.loot:
                            player.inventory.append(item)
                        self.loot=[]
                        print(f"[chartreuse4]you take the items[/chartreuse4]")
                        break
                    if take_items == "no" or take_items == "n":
                        print("[chartreuse4]You leave the items[/chartreuse4]")
                        break

            else:
                print("You find nothing")
        else:
            print("it is locked")
    
    def check_locked(self,player):
        items=[item for item in player.inventory]
        for item in items:
            if item.type == "key":
                if item.key_name == self.description:
                    print(f"you unlock the {self.description} with the {item.description}")
                    self.locked=False
                    time.sleep(1.5)

def enter_room(rooms,room_number):
    '''
    initiate game state when the player enters a room
    '''
    if rooms[room_number].player.room_reached < room_number+1:
        rooms[room_number].player.room_reached = room_number+1
    rooms[room_number].examine(rooms[room_number].player)
    rooms[room_number].visited=True
    start_turn(rooms, room_number)

def start_turn(rooms,room_number):
    room=rooms[room_number]
    monsters_attack(room)
    action = Prompt.ask("[gold3]choose an action[/gold3] (type 'help' for options) ")
    choose_action(room,rooms, room_number,action)
    start_turn(rooms, room_number)
    
def monsters_attack(room):
    if room.battle_started == True and room.monster_action == True:
        for monster in room.monsters:
            monster.attack(room.player)
            if room.player.hp < 1:
                print("you died")
                killed_by=monster.description
                lose_game(room,killed_by)

def lose_game(room,killed_by):
    escaped = "no"
    time.sleep(3)
    print("GAME OVER")
    results(room,killed_by,escaped)


def win_game(room):
    if room.player.dragon_killed == False:
        print(
            "You can escape the dungeon now, however the dragon is still "
            "back there in the dungeon")
        while True:
            answer = Prompt.ask( "[gold3]Are you sure you want to leave? [gold3](yes/no)")
            if answer == "yes" or answer == "y":
                break
            if answer == "no" or answer == "n":
                room
                return
    clear_console()
    time.sleep(1)
    print('Congratulations! you escaped the dungeon!')
    escaped= "yes"
    killed_by = "survived"
    results(room, killed_by, escaped)

def results(room,killed_by,escaped):
    if "gold medallion" in [item.description for item in room.player.inventory]:
        gold_medallion = "yes"
    else:
        gold_medallion = "no"
    results = (room.player.description,room.player.room_reached,killed_by,escaped,gold_medallion)
    hof=SHEET.worksheet('Sheet1')
    hof.append_row(results)
    see_HOF = Prompt.ask("[chartreuse4]See Hall of Fame? (yes/no)[/chartreuse4]")
    while True:
        if see_HOF == "yes" or see_HOF == "y":
            show_HOF()
            break
        if see_HOF == "no" or see_HOF == "n":
            break
    Prompt.ask("[chartreuse4]press enter to restart[/chartreuse4]")
    main()

def show_HOF():
    hall_of_fame=SHEET.worksheet('Sheet1')
    HOF = hall_of_fame.get_all_values()
    HOF.pop(0)
    for row in HOF:
        row[1]=int(row[1])

    HOF.sort(key=itemgetter(4,3,1),reverse=True)
    table = PrettyTable()
    table.field_names=["NAME", "ROOM REACHED", "KILLED BY", "ESCAPED" ,"GOLD MEDALLION"]
    for row in HOF:
        table.add_row(row)
    
    console.print(table,style="purple")




def choose_action(room,rooms,room_number,action):
    options=["examine","inventory","forwards","backwards","status","attack","equip","use","talk"]
    if action == "help":
        print("list of available commands:")
        for option in options:
            console.print(option,style="info")
        room.monster_action=False
    elif action.startswith("examine"):
        examine(room,action)
    elif action.startswith("take"):
        take(room, action)
    elif action.startswith("talk"):
        talk(room,action)
    elif action.startswith("attack"):
        if len(room.monsters) > 0:
            choose_target(room,action)
        else:
            print("There is nothing to attack")
    elif action == "forwards":
        if len(room.monsters) == 0 or room.password == True:
            if room.door == "open":
                if room.password == True and len(room.monsters) > 0:
                    print("the dragon allows you to pass")
                    time.sleep(2)
                room_number+=1
                if room_number == 11:
                    room_number = 10
                    win_game(room)
                enter_room(rooms,room_number)
            else:
                check_door(rooms,room_number)
        else:
            console.print("You must clear the path first", style = "info")
            room.monster_action=False
    elif action == "backwards":
        if room_number > 0:
            if len(room.monsters) == 0 or room_number == 5:
                room_number-=1
                enter_room(rooms,room_number)
            else:
                console.print("You don't run away from a fight!", style = "info")
                room.monster_action=False
        else:
            console.print("You can only go forwards from here", style = "info")
    elif action == "inventory":
        room.player.display_inventory()
        room.monster_action = False
    elif action == "status":
        room.player.status()  
        room.monster_action = False
    elif action.startswith("equip"):
        room.monster_action = room.player.inv_equip(action)
    elif action.startswith("use"):
       room.monster_action = room.player.inv_use(action)
    else:
        console.print("Please choose a valid option (type 'help' for list of commands)", style = "info")
        room.monster_action=False


def take(room, action):
    take_string=action.split(" ", 1)
    if len(take_string) > 1:
        item_string=take_string[1]
    else:
        console.print("take what? (hint: try 'take <name>')", style = "info")
        room.monster_action = False
        return
    if item_string in [item.description for item in room.items]:
        if len(room.monsters) > 0:
            print("you can't reach that right now")
        else:
            for item in room.items:
                if item_string == item.description:
                    room.items.pop(room.items.index(item))
                    room.player.inventory.append(item)
                    print(f'you take the [turquoise2]{item.description}[/turquoise2]')
    else:
        console.print("You don't see that here", style = "info")
        room.monster_action = False


def talk(room, action):
    talk_string=action.split(" ", 2)
    if len(talk_string) > 2:
        monster_string=talk_string[2]
    else:
        console.print("talk to what? (hint: try 'talk to <name>')", style = "info")
        room.monster_action=False
        return
    for monster in room.monsters:
        if monster.description == monster_string:
            monster.talk(room)
            room.monster_action = True
            return
    console.print("talk to what?", style = "info")

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

def examine (room,action):
    examinables=[room]
    examine_string=action.split(" ", 1)
    if len(examine_string) > 1:
        examine_object=examine_string[1]
    else:
        console. print("examine what? (hint: try 'examine room')", style = "info")
        room.monster_action=False
        return
    for item in room.items:
        examinables.append(item)
    for monster in room.monsters:
        examinables.append(monster)
    for feature in room.features:
        examinables.append(feature)
    for item in room.player.inventory:
        examinables.append(item)
    count = [examinable.description for examinable in examinables].count(examine_object)
    if count == 0:
        console.print("you don't see that", style = "info")
        room.monster_action=False
        return
    if count == 1:
        room.monster_action = True
        for examinable in examinables:
            if examinable.description == examine_object:
                examinable.examine(room.player)
    else:
        #print numbered list of options
        object_dic = examine_list(examinables,examine_object)
        #select object to examine from list
        object_selected=False
        while object_selected == False:
            object_selected , object_select = choose_object_number(room, count)

        object_index=object_dic.get(object_select)
        examinables[object_index].examine(room.player)

def examine_list(examinables, examine_object):
    examine_number=0
    examine_index=-1
    examine_dic={}
    for  examinable in examinables:
        examine_index+=1
        if examinable.description == examine_object:
            examine_number+=1
            print(f'{examine_number}: {examinable.description}')
            examine_dic[examine_number]=examine_index
    return examine_dic

def choose_object_number(room, object_count):
    object_select = input('Enter a number to choose which item to examine: ')
    try:
        object_select=int(object_select)
        object_selected=True
    except:
        console.print('Please enter a number', style = "info")
        room.monster_action=False
        object_selected=False
    else:
        if object_select < 1 or object_select > object_count:
            room.monster_action=False
            object_selected=False
            console.print('Please pick a valid number', stlye = "info") 
    return object_selected,object_select
    

def choose_target(room,action):
    target_string = action.split(" ", 1)
    #user specifies target
    if len(target_string) > 1:
        target = target_string[1]
        monsters = [monster.description for monster in room.monsters]
        target_count=monsters.count(target)
        if target_count == 1:
            target_index = 0
            for monster in room.monsters:
                if monster.description == target:
                    attack_monster(room, target_index)
                target_index+=1
            #there is only one target, skip target selection
            return 
        elif target_count > 1:
            target_dic = target_list(room,target)
        else:
            room.monster_action=False
            console.print("attack what?", style = "info")
            return 
    #no target specified
    else:
        target = False
        target_dic = target_list(room, target)
        target_count=len(target_dic)
    #select target number from list
    target_selected=False
    while target_selected == False:
        target_selected , target_select = choose_target_number(room,target_selected,target_count)

    target_index=target_dic.get(target_select)
    attack_monster(room, target_index) 

def attack_monster(room,target_index):
    room.player.attack(room.monsters[target_index])
    room.battle_started=True
    room.monster_action=True
    kill_monster(room, target_index)  

def target_list(room,target):
    target_number=0
    target_index=-1
    target_dic={}
    for monster in room.monsters:
        target_index+=1
        if monster.description == (target) or target == False:
            target_number+=1
            print(f'[bright_white]{target_number}[/bright_white]: [red1]{monster.description}[/red1] HP - [green1]{monster.hp}[/green1]/[chartreuse4]{monster.start_hp}[/chartreuse4]')
            target_dic[target_number]=target_index
    return target_dic

def choose_target_number(room,target_selected,target_count):
    target_select = Prompt.ask(f'[gold3]Enter a number to choose a target: [/gold3]')
    try:
        target_select=int(target_select)
        target_selected=True
    except:
        print('Please enter a number')
        room.monster_action=False
        target_selected=False
    else:
        if target_select < 1 or target_select > target_count:
            room.monster_action=False
            target_selected=False
            print('Please pick a valid number') 
    return target_selected,target_select

def kill_monster(room, target_index):
    if room.monsters[target_index].hp == 0:
        time.sleep(1)
        console.print(f'{room.monsters[target_index].description} dies',style="red")
        if room.monsters[target_index].description == "dragon":
            room.player.dragon_killed = True
        dead_monster=room.monsters.pop(target_index)
        description=f'dead {dead_monster.description}'
        details="you examine the corpse"
        loot=dead_monster.loot
        corpse=Feature(description,details,loot,False)
        corpse.description = f'{dead_monster.description}'
        room.features.append(corpse)

def choose_name():
    clear_console()
    name = input("please choose your name: ")
    if len(name) > 10:
        print("maximum of 10 characters")
        choose_name()
    else:
        return name
    
def main ():
    #create items
    #armor
    no_armor = Armor("none","none", 0, 0)
    rusty_armour= Armor("rusty armor", "it has seen better days",2,-1)
    leather_armor = Armor("leather armor", "it is light, and offers some protection",3,0)
    plate_armor = Armor("plate armor", "it is heavy, but offers good protection",5,-1)
    dragonscale_armor = Armor("dragonscale armor", "it glistens",10,1)
    scales = Armor("none", "none",10,0)
    stone_skin = Armor("none", "none", 5, -2)
    #weapons
    fists = Weapon("fists", "none", [1,2], 0)
    dagger = Weapon("dagger", "a small stabby weapon", [1,6], 1)
    club = Weapon("club", "a large blunt weapon", [2,10], -1)
    sword = Weapon("sword","a fine steel sword",[1,10],2)
    silver_sword = Weapon("silver sword","a shiny silver sword",[2,12],3)
    dragon_lance = Weapon("dragon lance", "it glistens", [10,25],4)
    stinger = Weapon("stinger", "none", [1,1], 0)
    claws = Weapon("claws","none",[20,30],5)
    bite= Weapon("bite","none",[4,9],4)
    stone_fists = Weapon("fists", "none", [5,15],4)
    #potions
    healing_potion = Potion("healing potion","it is red and smells fruity", "hp",10)
    Super_healing_potion = Potion("super healing potion","really potent stuff", "hp",20)
    agility_potion = Potion("agility potion", "it is green and sticky","agility",3)
    strength_potion = Potion("strength potion", "orange and bubbly", "strength",2)
    #keys
    rusty_key=Key("rusty key","It smells of goblin brew","prison_door")
    bronze_key=Key("bronze key","It is dusty","bronze chest")
    silver_key=Key("silver key","It is shiny","silver chest")
    golden_key=Key("golden key","It has strange markings","golden chest")
    gold_medallion = Key("gold medallion", "it is proof that you killed the dragon", "none")

    items=[
        [],#1
        [],#2
        [],#3
        [],#4
        [],#5
        [],#6
        [],#7
        [],#8
        [],#9
        [plate_armor],#10
        [dragon_lance]#11
    ]

    #initialise player
    name = choose_name()
    player=Player(name, "A warrior", 25, 3, 4, dragonscale_armor, dragon_lance,[Super_healing_potion,Super_healing_potion],"")
    player.hp=20
    player.start_hp=20
    #creat monsters
    g_speak = "it is probably swearing at you, but you don't understand goblin"
    dg_details = "The goblin looks very drunk"
    g_details = "goblins are funny looking creatures"
    t_speak = "it grunts at you"
    t_details = "Looks big, stupid and angry. It is carrying a big club."
    s_speak = "it hisses at you"
    s_details = "it is creepy"
    sg_speak = "it remains silent"
    sg_details ="it is a living statue, made of pure stone"
    d_details = "it is huge and scaly"
    d_speak = ""
    w_details = "it has really big teeth"
    w_speak = "it is not a talking wolf"
    drunk_goblin=Monster("goblin",dg_details, 10, 1, -10, no_armor,dagger,[rusty_key],g_speak)
    trolls = []
    for i in range (3):
        trolls.append(Monster("troll",t_details, 20, 2, -4, no_armor,club,[],t_speak))
    goblins =[]
    for i in range (5):
        goblins.append(Monster("goblin", g_details, 10, 1, 0, no_armor,dagger,[],g_speak))
    goblin_captain=Monster("goblin captain",g_details, 13, 1, 0, leather_armor,sword,[],g_speak)
    dragon=Dragon("dragon", d_details,100,0,0,scales,claws,[gold_medallion],d_speak)
    wolves=[]
    for i in range(2):
        wolves.append(Monster("wolf", w_details, 20,0,0, no_armor,bite, [], w_speak))

    stone_guardian = Monster("stone guardian", sg_details, 50, 0, 0, stone_skin,stone_fists,[golden_key],sg_speak)
    spiders=[]
    for i in range(5):
        spiders.append(Monster("spider",s_details, 1,0,0,no_armor,stinger,[],s_speak))

    monsters=[
        [drunk_goblin],#1
        [trolls[0]],#2
        [],#3
        [spider for spider in spiders],#4
        [],#5
        [dragon],#6
        [goblins[0],goblins[1],goblin_captain],#7
        [trolls[1],goblins[2],goblins[3]],#8
        [],#9
        [trolls[2], goblins[4],wolves[0],wolves[1]],#10
        [stone_guardian]#11
    ]

    #create features
    wooden_chest_0=Feature("wooden chest","the chest is old and shabby", [healing_potion],False)
    bronze_chest=Feature("bronze chest","the chest is dusty", [healing_potion,strength_potion, agility_potion],True)
    silver_chest=Feature("silver chest","the chest is smooth and shiny", [silver_sword,healing_potion],True)
    golden_chest=Feature("golden chest","the chest has strange markings on it", [dragonscale_armor,Super_healing_potion],True)
    spider_egg=Feature("egg","it is wet and slimey",[],False)
    spider_egg_2=Feature("egg","it is wet and slimey",[bronze_key],False)
    well=Feature("well", "You can't see the bottom",[rusty_armour],False)
    wooden_chest = Feature("wooden chest","goblins like to store there stuff in chests", [Super_healing_potion],False)
    table = Feature ("table", "it has goblin brew stains all over it",[silver_key],False)
    bag_of_potions = Feature("bag of potions","someone left this here for Leda",[Super_healing_potion,Super_healing_potion,Super_healing_potion],False)
    features=[
        [],#1
        [],#2
        [wooden_chest_0, bronze_chest, silver_chest, golden_chest],#3
        [spider_egg,spider_egg_2,spider_egg],#4
        [well],#5
        [],#6
        [wooden_chest],#7
        [table],#8
        [bag_of_potions],#9
        [],#10
        []#11
        ]
    #create rooms
    room_descriptions = [
        "Regaining consciousness, you open your eyes and realise you are in a dark, "
        "dank-smelling dungeon. From the faint sounds above you, you realise you are " 
        "in the depths of the citadel, controlled by the evil sorceress queen, Achlys. "
        "It dawns on you that by wrongfully imprisoning you, Achlys has removed the "
        "last obstacle to her malicious schemes. You must find a way to escape, "
        "though you know that her loyal monsters will fight you to the death. "
        "The innocent citizens of Greystorm will be counting on you to "
        "save them. "
        "You hear clumsy, heavy footsteps approaching your cell, "
        "the door creaks open and an evidently inebriated goblin stumbles in. "
        "You reach for your weapon but…your scabbard is empty. "
        "He begins to berate you, but you don’t know what he’s saying - "
        "you don’t speak Goblish. "
        "He lunges towards you and you see a dagger in his gnarly hand: ",#1

        "You lurch out of your cell and find yourself in the guard quarters. "
        "You are confronted by a large troll. He glares angrily at you.",#2

        "Leaving the troll’s lifeless body behind, you enter a small room. "
        "You hear water dripping. In the dim light, cast by a torch high "
        "up on the wall, you spy four chests; one wooden, one bronze, one "
        "silver, one gold..",#3

        "You stagger down a narrow corridor and spot a gap in the walls. "
        "You feel your way carefully through the gap, along jagged rock "
        "walls until you edge your way into an opening. You feel "
        "something enshroud your face, sticking to you, pulling at you. "
        "You reach out with your hands and desperately rip it away. You "
        "look down and see three big white egg sacs. They seem to be wriggling. "
        "You look up and see thick webs and dark shapes moving hurriedly "
        "across the ceiling. Dozens of glowing, hungry eyes are fixed on you.", #4

        "You enter a small cave. There is a well in the center of the room",#5

        "You find yourself in another cavern, this time it’s huge. There is "
        "a large stone bridge.  Standing in the middle is an enormous, yellow-eyed "
        "dragon.\n\nThe dragon looks curiously at you and lowers its scaly head.",#6

        "You hurry past the dragon, down a passageway. You dash through the next "
        "unlocked door you find and are met by a trio of goblins, one appears to "
        "be in charge. They grunt at you.",#7

        "You see two goblins and a troll sitting around a table. They look annoyed that you"
        "disturbed them",#8

        "room 9",#9
        "hi leda",#10
        "You have reached the final room. Ahead of you is the exit of the dungeon."
        "Daylight dazzles your eyes. In your path stands a stone guardian"#11 
    ]
    room_descriptions_visited = [
        "You are in a dark wet cell. There is a door to the east.",
        "You are in a dimly lit cave. It smells like trolls have been living here for a long time",
        "You are in a small cave with a well at the center of the room",
        "You are in a cavern, webs cover the walls and ceiling.",
        "room 5",
        "room 6",
        "room 7",
        "room 8",
        "room 9",
        "room 10",
        "room 11"
        ]
    
    #create rooms
    rooms=[]
    for i in range(11):
        rooms.append (Room(room_descriptions[i],room_descriptions_visited[i],player,monsters[i],items[i],features[i]))
    
    rooms[0].door="locked"
    rooms[0].key_name="prison_door"
    rooms[0].monster_action = True
    rooms[0].battle_started = True
    rooms[5].password=True

    room_number=5
    enter_room(rooms,room_number)
main()