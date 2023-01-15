from collections import defaultdict
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
    speed_factor:bool

    def __init__(self, word_size, word_guess_file,word_answer_file, speed_factor=0):
        self.previous_results = {}
        self.known_positions=np.full(word_size, "")
        self.known_bad_positions=np.full(word_size,None)
        self.total_count_letters=dict()
        self.words = WordDictionary().load_words(word_guess_file)
        self.possible_words = WordDictionary().load_words(word_answer_file)
        self.speed_factor = speed_factor


    def save_results(self, word, result_vector, update_self=True):
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


    
    def evaluate_guess(self, guess):
        '''
        Evalue un guess potentiel : Trouve la taille des partitions en fonction des différents résultats possibles
        '''
        
        partitions_len = defaultdict(lambda: 0)
        # Check word
        for w in self.possible_words:
            r = check_word(w,guess)
            partitions_len[str(r)] += 1
            

        # Le score attribué à ce guess est la taille de la plus grande partition (le plus faible est le meilleur)
        score = max(partitions_len.values())
        # print("guess :",guess," //  score :", score)
        return score
    
    def get_scores_async(self, words=None, nb_proc=cpu_count()):
        words = words if words else self.words
        # print(f"Async sur {nb_proc} proc")
        with Pool(processes=nb_proc) as pool:
                async_results = [{
                        "guess" : w,
                        "result":pool.apply_async(self.evaluate_guess, (w,))
                    } for w in words]
                scores = {f"{res['guess']}" : res["result"].get(timeout=100) for res in async_results}
                return scores

        
            
    def find_next_guess(self, words = None):
        scores = []
        if len(self.possible_words)<=2:
            # Opti : si <=2 on ne cherche pas et on tente au hasard
            print("Seulement deux mots possible :",self.possible_words)
            best_guess = random.choice(self.possible_words)
            while best_guess in self.previous_results:
                best_guess = random.choice(self.possible_words)
            return best_guess
        
        words = words if words else self.words
        
        if self.speed_factor : # Opti 
            pw_len = len(self.possible_words)
            keep = len(words)/pw_len*100/self.speed_factor

            keep = len(words)/5 if keep<len(words)/5 else keep
            words = random.sample(words,int(keep)) if keep<len(words) else words
            print("random sample size :", len(words), "  //  pw len :",pw_len)


        scores = self.get_scores_async(words)
        best_guess = min(scores,key=scores.get)
        while best_guess in self.previous_results:
            scores.pop(best_guess)
            best_guess = min(scores,key=scores.get)

        # Le meilleur prochain guess est celui avec le plus petit score possible
        # print("best : ", best_guess, "  //  score :",min(scores.values()))
        return best_guess

    
    def guess(self):
        # start_time = time.time()
        if len(self.previous_results)==0:
            return "salet" # A priori le meilleur mot de départ mais pourrait être un mot choisis au hasard
        if len(self.possible_words)==1:
            # Plus qu'un mot possible : on a trouvé !
            return self.possible_words[0]
        best_guess = self.find_next_guess()
        # exec_time = time.time()-start_time
        # print("==== Temps d'exec :", int(exec_time),"s")
        return best_guess

