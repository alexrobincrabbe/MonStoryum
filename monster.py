import random as rnd
import math
import time
from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from prettytable import PrettyTable
from rich import print

#my function imports
from hangman import hangman

custom_theme= Theme({
    "info" : "grey62",
})

console=Console(theme=custom_theme)

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
        self.riddle_solved = False

    def talk(self,room):
        if self.riddle_solved == False:
            print(
                "The walls shake as, in a booming, gravelly voice, "
                "the dragon suddenly speaks! "
                " 'I have been here for centuries and you are the first "
                "to say a single word to me. Usually they all run away! "
                "I will let you pass by me unharmed, but only if you play "
                "my game…and win!”' ")
            while True:
                answer = Prompt.ask("[chartreuse4] 'would you like to play?'[/chartreuse4] (yes/no)")
                if answer == "yes" or answer == "y":
                    print (
                        " [chartreuse4]'Let us begin, the rules of my game are simple. \n"
                        "You must guess the letters for the word I am thinking of. "
                        "For each correct guess, I will reveal where that letter "
                        "belongs in my word. \n"
                        "If you guess my word, you are free to go. If you guess incorrectly "
                        "five times…I will eat you.' [/chartreuse4]"
                    )
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
                print(" 'It has been so long since my last meal...' ")
                room.monster_action = True
                room.battle_started = True
            else:
                self.riddle_solved = True
                room.password = True
                print(
                    " [chartreuse4]'You’ve beaten me at my own game, "
                    " I will allow you to pass.' [/chartreuse4]\n The dragon " 
                    "steps aside, allowing you just enough space to pass by. "
                    "Taking a deep breath, you brave the bridge and scurry past "
                    "as fast as you can.' "
                    )
        else:
            print("[chartreuse4]'you have already bested my game human. Leave quickly before I change my mind'[/chartreuse4]")
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
                        if self.weapon.description == item.description:
                            print(f"[blue]{item.description}[/blue] is already equipped")
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
            console.print("choose an object to equip",style = "info")
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
            console.print("choose an object to use", style = "info")
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
        stats_table.add_column("Agility",[self.agility])
        console.print(stats_table,style="orange1")