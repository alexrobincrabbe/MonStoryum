import time
from rich.prompt import Prompt
from clear import clear_console
import gspread
from google.oauth2.service_account import Credentials
from rich import print
from rich.prompt import Prompt
from rich.theme import Theme
from rich.console import Console
from prettytable import PrettyTable
from operator import itemgetter

custom_theme= Theme({
    "info" : "grey62",
    "features" : "green",
    "monsters" : "red",
    "stat" : "bright_green",
    "option" : "blue",
    "items" : "turquoise2"
})
console=Console(theme=custom_theme)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Hall_of_fame')

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
    return True

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