import random
from collections import defaultdict

from utils import WordDictionary



class AlgorithmicIA:
    """A class representing the computer player (random IA) 
    in the Wordle game.
    """

    def __init__(self, WORD_TO_GUESS, GUESSES):
        """
        Initialize the computer player.
        
        Args:
            WORD_TO_GUESS (str): the word that the computer is trying to guess.
            GUESSES (list): a list to store the guesses made by the computer.
        """

        self.CHANCES = 6
        self.letters_not_to_touch = []
        self.letters_found = []
        self.WIN = False
        self.DEFEAT = False
        self.words_file = "dictionary_words_5.txt"
        self.words_to_keep = WordDictionary().load_words(self.words_file)
        self.all_words = WordDictionary().load_words(self.words_file)
        self.all_words = [word.upper() for word in self.all_words]
        self.WORD_TO_GUESS = WORD_TO_GUESS
        self.GUESSES = GUESSES

    
    def occurrence_logic(self):


        letter_count = defaultdict(lambda: [0]*5)

        for word in self.words_to_keep:
            # Boucle sur les lettres
            for i in range(len(word)):
                letter_count[word[i]][i] += 1

        sorted_letter_count = dict(sorted(letter_count.items(), key=lambda x: x[0]))

        # Initialisation de l'index et du poids pour le mot avec le plus de poids
        best_word_index = -1
        best_word_weight = 0

        # Boucle sur les mots
        for i, word in enumerate(self.words_to_keep):
            # Poids pour le mot en cours
            weight = 0
            # Boucle sur les lettres
            for j, letter in enumerate(word):
                weight += sorted_letter_count[letter][j]
            # Mise à jour de l'index et du poids si on a trouvé un meilleur mot
            if weight > best_word_weight:
                best_word_index = i
                best_word_weight = weight
        #if there is only one letter left and multiple letters to try, this section will find the best word to try
        
        guess = self.words_to_keep[best_word_index].upper()
        self.GUESSES.append(guess) 

        return guess


    def algorithmic_IA(self, chance_number):
        """
        Perform a turn for the computer player.
        
        Args:
            chance_number (int): the number of chances the computer has left to make a correct guess.
        
        Returns:
            tuple: A tuple containing the following elements:
                - list: the guesses made by the computer so far
                - bool: whether the computer has won the game
                - bool: whether the computer has lost the game
        """
        ########################
        ###### IA LOGIC ########
        ########################

        print('LEN :',len(self.letters_found))
        print('NB :', chance_number)

        if len(self.letters_found)==4 and chance_number<=4:
            print('ok')
            #find all the words that contains all the letters to keep
            matching_words = [word.upper() for word in self.words_to_keep if set(self.letters_found).issubset(set(word.upper()))]
            print(matching_words)
            #check if there is more than 2 words to try
            if len(matching_words)>2:
                print('ok2')
                #extract all the remaining letters to test from the previous words
                letters_to_test = list(set([letter for word in matching_words for letter in set(word) if letter not in set(self.letters_found)]))
                print(letters_to_test)  
                #find the word that test most remaining letters
                guess = max(self.all_words, key=lambda x: len(set(x).intersection(set(letters_to_test))))
                print(guess)
                self.GUESSES.append(guess)
                #return self.GUESSES, self.WIN, self.DEFEAT

            else:
                guess = self.occurrence_logic()

        else:
            guess = self.occurrence_logic()


        ########################
        ##### END IA LOGIC #####
        ########################

          
        # Si le mot est trouvé
        if guess == self.WORD_TO_GUESS:
            self.WIN = True
            return self.GUESSES, self.WIN, self.DEFEAT, chance_number

        for i in range(len(guess)):

            # Si la lettre est à la bonne place et pas déjà trouvée
            if guess[i] == self.WORD_TO_GUESS[i] and i not in self.letters_not_to_touch:
                self.letters_not_to_touch.append(i)
                self.letters_found.append(guess[i])
                self.words_to_keep = [word for word in self.words_to_keep if word[i] == guess[i].lower()]

        # Si la lettre est dans le mot mais pas à la bonne place
        # - Garder uniquement les mots contenant la lettre en question
        # - Enlever tous les mots qui l'ont à la mauvaise position
        for i in range(len(guess)):
            # Si la lettre n'est pas déjà trouvée
            if i not in self.letters_not_to_touch:
                for j in range(len(self.WORD_TO_GUESS)):
                    if guess[i] == self.WORD_TO_GUESS[j]:
                        # On ne garde que les mots contenant cette lettre
                        self.words_to_keep = [word for word in self.words_to_keep if guess[i].lower() in word]
                        # On enlève les mots qui contiennent cette lettre à la mauvaise position
                        self.words_to_keep = [word for word in self.words_to_keep if guess[i].lower() != word[i]]
                        break
        
        # Si la lettre n'est pas dans le mot
        for i in range(len(guess)):
            letter_in_word = False
            for j in range(len(self.WORD_TO_GUESS)):
                if guess[i] == self.WORD_TO_GUESS[j]:
                    letter_in_word = True
            if not letter_in_word:
                self.words_to_keep = [word for word in self.words_to_keep if guess[i].lower() not in word]


        if chance_number == 6:
            self.DEFEAT = True

        return self.GUESSES, self.WIN, self.DEFEAT, chance_number
