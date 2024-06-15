from rich import print
from rich.theme import Theme
from rich.console import Console
from rich.theme import Theme

#my function imports
from game.clear import clear_console

custom_theme= Theme({
    "info" : "grey62",
    "features" : "green",
    "monsters" : "red",
    "items" : "turquoise2"
})

console=Console(theme=custom_theme)

class Room:
    '''
    Main class, contains object instances of all other classes as attributes.
    '''
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
        self.description = "room"
        self.password = False
        self.game_won = False
    
    def examine(self, player):
        '''
        prints description of room, as well as description of all:
        items,features, monsters that are in the room.
        '''
        clear_console()
        if self.visited == False:
            console.print(f'{self.details}',style="info")
        else:
            console.print(f'{self.details_visited}',style="info")
        print("You see:")
        for monster in self.monsters:
            console.print(f'{monster.description}',style = "monsters")
        for item in self.items:
            console.print(f'{item.description}', style = "items")
        for feature in self.features:
            console.print(f'{feature.alt_description}',style="features")