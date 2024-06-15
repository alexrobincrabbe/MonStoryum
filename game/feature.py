import time
from rich import print
from rich.prompt import Prompt
from rich.console import Console
from rich.theme import Theme
custom_theme= Theme({
    "info" : "grey62",
})

console=Console(theme=custom_theme)
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
                    take_items = Prompt.ask(f"[gold3]take items?[/gold3](yes/no)")
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