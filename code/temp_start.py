import time
from minimax_ia import IAMiniMax
from terminal_display import TerminalDisplay

if __name__ == '__main__':
    # TerminalDisplay().start_game(IAMiniMax(5, 'dictionary_words_5.txt'), word_to_guess="salad")
    # TerminalDisplay().start_game(IAMiniMax(5, 'dictionary_words_5.txt'), word_to_guess="world")
    start_time = time.time()

    TerminalDisplay().start_game(IAMiniMax(5, 'dictionary_words_5.txt'))
    exec_time = time.time()-start_time
    print("========= Temps d'exec total :", int(exec_time),"s")
    