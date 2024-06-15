'''
Contains definitions of Item classes
'''
from rich.theme import Theme
from rich.console import Console

custom_theme = Theme({
    "info": "grey62",
})

console = Console(theme=custom_theme)


class Item:
    '''
    Item superclass.
    initialises description attributes and examine method
    '''

    def __init__(self, description, details):
        self.description = description
        self.details = details

    def examine(self, player):
        '''
        describes monster
        '''
        console.print(f'{self.details}', style="info")


class Weapon(Item):
    '''
    Weapon specific attributes added to Item class
    '''

    def __init__(self, description, details, damage, hit):
        Item.__init__(self, description, details)
        self.damage = damage
        self.hit = hit
        self.type = "weapon"


class Armor(Item):
    '''
    Armor specific attributes added to Item class
    '''

    def __init__(self, description, details, armor_value, dodge):
        Item.__init__(self, description, details)
        self.armor_value = armor_value
        self.dodge = dodge
        self.type = "armor"


class Potion(Item):
    '''
    Potion specific attributes added to Item class
    '''

    def __init__(self, description, details, stat, effect):
        Item.__init__(self, description, details)
        self.stat = stat
        self.effect = effect
        self.type = "potion"


class Key(Item):
    '''
    Key specific attributes added to Item class
    '''

    def __init__(self, description, details, key_name):
        Item.__init__(self, description, details)
        self.key_name = key_name
        self.type = "key"
