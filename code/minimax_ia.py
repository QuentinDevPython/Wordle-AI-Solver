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

    def __init__(self, word_size, word_file):
        self.previous_results = {}
        self.known_positions=np.full(word_size, "")
        self.known_bad_positions=np.full(word_size,None)
        self.total_count_letters=dict()
        self.words = WordDictionary().load_words(word_file)
        self.possible_words = self.words
        # print()


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
        # print("total_count_letters",self.total_count_letters)
        # print("known_positions", self.known_positions)
        # print("known_bad_positions", self.known_bad_positions)
        self.possible_words = reduce_words(self.possible_words,
                        self.total_count_letters,
                        self.known_positions,
                        self.known_bad_positions
                        )             
        # print("\nRESULT :")
        # print("possible_words",self.possible_words)


    
    def evaluate_guess(self, guess):
        '''
        Evalue un guess potentiel : Trouve la taille des partitions en fonctions des différents résultats possibles
        '''
        array_guess = np.array(list(guess))
        # Cherche les resultats que pourrait avoir ce mot :
        result = np.full(len(array_guess), -1)

        # Evalue score de base
        for i, letter in enumerate(array_guess):
            good_letter = self.known_positions[i]
            count = self.total_count_letters.get(letter)
            if count == None :
                # Aucune info sur la lettre : degré de liberté
                continue
            if good_letter and good_letter == letter:
                # La lettre est bonne
                result[i] = 2
            if count == 0:
                # La lettre n'est pas présente dans le mot
                result[i] = 0


        # Remplacer les -1 par chaque possibilité de resultats (0,1,2)
        results = []
        replace_indexes = np.where(result==-1)[0]
        possible_rslt = itertools.product([0,1,2],repeat=len(replace_indexes))
        for combination in possible_rslt:
            new_result = result.copy()
            for i, idx in enumerate(replace_indexes):
                new_result[idx] = combination[i]
            results.append(new_result)

        # Trouver les partitions de toutes ces possibilitées de resultats :
        # On ne sauvegarde que la taille de la partition
        partitions_len = []
        for r in results:
            # new_informations = self.save_results(guess,r,update_self=False)
            # # print(new_informations)
            # partition = reduce_words(self.possible_words,
            #             new_informations["total_count_letters"],
            #             new_informations["known_positions"],
            #             new_informations["known_bad_positions"]
            #             )
            # partitions_len.append(len(partition))

            # Check word
            partition_len = 0
            for w in self.possible_words:
                s = check_word(w,guess)
                if all(r == s):
                    partition_len += 1
            partitions_len.append(partition_len)

        # Le score attribué à ce guess est la taille de la plus grande partition (le plus faible est le meilleur)
        # print("guess :",guess," //  score :", max(partitions_len))
        return max(partitions_len)
    
    def get_scores_async(self, words=None, nb_proc=cpu_count()):
        words = words if words else self.words
        # print(f"Async sur {nb_proc} proc")
        with Pool(processes=nb_proc) as pool:
                async_results = [{
                        "guess" : w,
                        "result":pool.apply_async(self.evaluate_guess, (w,))
                    } for w in words]
                # scores = dict([{f"{res['guess']}" : res["result"].get(timeout=100)} for res in async_results])
                scores = {f"{res['guess']}" : res["result"].get(timeout=100) for res in async_results}
                # scores = {w:pool.apply_async(self.evaluate_guess, (w,)).get(timeout=100) for w in words}
                return scores

        
            
    def find_next_guess(self, words = None, fast=False):
        scores = []

        
        words = words if words else self.words
        
        if fast : # Opti 
            pw_len = len(self.possible_words)
            # keep = len(words)*(5/pw_len) if pw_len>10 else len(words)
            keep = (len(words)/2)*(100/pw_len)
            # keep = len(words)-pw_len*100
            # keep = 3
            words = random.sample(words,int(keep)) if keep<len(words) else words
            print("random sample size :", len(words))
            
        print(f"Evaluation des scores async sur {cpu_count()} procs")

        scores = self.get_scores_async(words)
        best_guess = min(scores,key=scores.get)
        while best_guess in self.previous_results:
            scores.pop(best_guess)
            best_guess = min(scores,key=scores.get)

        # for w in words:
        #     score = self.evaluate_guess(w)   
        #     if score == 1:
        #         # Ce guess sépare parfaitement les mots possible
        #         return w
        #     scores.append(score)

        # recursive 

        # Le meilleur prochain guess est celui avec le plus petit score possible
        # return self.words[np.argmin(scores)]
        print("best : ", best_guess, "  //  score :",min(scores.values()))
        return best_guess

    # def find_next_guess_async(self, fast=False):
        


    
    def guess(self, fast = True):
        start_time = time.time()
        if len(self.previous_results)==0:
            return "salet" # A priori le meilleur mot de départ mais pourrait être un mot choisis au hasard
        if len(self.possible_words)==1:
            # Plus qu'un mot possible : on a trouvé !
            return self.possible_words[0]
        if len(self.possible_words) < 10:
            fast=False
        best_guess = self.find_next_guess(fast=fast)
        exec_time = time.time()-start_time
        print("==== Temps d'exec :", int(exec_time),"s")
        return best_guess

