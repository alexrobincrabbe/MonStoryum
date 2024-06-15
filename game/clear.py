'''
contains function to clear the console
'''
import os

def clear_console():
    '''
    clears the console
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
   