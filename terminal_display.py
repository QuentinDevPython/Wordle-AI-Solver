import random
import numpy as np

def load_english_words(file_name):
    file = open(file_name)
    words = file.readlines()
    words = [word[:5].upper() for word in words]
    file.close()
    return words

ENGLISH_WORDS_5_LETTERS = load_english_words('dictionary_words_5.txt')

WORD_TO_GUESS = random.choice(ENGLISH_WORDS_5_LETTERS)
print(WORD_TO_GUESS)


def check_word(word, guess):
    # 2 : Position correcte
    # 1 : Lettre dans le mot mais position incorrecte
    # 0 : Lettre pas dans le mot
    # Deux mots égaux si uniquement des 2
    rslt = []
    for idx, letter in enumerate(guess):
        if letter == word[idx]:
            rslt.append(2)
        elif letter in word:
            n_target = word.count(letter)
            n_correct = 0
            n_occurrence = 0
            
            for i, g in enumerate(guess):
                if g == letter:
                    if i <= idx:
                        n_occurrence += 1
                    if letter == word[i]:
                        n_correct += 1

            if n_target - n_correct - n_occurrence >= 0:
                rslt.append(1)
            else:
                rslt.append(0)
        else:
            rslt.append(0)
    return rslt


def start_game(IA = None):
    # Input function est une entrée de l'utilisateur par défaut, peut être changé pour connecter à une IA.
    # Une IA doit être une instance d'une class avec au moins les fonctions guess() et save_results()
    word_found = False
    while not word_found:
        guess = ""
        if IA :
            # IA
            guess = IA.guess()
            print("Mot essayé par l'IA :", guess)
        else : 
            # Utilisateur
            print("Entrez un mot à essayer (5 lettres): ")
            guess = input().upper()
        
        rslt = np.array(check_word(WORD_TO_GUESS, guess))
        print(rslt)
        if np.all([rslt==2]):
            print("Mot trouvé")
            word_found=True
        if IA : 
            IA.save_results(guess,rslt)

from IA_test import IATest

start_game(IATest())
