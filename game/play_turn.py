'''
contains all of the functions that run once the game has started,
except for the endgame functions, and functions that are methods
of classes
'''

import time
from rich import print
from rich.theme import Theme
from rich.prompt import Prompt
from rich.console import Console

# my class imports
from game.feature import Feature

# my function imports
from game.endgame import win_game, lose_game

custom_theme = Theme({
    "info": "grey62",
    "features": "green",
    "monsters": "red",
    "items": "turquoise2"
})

console = Console(theme=custom_theme)


def enter_room(rooms, room_number):
    '''
    initiate game state when the player enters a room
    '''
    if rooms[room_number].player.room_reached < room_number + 1:
        rooms[room_number].player.room_reached = room_number + 1
    rooms[room_number].examine(rooms[room_number].player)
    rooms[room_number].visited = True
    if rooms[room_number].game_lost is True:
        return
    start_turn(rooms, room_number)


def start_turn(rooms, room_number: int):
    '''
    Main loop for the game turn,
    monster attack(if condition is met),
    checks if game ends,
    prompts player for action,
    does action
    '''
    while True:
        room = rooms[room_number]
        if room.game_lost is True:
            return
        if rooms[room_number].game_won is True:
            return
        monsters_attack(room)
        if rooms[room_number].game_lost is True:
            for room in rooms:
                room.game_lost = True
            return
        if room.player.hp == 0:
            return
        action = Prompt.ask(
            "[gold3]choose an action[/gold3] (type 'help' for options) ")
        choose_action(room, rooms, room_number, action)
        if room.game_lost is True or room.game_won is True:
            break


def monsters_attack(room):
    '''
    checks for conditions and iterates through monsters.
    each monster attacks until the play is killed
    '''
    if room.battle_started is True and room.monster_action is True:
        for monster in room.monsters:
            monster.attack(room.player)
            if room.player.hp < 1:
                print("you died")
                killed_by = monster.description
                lose_game(room, killed_by)
                room.game_lost = True
                return


def choose_action(room, rooms, room_number, action):
    '''
    checks the input of the player and calls the appropriate action fucntion
    '''
    match action:
        case "help":
            game_help(room)
        case action if action.startswith("examine"):
            examine(room, action)
        case action if action.startswith("take"):
            take(room, action)
        case action if action.startswith("talk"):
            talk(room, action)
        case action if action.startswith("attack"):
            if len(room.monsters) > 0:
                choose_target(room, action)
            else:
                print("There is nothing to attack")
        case "forwards":
            go_forwards(rooms, room_number)
            if room.game_won is True:
                return
        case "backwards":
            go_backwards(rooms, room_number)
        case "inventory":
            room.player.display_inventory()
            room.monster_action = False
        case "status":
            room.player.status()
            room.monster_action = False
        case action if action.startswith("equip"):
            room.monster_action = room.player.inv_equip(action)
        case action if action.startswith("use"):
            room.monster_action = room.player.inv_use(action)
        case _:
            console.print("Please choose a valid option"
                          "(type 'help' for list of commands)", style="info")
            room.monster_action = False


def game_help(room):
    '''
    display list of commands
    '''
    options = ["examine", "inventory", "forwards", "backwards", "status",
               "attack", "equip", "use", "talk", "take"]
    print("list of available commands:")
    for option in options:
        console.print(option, style="info")
    room.monster_action = False


def go_forwards(rooms, room_number):
    '''
    checks conditions and enters next room
    '''
    room = rooms[room_number]
    if len(room.monsters) == 0:
        if room.door == "open":
            room_number += 1
            # if last room, win game and return
            if room_number == 11:
                room.game_won = win_game(room)
                if room.game_won is True:
                    for room in rooms:
                        room.game_won = True
                    return
                else:
                    # if player chooses not to exit the dungeon, return to last
                    # room
                    room_number = 10
            enter_room(rooms, room_number)
            if room.game_lost is True or room.game_won is True:
                return
        else:
            # check if player has key to locked door
            check_door(rooms, room_number)
    elif room_number == 5 and room.password is True:
        print("the dragon allows you to pass")
        time.sleep(2)
        room_number += 1
        enter_room(rooms, room_number)
        if room.game_lost is True:
            return
    else:
        console.print("You must clear the path first", style="info")
        room.monster_action = True


def go_backwards(rooms, room_number):
    '''
    checks conditions and enters previous room
    '''
    room = rooms[room_number]
    if room_number > 0:
        if room_number == 5:
            if room.battle_started is False or len(room.monsters) == 0:
                room_number -= 1
                enter_room(rooms, room_number)
                if room.game_lost is True:
                    return
            else:
                console.print(
                    "The dragon will not let you get away like that",
                    style="info")
        elif len(room.monsters) == 0:
            room_number -= 1
            enter_room(rooms, room_number)
            if room.game_lost is True:
                return
        else:
            console.print("You don't run away from a fight!", style="info")
            room.monster_action = True
    else:
        console.print("You can only go forwards from here", style="info")


def take(room, action):
    '''
    checks if item is in the room items list,
    removes from room items,
    adds to player inventory
    '''
    take_string = action.split(" ", 1)
    if len(take_string) > 1:
        item_string = take_string[1]
    else:
        console.print("take what? (hint: try 'take <name>')", style="info")
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
                    print(
                        f'you take the [turquoise2]{
                            item.description}[/turquoise2]')
    else:
        console.print("You don't see that here", style="info")
        room.monster_action = False


def talk(room, action):
    '''
    calls the appropriate talk method
    '''
    talk_string = action.split(" ", 2)
    if len(talk_string) > 2:
        monster_string = talk_string[2]
    else:
        console.print(
            "talk to what? (hint: try 'talk to <name>')",
            style="info")
        room.monster_action = False
        return
    for monster in room.monsters:
        if monster.description == monster_string:
            monster.talk(room)
            room.monster_action = True
            return
    console.print("talk to what?", style="info")


def check_door(rooms, room_number):
    '''
    checks if door is locked
    '''
    room = rooms[room_number]
    key_name = room.key_name
    items = [item for item in room.player.inventory]
    for item in items:
        if item.type == "key":
            if item.key_name == key_name:
                print(
                    f"you unlock the door with the [gold3]{
                        item.description}[/gold3]")
                room.door = "open"
                time.sleep(3)
                room_number += 1
                enter_room(rooms, room_number)
                if room.game_lost is True:
                    return
    # this condition fixes a bug at endgame
    if room.game_lost is False and room.game_won is False:
        print("The door is locked")


def examine(room, action):
    '''
    checks if item/monster is in the room,
    checks if multiple instances exist,
    if there are multiple instances call a list,
    otherwise call the examine method
    '''
    examinables = [room]
    examine_string = action.split(" ", 1)
    if len(examine_string) > 1:
        examine_object = examine_string[1]
    else:
        console. print(
            "examine what? (hint: try 'examine room')",
            style="info")
        room.monster_action = False
        return
    for item in room.items:
        examinables.append(item)
    for monster in room.monsters:
        examinables.append(monster)
    for feature in room.features:
        examinables.append(feature)
    for item in room.player.inventory:
        examinables.append(item)
    count = [examinable.description for examinable in examinables].count(
        examine_object)
    if count == 0:
        console.print("you don't see that", style="info")
        room.monster_action = False
        return
    if count == 1:
        room.monster_action = True
        for examinable in examinables:
            if examinable.description == examine_object:
                examinable.examine(room.player)
    else:
        # print numbered list of options
        object_dic = examine_list(examinables, examine_object)
        # select object to examine from list
        object_selected = False
        while object_selected is False:
            object_selected, object_select = choose_object_number(room, count)

        object_index = object_dic.get(object_select)
        examinables[object_index].examine(room.player)


def examine_list(examinables, examine_object):
    '''
    prints a numbered list
    and returns a dictionary mapping the list numbers to the array index number
    '''
    examine_number = 0
    examine_index = -1
    examine_dic = {}
    for examinable in examinables:
        examine_index += 1
        if examinable.description == examine_object:
            examine_number += 1
            print(f'{examine_number}: {examinable.description}')
            examine_dic[examine_number] = examine_index
    return examine_dic


def choose_object_number(room, object_count) -> int:
    '''
    validates the players input to select an item from a numbered list
    '''

    object_select = input('Enter a number to choose which item to examine: ')
    try:
        object_select = int(object_select)
        object_selected = True
    except ValueError:
        console.print('Please enter a number', style="info")
        room.monster_action = False
        object_selected = False
    else:
        if object_select < 1 or object_select > object_count:
            room.monster_action = False
            object_selected = False
            console.print('Please pick a valid number', style="info")
    return object_selected, object_select


def choose_target(room, action):
    '''
    checks if target is in room,
    if there is more than once instand of target, or no target is specified
    choose target from a numbered list.
    '''
    target_string = action.split(" ", 1)
    # user specifies target
    if len(target_string) > 1:
        target = target_string[1]
        monsters = [monster.description for monster in room.monsters]
        target_count = monsters.count(target)
        if target_count == 1:
            target_index = 0
            for monster in room.monsters:
                if monster.description == target:
                    attack_monster(room, target_index)
                target_index += 1
            # there is only one target, skip target selection
            return
        elif target_count > 1:
            target_dic = target_list(room, target)
        else:
            room.monster_action = False
            console.print("attack what?", style="info")
            return
    # no target specified
    else:
        target = False
        target_dic = target_list(room, target)
        target_count = len(target_dic)
    # select target number from list
    target_selected = False
    while target_selected is False:
        target_selected, target_select = choose_target_number(
            room, target_selected, target_count)

    target_index = target_dic.get(target_select)
    attack_monster(room, target_index)


def attack_monster(room, target_index):
    '''
    calls function to attack monster, sets battle as initiated,
    calls function to check if the monster is killed
    '''
    room.player.attack(room.monsters[target_index])
    room.battle_started = True
    room.monster_action = True
    kill_monster(room, target_index)


def target_list(room, target):
    '''
    procuces a list of targets, if no target is specified,
    or there are multiple instances of the same target.
    returns a dictionary that maps the number on the printed list
    to the correct index in the monsters array
    '''
    target_number = 0
    target_index = -1
    target_dic = {}
    for monster in room.monsters:
        target_index += 1
        if monster.description == (target) or target is False:
            target_number += 1
            print(
                f'[bright_white]{target_number}[/bright_white]: '
                f'[red1]{monster.description}[/red1] HP - [green1]{monster.hp}'
                f'[/green1]/[chartreuse4]{monster.start_hp}[/chartreuse4]'
            )
            target_dic[target_number] = target_index
    return target_dic


def choose_target_number(room, target_selected, target_count) -> int:
    '''
    validates player input and returns and integer, to select a target
    from the target list
    '''
    target_select = Prompt.ask(
        '[gold3]Enter a number to choose a target: [/gold3]')
    try:
        target_select = int(target_select)
        target_selected = True
    except ValueError:
        print('Please enter a number')
        room.monster_action = False
        target_selected = False
    else:
        if target_select < 1 or target_select > target_count:
            room.monster_action = False
            target_selected = False
            print('Please pick a valid number')
    return target_selected, target_select


def kill_monster(room, target_index):
    '''
    prints message that monster is killed,
    removes monster from list of monsters in the room,
    creates a feature, with the prefix "dead" and items
    carried by the monster
    '''
    if room.monsters[target_index].hp == 0:
        time.sleep(1)
        console.print(
            f'{room.monsters[target_index].description} dies', style="red")
        if room.monsters[target_index].description == "dragon":
            room.player.dragon_killed = True
        dead_monster = room.monsters.pop(target_index)
        description = f'dead {dead_monster.description}'
        details = "you examine the corpse"
        loot = dead_monster.loot
        corpse = Feature(description, details, loot, False)
        corpse.description = f'{dead_monster.description}'
        room.features.append(corpse)
