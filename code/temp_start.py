from collections import Counter
import time

import numpy as np
from minimax_ia import IAMiniMax
from terminal_display import TerminalDisplay

if __name__ == '__main__':

    
    # TerminalDisplay().start_game(IAMiniMax(5, 'dictionary_words_5.txt','dictionary_words_answers.txt'), word_to_guess="salad")
    # TerminalDisplay().start_game(IAMiniMax(5, 'dictionary_words_5.txt','dictionary_words_answers.txt'), word_to_guess="world")
    term = TerminalDisplay()
    scores = []
    times = []

    # Mode rapide :
    fast=True 
    # Changer le nombre d'essais pour faire les moyennes
    n_try = 400

    for i in range(n_try):
        print(f"====== {i+1}/{n_try} ======")
        start_time = time.time()
        score = term.start_game(IAMiniMax(5, 'dictionary_words_5.txt','dictionary_words_answers.txt',fast_mode=fast))
        exec_time = int(time.time()-start_time)
        print(f"\nTemps d'exec : {exec_time} s")
        
        scores.append(score)
        times.append(exec_time)
        if n_try>1:
            print("Score moyen : ",np.mean(scores))
            print("Scores : ",Counter(scores))
            print("Temps moyen : ",np.mean(times))
        print()
    # if n_try>1:
    #     print()
    #     print("Score moyen final : ",np.mean(scores))
    #     print("Scores final : ",Counter(scores))
    #     print("Temps moyen final : ",np.mean(times),"s")
    