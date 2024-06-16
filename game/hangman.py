'''
Contains hangman function
'''

import random as rnd
from rich.prompt import Prompt
from rich import print


def hangman():
    '''
    Function to play a simple hangman stlye game
    Player has 5 guesses to guess all the letters in the word
    returns True if the game is won
    returns False if the game is lost
    '''
    win = False
    guesses_remaining = 5
    #
    word_list = ["dinner", "breakfast", "hungry", "delicious"]
    word = rnd.choice(word_list)
    # create string with a space and an underscore for each letter in the word
    number_of_letters = len(word)
    show_word = ""
    for _ in range(number_of_letters):
        show_word += " _"

    print(f'[green3]{show_word}[/green3]')
    # check if the letter is in the word and replace the underscore
    while win is False:
        guess = Prompt.ask("[chartreuse4]'guess a letter' [chartreuse4]")
        if len(guess) > 1:
            print("[chartreuse4] 'just one letter please...'[chartreuse4] ")
        else:
            if guess in word:
                if guess in show_word:
                    print(
                        " [chartreuse4]'you have already guessed that letter, "
                        "I already tire of you little human...' "
                        "[/chartreuse4]")
                else:
                    index = 0
                    for letter in word:
                        if guess == letter:
                            show_word = show_word[:index * 2 + 1] + \
                                letter + show_word[index * 2 + 2:]
                        index += 1
                    print(show_word)
                    # if all letters have been guessed, win the game
                    if show_word.replace(" ", "") == word:
                        print("[green3]you win[green3]")
                        win = True
                        return win
            else:
                print("[chartreuse4]'incorrect'[chartreuse4]")
                guesses_remaining -= 1
                if guesses_remaining == 0:
                    print("you lose")
                    return win
                else:
                    print(f" [chartreuse4]'you have [red1] "
                          f"{guesses_remaining}[/red1]"
                          "wrong guesses left..'[chartreuse4] ")
                    print("The dragon licks it's lips")
