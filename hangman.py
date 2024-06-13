import random as rnd

def hangman():
    win = False
    guesses_remaining = 5
    word_list = ["monster", "bunnies", "mouse","pirate", ]
    word = rnd.choice(word_list)
    number_of_letters=len(word)
    show_word=""
    for step in range(number_of_letters):
        show_word+=" _"
    print(show_word)
    while win == False:
        guess = input("guess a letter")
        if guess in word:
            index=0
            for letter in word:
                if guess == letter:
                    show_word = show_word[:index*2+1] + letter + show_word[index*2 + 2:]
                index+=1
            print(show_word)
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
