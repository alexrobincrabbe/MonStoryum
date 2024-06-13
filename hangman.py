import random as rnd

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
    word_list = ["monster", "bunnies", "mouse","pirate", "magical"]
    word = rnd.choice(word_list)
    #create string with a space and an underscore for each letter in the word
    number_of_letters=len(word)
    show_word=""
    for step in range(number_of_letters):
        show_word+=" _"
    print(show_word)
    # check if the letter is in the word and replace the underscore
    while win == False:
        guess = input("guess a letter: ")
        if guess in word:
            index=0
            for letter in word:
                if guess == letter:
                    show_word = show_word[:index*2+1] + letter + show_word[index*2 + 2:]
                index+=1
            print(show_word)
            #if all letters have been guessed, win the game
            if show_word.replace(" ","") == word:
                print("you win")
                win = True
                return win
        else:
            print("incorrect")
            guesses_remaining-=1
            if guesses_remaining == 0:
                print("you lose")
                return win
            else:
                print(f"you have {guesses_remaining} wrong guesses left")
