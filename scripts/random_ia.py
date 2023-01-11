import random

## Etapes de l'IA Random
# - Prendre un premier mot aléatoirement 
# - Le comparer au mot à deviner pour retirer les lettres mauvaises, les bonnes lettres
# - Enlever dans le dictionnaire les mots qui ne nous seront pas utiles
# - Rechoisir un mot alétoirement

# WORD_TO_GUESS = random.choice(ENGLISH_WORDS_5_LETTERS)
# print(WORD_TO_GUESS)

def random_IA(WORD_TO_GUESS, GUESSES, words_to_keep, letters_not_to_touch, chance_number, WIN, DEFEAT):

    guess = random.choice(words_to_keep)
    GUESSES.append(guess)

    # Si le mot est trouvé
    if guess == WORD_TO_GUESS:
        print("WIN")
        WIN = True
        return GUESSES, WIN, DEFEAT, words_to_keep, letters_not_to_touch 

    for i in range(len(guess)):

        # Si la lettre est à la bonne place et pas déjà trouvée
        if guess[i] == WORD_TO_GUESS[i] and i not in letters_not_to_touch:
            letters_not_to_touch.append(i)
            words_to_keep = [word for word in words_to_keep if word[i] == guess[i]]

    # Si la lettre est dans le mot mais pas à la bonne place
    # - Garder uniquement les mots contenant la lettre en question
    # - Enlever tous les mots qui l'ont à la mauvaise position
    for i in range(len(guess)):
        # Si la lettre n'est pas déjà trouvée
        if i not in letters_not_to_touch:
            for j in range(len(WORD_TO_GUESS)):
                if guess[i] == WORD_TO_GUESS[j]:
                    # On ne garde que les mots contenant cette lettre
                    words_to_keep = [word for word in words_to_keep if guess[i] in word]
                    # On enlève les mots qui contiennent cette lettre à la mauvaise position
                    words_to_keep = [word for word in words_to_keep if guess[i] != word[i]]
                    break
    
    # Si la lettre n'est pas dans le mot
    for i in range(len(guess)):
        letter_in_word = False
        for j in range(len(WORD_TO_GUESS)):
            if guess[i] == WORD_TO_GUESS[j]:
                letter_in_word = True
        if not letter_in_word:
            words_to_keep = [word for word in words_to_keep if guess[i] not in word]

    if chance_number == 6:
        DEFEAT = True
        print('DEFEAT')

    return GUESSES, WIN, DEFEAT, words_to_keep, letters_not_to_touch 