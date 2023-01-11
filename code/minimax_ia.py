import numpy as np
from utils import WordDictionary, reduce_words


class IAMiniMax:
    '''
    Trouver le guess qui minimise le nombre de possibilité pour le prochain guess
    '''
    previous_results:dict
    possible_words:np.ndarray
    known_positions:np.ndarray
    known_bad_positions:np.ndarray
    total_count_letters:dict # lettre -> MINIMUM de présence dans le mot cible

    def __init__(self, word_size, word_file):
        self.previous_results = {}
        self.known_positions=np.full(word_size, "")
        self.known_bad_positions=np.full(word_size,None)
        self.total_count_letters=dict()
        self.possible_words = WordDictionary().load_words("dictionary_words_5.txt")
        # print()

    def save_results(self, word, result_vector):
        '''
        Sauvegarde les nouveaux resultats et met à jour les lettres connues et leur nombre dans le mot cible
        '''
        self.previous_results[word] = np.array(result_vector)
        # know_position = result_vector==2
        letters_count = dict()

        for i, (letter, result) in enumerate(zip(word,result_vector)):
            if result==0: # Pas présente
                letters_count[letter] = 0 
            else : # Présente
                # On l'ajoute dans le compteur
                if letter in letters_count:
                    letters_count[letter] += 1
                else :
                    letters_count[letter] = 1
                if result==1:
                    # La lettre est dans le mot mais la position est mauvaise :
                    if self.known_bad_positions[i]==None:
                        self.known_bad_positions[i] = np.array(letter, dtype=str)
                    else :
                        np.append(self.known_bad_positions[i], letter)
                elif result==2: 
                    # Si bonne position on l'ajoute dans les positions connues
                    self.known_positions[i] = letter

        # On met à jour le compte total des lettres
        for letter, count in letters_count.items():
            if count >= self.total_count_letters.get(letter, 0):
                self.total_count_letters[letter] = count
        

    def reduce_words(self):
        print("total_count_letters",self.total_count_letters)
        print("known_positions", self.known_positions)
        print("known_bad_positions", self.known_bad_positions)
        self.possible_words = reduce_words(self.possible_words,
                        self.total_count_letters,
                        self.known_positions,
                        self.known_bad_positions
                        )             
        print("\nRESULT :")
        print("possible_words",self.possible_words)
        


    
    def guess(self):
        # rslts = self.previous_results
        print(self.previous_results)
        return "AAAAA"


ia = IAMiniMax(5,"dictionary_words_5.txt")
ia.save_results("badzz", [2,2,1,0,0])
# ia.previous_results
ia.reduce_words()