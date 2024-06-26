'''
contains the functions that end the game,
as well as recording the players score
and displaying the hall of fame using the google sheets API
'''

import time
from operator import itemgetter

import gspread
from google.oauth2.service_account import Credentials
from rich.prompt import Prompt
from rich import print
from rich.theme import Theme
from rich.console import Console
from prettytable import PrettyTable

# my function imports
from game.clear import clear_console

custom_theme = Theme({
    "info": "grey62",
    "features": "green",
    "monsters": "red",
    "stat": "bright_green",
    "option": "blue",
    "items": "turquoise2"
})
console = Console(theme=custom_theme)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Hall_of_fame')


def lose_game(room, killed_by):
    '''
    ends the game
    '''
    escaped = "no"
    time.sleep(3)
    print("You tried your best but, sadly, have perished…who "
          "will stop Achlys and her monsters now?")
    add_results(room, killed_by, escaped)


def win_game(room):
    '''
    checks if player wants to leave the dungeon
    and ends the game
    '''
    if room.player.dragon_killed is False:
        print(
            "You can escape the dungeon now, however the dragon is still "
            "back there in the dungeon")
        while True:
            answer = Prompt.ask(
                "[gold3]Are you sure you want to leave? [gold3](yes/no)")
            if answer == "yes" or answer == "y":
                break
            if answer == "no" or answer == "n":
                return False
    clear_console()
    time.sleep(1)
    print("It has never been done before, but you have succeeded where "
          "so many before you have failed. Congratulations, you are no "
          "longer Achlys' prisoner - you have fought heroically and you "
          "have your freedom. But now you must go on and save Greystorm, "
          "it is your destiny…")
    escaped = "yes"
    killed_by = "survived"
    add_results(room, killed_by, escaped)
    return True


def add_results(room, killed_by, escaped):
    '''
    adds the players results to the HoF
    '''
    if "gold medallion" in [
            item.description for item in room.player.inventory]:
        gold_medallion = "yes"
    else:
        gold_medallion = "no"
    results = (
        room.player.description,
        room.player.room_reached,
        killed_by,
        escaped,
        gold_medallion)
    hof = SHEET.worksheet('Sheet1')
    hof.append_row(results)
    while True:
        see_hof = Prompt.ask(
            "[chartreuse4]See Hall of Fame? (yes/no)[/chartreuse4]")
        if see_hof == "yes" or see_hof == "y":
            show_hof()
            break
        if see_hof == "no" or see_hof == "n":
            break


def show_hof():
    '''
    prints the HoF in a table
    '''
    hall_of_fame = SHEET.worksheet('Sheet1')
    hof = hall_of_fame.get_all_values()
    # remove headings row
    hof.pop(0)
    for row in hof:
        row[1] = int(row[1])
    # sort the HoF by:gold medallion, escaped, room reached
    hof.sort(key=itemgetter(4, 3, 1), reverse=True)
    table = PrettyTable()
    table.field_names = [
        "NAME",
        "ROOM REACHED",
        "KILLED BY",
        "ESCAPED",
        "GOLD MEDALLION"]
    for row in hof:
        table.add_row(row)
    # show the HoF
    console.print(table, style="purple")
