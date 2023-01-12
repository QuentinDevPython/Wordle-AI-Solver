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
        
        guess = self.words_to_keep[best_word_index].upper()
        self.GUESSES.append(guess) 

        return guess

    
    def determine_color_for_ia(self, guess, j):
        """Determine the color of the letter based on whether the 
        guess is correct, partially correct, or incorrect.
        
        Args:
            guess (str): The current guess word
            j (int): The index of the letter in the word
        Returns:
            tuple: The RGB color code
        """

        letter = guess[j]
        if letter == self.WORD_TO_GUESS[j]:
            return "GREEN"
        elif letter in self.WORD_TO_GUESS:
            n_target = self.WORD_TO_GUESS.count(letter)
            n_correct = 0
            n_occurrence = 0
            
            for i in range(5):
                if guess[i] == letter:
                    if letter == self.WORD_TO_GUESS[i]:
                        n_correct += 1
                    elif i <= j:
                        n_occurrence += 1

            if n_target - n_correct - n_occurrence >= 0:
                return "ORANGE"
            else:
                return "GREY"
        else:
            return "GREY"


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

        if len(self.letters_found)==4 and chance_number<=4:
            #find all the words that contains all the letters to keep
            matching_words = [word.upper() for word in self.words_to_keep if set(self.letters_found).issubset(set(word.upper()))]
            #check if there is more than 2 words to try
            if len(matching_words)>2:
                #extract all the remaining letters to test from the previous words
                letters_to_test = list(set([letter for word in matching_words for letter in set(word) if letter not in set(self.letters_found)]))
                #find the word that test most remaining letters
                guess = max(self.all_words, key=lambda x: len(set(x).intersection(set(letters_to_test))))
                self.GUESSES.append(guess)

            else:
                guess = self.occurrence_logic()

        else:
            guess = self.occurrence_logic()


        # Si le mot est trouvé
        if guess == self.WORD_TO_GUESS:
            self.WIN = True
            return self.GUESSES, self.WIN, self.DEFEAT, chance_number

        # Connaître les couleurs renvoyées par le jeu
        colors = []
        for j in range(5):
            color = self.determine_color_for_ia(guess, j)
            colors.append((guess[j], color))

        # Boucle sur le mot suggéré
        for i in range(len(guess)):
            # Si Vert
            if colors[i][1] == "GREEN" and i not in self.letters_not_to_touch:
                # Garder tous les mots contenant la lettre à cette position
                self.words_to_keep = [word for word in self.words_to_keep if word[i] == guess[i].lower()]
                self.letters_not_to_touch.append(i)
                self.letters_found.append(guess[i])

            # Si gris
            if colors[i][1] == "GREY":
                nb_letter_occurrence = guess.count(guess[i])
                # Si seule occurrence de la lettre dans guess
                if nb_letter_occurrence == 1:
                    # Enlever touts les mots contenant cette lettre
                    self.words_to_keep = [word for word in self.words_to_keep if guess[i].lower() not in word]
                # Si deux occurrences de la lettre dans guess
                elif nb_letter_occurrence == 2:
                    index_occurrence = [j for j in range(len(guess)) if guess[i] == guess[j] and i != j][0]
                    print(index_occurrence)
                    # si cette autre occurrence est en vert
                    if colors[index_occurrence][1] == "GREEN":
                        print('ok')
                        # Enlever tous les mots contenant cette lettre aux autres positions
                        self.words_to_keep = [word for word in self.words_to_keep if word[index_occurrence] == guess[i].lower() and word.count(guess[i].lower()) == 1]
                    # Si cette autre occurrence est en orange
                    elif colors[index_occurrence][1] == "ORANGE":
                        # Enlever tous les mots contenant cette lettre à cette position
                        self.words_to_keep = [word for word in self.words_to_keep if word[i] != guess[i].lower()]
                    # si cette autre occurrence est en gris
                    elif colors[index_occurrence][1] == "GREY":
                        # Enlever touts les mots contenant cette lettre
                        self.words_to_keep = [word for word in self.words_to_keep if guess[i].lower() not in word]

            # Si orange
            if colors[i][1] == "ORANGE":
                # Garder uniquement les mots contenant cette lettre
                self.words_to_keep = [word for word in self.words_to_keep if guess[i].lower() in word]
                # Enlever tous les mots contenant la lettre à cette position
                self.words_to_keep = [word for word in self.words_to_keep if word[i] != guess[i].lower()]

        if chance_number == 6:
            self.DEFEAT = True

        return self.GUESSES, self.WIN, self.DEFEAT, chance_number
