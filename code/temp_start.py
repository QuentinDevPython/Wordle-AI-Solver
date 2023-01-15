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
    # Vitesse (Plus grand, plus rapide. 0 pour ne pas accelerer)
    speed=20 
    # Note : 40s sans, 20s avec 10, 15s avec 20
    
    # Changer le nombre d'essais pour faire les moyennes
    n_try = 1

    for i in range(n_try):
        start_time = time.time()
        score = term.start_game(IAMiniMax(5, 'dictionary_words_5.txt','dictionary_words_answers.txt',speed_factor=speed))
        exec_time = int(time.time()-start_time)
        print("========= Temps d'exec :", exec_time,"s")
        print()
        scores.append(score)
        times.append(exec_time)
    if n_try>1:
        print("Score moyen : ",np.mean(scores))
        print("Temps moyen : ",np.mean(times),"s")
    