import random as rnd
import os
from rich import print
from rich import pretty
from rich.theme import Theme
from rich.console import Console
pretty.install()
from prettytable import PrettyTable
import time
import math

custom_theme= Theme({
    "features": "green",
    "monsters": "red",
    "stat": "bright_green",
    "option": "blue",
    "header": "blue"
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
            print(self.details)
        else:
            print(self.details_visited)
        print("You see:")
        for monster in self.monsters:
            console.print(f'{monster.description}',style="monsters")
        for item in self.items:
            console.print(f'{item.description}')
        for feature in self.features:
            console.print(f'{feature.description}',style="features")
    
class Item:
    def __init__(self,description,details):
        self.description=description
        self.details=details
    
    def examine(self, player):
        print(self.details)

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
        time.sleep(1)
        print(f'[blue]{self.description}[/blue] attacks [blue]{target.description}[/blue]...')
        time.sleep(1)
        hit=self.agility+self.weapon.hit + (rnd.random()*10)
        dodge=target.agility + target.armor.dodge + (rnd.random()*10)
        if hit > dodge:
            damage=self.strength + rnd.randrange(self.weapon.damage[0],self.weapon.damage[1]+1) - target.armor.armor_value
            damage = 1 if damage < 1 else damage
            print(f'{self.description} hits for [red]{damage}[/red] points of damage')
            target.hp-=damage
            target.hp = 0 if target.hp < 0 else target.hp
        else:
            print(f'{self.description} misses')

    def examine(self,player):
        print(self.details)
    
    def talk(self):
        print(self.speak)
        
class Player(Monster):
    def __init__(self,description,details,hp,strength,agility,armor,weapon,loot,speak):
        Monster.__init__(self,description,details,hp,strength,agility,armor,weapon,loot,speak)
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
    
    def examine(self,player):
        print(self.details)
        if self.locked == True:
            self.check_locked(player)
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
    rooms[room_number].examine(rooms[room_number].player)
    rooms[room_number].visited=True
    start_turn(rooms, room_number)

def start_turn(rooms,room_number):
    room=rooms[room_number]
    monsters_attack(room)
    action=input('choose an action:')
    choose_action(room,rooms, room_number,action)
    start_turn(rooms, room_number)
    
def monsters_attack(room):
    if room.battle_started == True and room.monster_action == True:
        for monster in room.monsters:
            monster.attack(room.player)

def choose_action(room,rooms,room_number,action):
    options=["examine","inventory","forwards","backwards","status","attack","equip","use","talk"]
    if action == "help":
        print("list of available commands:")
        for option in options:
            console.print(option,style="option")
        room.monster_action=False
    elif action.startswith("examine"):
        room.monster_action=examine(room,action)
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
                if room.password == True:
                    print("the dragon allows you to pass")
                    time.sleep(2)
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
        room.monster_action = False
    elif action == "status":
        room.player.status()  
        room.monster_action = False
    elif action.startswith("equip"):
        room.monster_action = room.player.inv_equip(action)
    elif action.startswith("use"):
       room.monster_action = room.player.inv_use(action)
    else:
        print("Please choose a valid option (type 'help' for list of commands)")
        room.monster_action=False

def talk(room, action):
    talk_string=action.split(" ", 2)
    if len(talk_string) > 2:
        monster_string=talk_string[2]
    else:
        print("talk to what (hint: try 'talk to <name>')")
        room.monster_action=False
        return
    for monster in room.monsters:
        if monster.description == monster_string:
            monster.talk()
            return
    print("talk to what?")

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
        print("examine what? (hint: try 'examine room')")
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
        print("you don't see that")
        room.monster_action=False
        return
    if count == 1:
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
        print('Please enter a number')
        room.monster_action=False
        object_selected=False
    else:
        if object_select < 1 or object_select > object_count:
            room.monster_action=False
            object_selected=False
            print('Please pick a valid number') 
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
            print("attack what?")
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
            print(f'{target_number}: {monster.description} HP - {monster.hp}/{monster.start_hp  }')
            target_dic[target_number]=target_index
    return target_dic

def choose_target_number(room,target_selected,target_count):
    target_select = input('Enter a number to choose a target: ')
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
        dead_monster=room.monsters.pop(target_index)
        description=f'dead {dead_monster.description}'
        details="you examine the corpse"
        loot=dead_monster.loot
        corpse=Feature(description,details,loot,False)
        room.features.append(corpse)

def main ():
    #create items
    #armor
    no_armor = Armor("none","none", 0, 0)
    leather_armor = Armor("leather armor", "it is light, and offers some protection",1,0)
    plate_armor = Armor("plate armor", "it is heavy, but offers good protection",2,-1)
    dragonscale_armor = Armor("dragonscale armor", "it glistens",10,1)
    scales = Armor("none", "none",10,0)
    stone_skin = Armor("none", "none", 5, -2)
    #weapons
    stinger = Weapon("stinger", "none", [1,1], 0)
    fists = Weapon("fists", "none", [1,2], 0)
    dagger = Weapon("dagger", "a small stabby weapon", [3,6], 1)
    club = Weapon("club", "a large blunt weapon", [6,12], -1)
    nimble_sword = Weapon("sword","a fine steel sword",[6,10],2)
    dragon_lance = Weapon("dragon lance", "it glistens", [20,25],3)
    claws = Weapon("claws","none",[20,25],0)
    bite= Weapon("bite","none",[7,10],0)
    stone_fists = Weapon("fists", "none", [8,15],0)
    #potions
    healing_potion = Potion("healing potion","it is red and smells fruity", "hp",10)
    Super_healing_potion = Potion("super healing potion","really potent stuff", "hp",20)
    agility_potion = Potion("agility potion", "it is green and sticky","agility",1)
    strength_potion = Potion("strength potion", "orange and bubbly", "strength",1)
    #keys
    rusty_key=Key("rusty key","It smells of goblin brew","prison_door")
    bronze_key=Key("bronze key","It is dusty","bronze chest")
    silver_key=Key("silver key","It is shiny","silver chest")
    golden_key=Key("golden key","It has strange markings","golden chest")

    items=[
        [],#1
        [],#2
        [],#3
        [],#4
        [],#5
        [],#6
        [],#7
        [],#8
        [plate_armor],#9
        [dragon_lance]#10
    ]

    #initialise player
    player=Player("Alex", "A warrior", 25, 100, 100, no_armor, fists,[],"")

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
    drunk_goblin=Monster("goblin",dg_details, 10, 1, -6, no_armor,dagger,[rusty_key],g_speak)
    trolls = []
    for i in range (3):
        trolls.append(Monster("troll",t_details, 25, 2, -1, no_armor,club,[],t_speak))
    goblins =[]
    for i in range (5):
        goblins.append(Monster("goblin", g_details, 10, 1, 0, no_armor,dagger,[],g_speak))
    goblin_captain=Monster("goblin captain",g_details, 13, 1, 0, leather_armor,nimble_sword,[],g_speak)
    dragon=Monster("dragon", d_details,100,0,0,scales,claws,[],d_speak)
    wolf = Monster("wolf", w_details, 10,0,1, no_armor,bite, [], w_speak)
    stone_guardian = Monster("stone guardian", sg_details, 30, 0, 0, stone_skin,stone_fists,[golden_key],sg_speak)
    spiders=[]
    for i in range(5):
        spiders.append(Monster("spider",s_details, 1,1,0,no_armor,stinger,[],s_speak))

    monsters=[
        [drunk_goblin],#1
        [trolls[0]],#2
        [],#3
        [spider for spider in spiders],#4
        [],#5
        [dragon],#6
        [goblins[0],goblins[1],goblin_captain],#7
        [trolls[1],goblins[2],goblins[3]],#8
        [trolls[2], goblins[4],wolf,wolf],#9
        [stone_guardian]#10
    ]

    #create features
    bronze_chest=Feature("bronze chest","the chest is dusty", [healing_potion],True)
    silver_chest=Feature("silver chest","the chest is smooth and shiny", [healing_potion],True)
    golden_chest=Feature("golden chest","the chest has strange markings on it", [healing_potion],True)
    spider_egg=Feature("egg","it is wet and slimey",[],False)
    spider_egg_2=Feature("egg","it is wet and slimey",[bronze_key],False)
    well=Feature("well", "You can't see the bottom",[],False)
    wooden_chest = Feature("wooden chest","goblins like to store there stuff in chests", [Super_healing_potion],False)
    table = Feature ("table", "it has goblin brew stains all over it",[silver_key],False)
    features=[
        [],#1
        [],#2
        [bronze_chest, silver_chest, golden_chest],#3
        [spider_egg,spider_egg_2,spider_egg],#4
        [well],#5
        [],#6
        [wooden_chest],#7
        [table],#8
        [],#9
        []#10
        ]
    #create rooms
    room_descriptions = [
        "You have are in a underground jailcell, deep beneath the citadel." 
        "You hear footsteps outside, the door swings open and a drunk goblin"
        "stumbles into the cell. He is yelling something at you, but you don't speak goblin",#1
        "You stumble out of the cell, into the guard quarters, you are confronted with"
        "a large angry looking troll. ",#2
        "You find enter a room. There are 3 chests. One Gold, one silver, one bronze.",#3
        "You enter a craggy enclosure. Webs cover the ceiling.Eggs line the walls"
        "You see dark shapes moving along the walls."
        "Dozens of tiny, hungry eyes are staring at you",#4
        "You enter a small cave. There is a well in the center of the room",#5
        "You find yourself in a huge cavern, with a stone bridge"
        "In the center of the bridge stands a dragon",#6
        "You enter a narrow stone corridoor. There are 3 troll guards standing in your path."   
        "You enter a cavern, and are confronted by a smalle troup of goblin guards. They grunt at you",#7
        "You see two goblins and a troll sitting around a table. They look annoyed that you"
        "disturbed them",#8
        "room 9",#9
        "You have reached the final room. Ahead of you is the exit of the dungeon."
        "Daylight dazzles your eyes. In your path stands a stone guardian"#10 
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
        "room 10"
        ]
    
    #create rooms
    rooms=[]
    for i in range(10):
        print(i)
        rooms.append (Room(room_descriptions[i],room_descriptions_visited[i],player,monsters[i],items[i],features[i]))
    
    rooms[0].door="locked"
    rooms[0].key_name="prison_door"
    rooms[5].password=True

    room_number=5
    enter_room(rooms,room_number)

main()