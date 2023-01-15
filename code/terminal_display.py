import random
import numpy as np
from utils import WordDictionary, check_word

class TerminalDisplay:
    guess_words:list[str]
    target_words:list[str]

    def __init__(self) -> None:
        self.guess_words = WordDictionary().load_words('dictionary_words_5.txt')
        self.target_words = WordDictionary().load_words('dictionary_words_answers.txt')
        

    def start_game(self, IA = None, word_to_guess=None):
        # Input function est une entrée de l'utilisateur par défaut, peut être changé pour connecter à une IA.
        # Une IA doit être une instance d'une class avec au moins les fonctions guess() et save_results()

        if not word_to_guess :
            word_to_guess = random.choice(self.target_words)
            
        word_found = False
        turn = 0
        while not word_found:
            turn += 1
            guess = ""
            if IA :
                # IA
                guess = IA.guess()
                print("Mot essayé par l'IA :", guess)
            else : 
                # Utilisateur
                print("Entrez un mot à essayer (5 lettres): ")
                guess = input()
            
            rslt = np.array(check_word(word_to_guess, guess))
            print(rslt)
            if np.all([rslt==2]):
                print("Mot trouvé en ",turn,"coups")
                word_found=True
            if IA : 
                IA.save_results(guess,rslt)
                print("possible words now : ", len(IA.possible_words))

