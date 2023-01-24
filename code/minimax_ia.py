from collections import defaultdict
from functools import cache
import random
import time
import numpy as np
from utils import WordDictionary, reduce_words, check_word
import itertools
from multiprocessing import Pool, cpu_count


class IAMiniMax:
    '''
    Trouver le guess qui minimise le nombre de possibilité pour le prochain guess.
    Minimax consiste à minimiser la perte maximum (c'est-à-dire dans le pire des cas).
    Dans notre cas on considère tous les mots possibles du dictionnaire et en choisissant 
    le mot qui minimise la taille de sa plus grande partition.
    '''
    previous_results:dict
    words:np.ndarray
    possible_words:np.ndarray
    known_positions:np.ndarray
    known_bad_positions:np.ndarray
    total_count_letters:dict # lettre -> MINIMUM de présence dans le mot cible
    fast_mode:bool
    cpu_count:int

    def __init__(self, word_size, word_guess_file,word_answer_file, GUESSES, WORD_TO_GUESS, fast_mode=0, proc_count=0):
        self.cpu_count = proc_count  if proc_count  else cpu_count()

        self.previous_results = {}
        self.known_positions=np.full(word_size, "")
        self.known_bad_positions=np.full(word_size,None)
        self.total_count_letters=dict()
        self.words = WordDictionary().load_words(word_guess_file)
        self.possible_words = WordDictionary().load_words(word_answer_file)
        self.fast_mode = fast_mode
        self.GUESSES = GUESSES
        self.WORD_TO_GUESS = WORD_TO_GUESS
        self.WIN = False
        self.DEFEAT = False
        self.CHANCES = 6


    def save_result(self, word, result_vector, update_self=True):
        '''
        Sauvegarde les nouveaux resultats et met à jour les lettres connues et leur nombre dans le mot cible
        '''
        
        letters_count = dict()
        known_positions = self.known_positions if update_self else self.known_positions.copy()
        known_bad_positions = self.known_bad_positions if update_self else self.known_bad_positions.copy()
        total_count_letters = self.total_count_letters if update_self else self.total_count_letters.copy()

        for i, (letter, result) in enumerate(zip(word,result_vector)):
            if result==0: # Pas présente
                if letter not in letters_count:
                    letters_count[letter] = 0 
            else : # Présente
                # On l'ajoute dans le compteur
                if letter in letters_count:
                    letters_count[letter] += 1
                else :
                    letters_count[letter] = 1
                if result==1:
                    # La lettre est dans le mot mais la position est mauvaise :
                    if known_bad_positions[i]==None:
                        known_bad_positions[i] = np.array(letter, dtype=str)
                    else :
                        np.append(known_bad_positions[i], letter)
                elif result==2: 
                    # Si bonne position on l'ajoute dans les positions connues
                    known_positions[i] = letter

        # On met à jour le compte total des lettres
        for letter, count in letters_count.items():
            if count >= total_count_letters.get(letter, 0):
                total_count_letters[letter] = count
        
        if update_self :
            self.previous_results[word] = np.array(result_vector)
            self.reduce_possible_words()
        
        return {
            "known_positions":known_positions,
            "known_bad_positions":known_bad_positions,
            "total_count_letters":total_count_letters
        }

    def reduce_possible_words(self):
        self.possible_words = reduce_words(self.possible_words,
            self.total_count_letters,
            self.known_positions,
            self.known_bad_positions
        )             


    @cache
    def evaluate_guess(self, guess, possible_words):
        '''
        Evalue un guess potentiel : Trouve la taille des partitions en fonction des différents résultats possibles
        '''
        
        partitions_len = defaultdict(lambda: 0)
        # Check word
        for w in possible_words:
            r = check_word(w,guess)
            partitions_len[str(r)] += 1
            

        # Le score attribué à ce guess est la taille de la plus grande partition (le plus faible est le meilleur)
        score = max(partitions_len.values())
        # print("guess :",guess," //  score :", score)
        return score
    
    def get_scores_async(self, words=None, nb_proc=None):
        nb_proc = self.cpu_count
        words = words if words else self.words
        # print(f"Async sur {nb_proc} proc")
        with Pool(processes=nb_proc) as pool:
                async_results = [{
                        "guess" : w,
                        "result":pool.apply_async(self.evaluate_guess, (w,tuple(self.possible_words)))
                    } for w in words if w not in self.previous_results]
                scores = {}
                for res in async_results:
                    rslt = res["result"].get(timeout=100)
                    scores[res['guess']] = rslt
                    if rslt==1:
                        #Opti : On trouvera pas plus bas
                        pool.close()
                        #print(len(scores)," size max 1")
                        break
                    
                # scores = {f"{res['guess']}" : res["result"].get(timeout=100) for res in async_results}
                return scores

        
            
    def find_next_guess(self, words = None):
        scores = []
        if len(self.possible_words)<=2:
            # Opti : si <=2 on ne cherche pas et on tente au hasard
            #print("Seulement deux mots possible :",self.possible_words)
            best_guess = random.choice(self.possible_words)
            while best_guess in self.previous_results:
                best_guess = random.choice(self.possible_words)
            return best_guess
        
        words = words if words else self.words
        
        if self.fast_mode : # Opti 
            pw_len = len(self.possible_words)
            w_len = len(words)
            # On simplifie le problème en réduisant le nombre de mots 
            # en fonction du nombre de mots possible
            keep = 0
            if pw_len > 100 :
                # 1/3
                keep = w_len/3
            elif pw_len > 50 :
                # 1/2
                keep = w_len/2
            elif pw_len > 20:
                # 2/3
                keep = 2*w_len/3
            elif pw_len > 10:
                # 3/4
                keep = 3*w_len/4
            words = random.sample(words,int(keep)) if keep else words
            #print("sample size :", len(words), "  //  pw len :",pw_len)


        scores = self.get_scores_async(words,self.cpu_count)
        best_guess = min(scores,key=scores.get)
        # while best_guess in self.previous_results:
        #     scores.pop(best_guess)
        #     best_guess = min(scores,key=scores.get)

        # Le meilleur prochain guess est celui avec le plus petit score possible
        # print("best : ", best_guess, "  //  score :",min(scores.values()))
        return best_guess

    
    def guess(self, chance_number):
        # start_time = time.time()
        
        if len(self.previous_results)==0:
            self.GUESSES.append("SALET")
            return self.GUESSES, self.WIN, self.DEFEAT, chance_number # A priori le meilleur mot de départ mais pourrait être un mot choisis au hasard

        elif len(self.possible_words)==1:
            # Plus qu'un mot possible : on a trouvé !
            self.GUESSES.append(self.possible_words[0].upper())
            self.WIN = True
            return self.GUESSES, self.WIN, self.DEFEAT, chance_number

        else:
            best_guess = self.find_next_guess()
            self.GUESSES.append(best_guess.upper())

        if best_guess.upper() == self.WORD_TO_GUESS:
            self.WIN = True
            return self.GUESSES, self.WIN, self.DEFEAT, chance_number

        elif chance_number == 6:
            self.DEFEAT = True

        return self.GUESSES, self.WIN, self.DEFEAT, chance_number

        # exec_time = time.time()-start_time
        # print("==== Temps d'exec :", int(exec_time),"s")

