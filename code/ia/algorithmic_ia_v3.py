import random
from collections import defaultdict

from utils import WordDictionary
import pandas as pd
import numpy as np

class AlgorithmicIAV3:
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
        self.response_words_file = "dictionary_words_answers.txt"
        self.WORDLE_ANSWERS_5_LETTERS = WordDictionary().load_words(self.response_words_file)
        self.all_words = WordDictionary().load_words(self.words_file)
        self.all_words = [word.upper() for word in self.all_words]
        self.WORD_TO_GUESS = WORD_TO_GUESS
        self.GUESSES = GUESSES


    def count_letters(self, word):

        letter_counts = {}
        for letter in word:
            if letter in letter_counts:
                letter_counts[letter] += 1
            else:
                letter_counts[letter] = 1
        return letter_counts

    
    def occurrence_logic(self):

        letter_count = defaultdict(lambda: [0]*5)

        for word in self.WORDLE_ANSWERS_5_LETTERS:
            # Boucle sur les lettres
            for i in range(len(word)):
                letter_count[word[i]][i] += 1

        sorted_letter_count = dict(sorted(letter_count.items(), key=lambda x: x[0]))

        words = {}
        max_freq = [0, 0, 0, 0, 0]
        
        for letter in sorted_letter_count:
            for i in range(5):
                if max_freq[i] < sorted_letter_count[letter][i]:
                    max_freq[i] = sorted_letter_count[letter][i]
        
        for word in self.WORDLE_ANSWERS_5_LETTERS:
            score = 1
            for i in range(5):
                c = word[i]
                score *= 1 + (sorted_letter_count[c][i] - max_freq[i]) **2

            words.update({word: score})
        
        guess = min(words, key=words.get).upper()

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
        if len(self.letters_found)==4 and chance_number<=5:
            #find all the words that contains all the letters to keep
            matching_words = [word.upper() for word in self.WORDLE_ANSWERS_5_LETTERS if set(self.letters_found).issubset(set(word.upper()))]
            #check if there is more than 2 words to try
            if len(matching_words)>2:
                #extract all the remaining letters to test from the previous words
                letters_to_test = list(set([letter for word in matching_words for letter in set(word) if letter not in set(self.letters_found)]))
                #find the word that test most remaining letters
                guess = max(self.all_words, key=lambda x: len(set(x).intersection(set(letters_to_test))))

            else:
                guess = self.occurrence_logic()

        elif len(self.letters_found)==3 and chance_number<=5:

            #find all the words that contains all the letters to keep
            matching_words = [word.upper() for word in self.WORDLE_ANSWERS_5_LETTERS if set(self.letters_found).issubset(set(word.upper()))]
            #check if there is more than 2 words to try
            if len(matching_words)>2:
                #extract all the remaining letters to test from the previous words
                letters_to_test = list(set([letter for word in matching_words for letter in set(word) if letter not in set(self.letters_found)]))
                #find the word that test most remaining letters
                guess = max(self.all_words, key=lambda x: len(set(x).intersection(set(letters_to_test))))

            else:
                guess = self.occurrence_logic()


        elif len(self.letters_found)==2 and chance_number<=3:  

            #find all the words that contains all the letters to keep
            matching_words = [word.upper() for word in self.WORDLE_ANSWERS_5_LETTERS if set(self.letters_found).issubset(set(word.upper()))]
            #check if there is more than 2 words to try
            if len(matching_words)>2:
                #extract all the remaining letters to test from the previous words
                letters_to_test = list(set([letter for word in matching_words for letter in set(word) if letter not in set(self.letters_found)]))
                #find the word that test most remaining letters
                guess = max(self.all_words, key=lambda x: len(set(x).intersection(set(letters_to_test))))

            else:
                guess = self.occurrence_logic()

        
        elif len(self.letters_found)==2 and chance_number<=4:
            
            colors_prev = []
            for j in range(5):
                color = self.determine_color_for_ia(self.GUESSES[-1], j)
                colors_prev.append((self.GUESSES[-1][j], color))

            count_grey = 0
            for j in range(5):
                if colors_prev[j][1] == "GREY":
                    count_grey += 1

            #find all the words that contains all the letters to keep
            matching_words = [word.upper() for word in self.WORDLE_ANSWERS_5_LETTERS if set(self.letters_found).issubset(set(word.upper()))]
            #check if there is more than 2 words to try
            if len(matching_words)>2 and count_grey == 5:
                #extract all the remaining letters to test from the previous words
                letters_to_test = list(set([letter for word in matching_words for letter in set(word) if letter not in set(self.letters_found)]))
                #find the word that test most remaining letters
                guess = max(self.all_words, key=lambda x: len(set(x).intersection(set(letters_to_test))))

            else:
                guess = self.occurrence_logic()


        else:
            guess = self.occurrence_logic()
        
        self.GUESSES.append(guess)

        # Connaître les couleurs renvoyées par le jeu
        colors = []
        for j in range(5):
            color = self.determine_color_for_ia(guess, j)
            colors.append((guess[j], color))

        # Si le mot est trouvé
        if guess == self.WORD_TO_GUESS:
            self.WIN = True
            return self.GUESSES, self.WIN, self.DEFEAT, chance_number, colors

        

        # Boucle sur le mot suggéré
        for i in range(len(guess)):
            # Si Vert
            if colors[i][1] == "GREEN" and i not in self.letters_not_to_touch:
                # Garder tous les mots contenant la lettre à cette position
                self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if word[i] == guess[i].lower()]
                self.letters_not_to_touch.append(i)
                self.letters_found.append(guess[i])

            # Si gris
            if colors[i][1] == "GREY":
                nb_letter_occurrence = guess.count(guess[i])
                # Si seule occurrence de la lettre dans guess
                if nb_letter_occurrence == 1:
                    # Enlever touts les mots contenant cette lettre
                    self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if guess[i].lower() not in word]
                # Si deux occurrences de la lettre dans guess
                elif nb_letter_occurrence == 2:
                    index_occurrence = [j for j in range(len(guess)) if guess[i] == guess[j] and i != j][0]
                    # si cette autre occurrence est en vert
                    if colors[index_occurrence][1] == "GREEN":
                        # Enlever tous les mots contenant cette lettre aux autres positions
                        self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if word[index_occurrence] == guess[i].lower() and word.count(guess[i].lower()) == 1]
                    # Si cette autre occurrence est en orange
                    elif colors[index_occurrence][1] == "ORANGE":
                        # Enlever tous les mots contenant cette lettre à cette position
                        self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if word[i] != guess[i].lower()]
                    # si cette autre occurrence est en gris
                    elif colors[index_occurrence][1] == "GREY":
                        # Enlever touts les mots contenant cette lettre
                        self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if guess[i].lower() not in word]
                # Si trois occurrences de la lettre dans guess
                elif nb_letter_occurrence == 3:
                    index_occurrence = [j for j in range(len(guess)) if guess[i] == guess[j] and i != j]  
                    # Si les deux occurrences sont vertes
                    if colors[index_occurrence[0]][1] == "GREEN" and colors[index_occurrence[1]][1] == "GREEN":
                        # Enlever tous les mots contenant cette lettre aux autres positions
                        self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if word[index_occurrence[0]] == guess[i].lower() and word[index_occurrence[1]] == guess[i].lower() and word.count(guess[i].lower()) == 2]
                    # Si la première occurrence est verte
                    elif colors[index_occurrence[0]][1] == "GREEN":
                        self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if word[index_occurrence[0]] == guess[i].lower() and word.count(guess[i].lower()) <= 2]
                    # Si la deuxième occurrence est verte
                    elif colors[index_occurrence[1]][1] == "GREEN":
                        self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if word[index_occurrence[1]] == guess[i].lower() and word.count(guess[i].lower()) <= 2]
                    # Si les deux autres occurrences sont grises
                    elif colors[index_occurrence[0]][1] == "GREY" and colors[index_occurrence[1]][1] == "GREY":
                        self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if guess[i].lower() not in word]

            # Si orange
            if colors[i][1] == "ORANGE":
                # Garder uniquement les mots contenant cette lettre
                self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if guess[i].lower() in word]
                # Enlever tous les mots contenant la lettre à cette position
                self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if word[i] != guess[i].lower()]

        if chance_number == 6:
            self.DEFEAT = True

        return self.GUESSES, self.WIN, self.DEFEAT, chance_number, colors


    def save_state_action(self, all_colors):
        """
        this function builds a dataframe with the current game guesses and results.
        this data will be later used to train a deep learning model based on this algorithmic ai results.
        We therefore store the guess, the colored result and the reulting action a each turn of the game.
        """
        #list of guesses
        guesses = self.GUESSES
        #word to guess
        wtg = self.WORD_TO_GUESS

        #initialise the dataframe
        df_state_action=pd.DataFrame(columns={'guess': np.array([]),'colored': np.array([]),'action': np.array([]), 'answer': np.array([])}, index=range(1, len(guesses)))
        
        # colored_guesses = []
        #get the colored version of each guess
        word_output = np.array([[-1 for _ in range(5)] for _ in range(6)])
        #guide to one hot encode
        #letter_to_index = {letter: index for index, letter in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}
        #word_indices = [[letter_to_index[letter] for letter in word] for word in guesses]
        # one-hot encode the indices
        # one_hot_words = []
        # for word in word_indices:
        #     one_hot_words.append(np.eye(26)[word])        
        # wtg = np.array([letter_to_index[letter] for letter in wtg])
        # wtg = np.eye(26)[wtg]
        #one_hot_words_list = np.array([[[-1 for _ in range(26)] for _ in range(5)] for _ in range(6)])
        for x in range(len(guesses)):
            #one_hot_words_list[x] = one_hot_words[x]
            try :
                action = guesses[x+1]
            except:
                action = ""
            
            colors = []
            for i in range(len(all_colors[x])):
                if all_colors[x][i][1] == "GREEN":
                    colors.append(2)
                elif all_colors[x][i][1] == "ORANGE":
                    colors.append(1)
                elif all_colors[x][i][1] == "GREY":
                    colors.append(0)
            word_output[x] = colors
            df_state_action.loc[x+1] = [guesses[:x+1],word_output.copy(), action,wtg]

            df_state_action_one_hot = pd.DataFrame()

            count = 0

            # Boucle sur les mots dans guesses
            for j in range(len(guesses[:x+1])):
                
                word = guesses[:x+1][j]

                for i in range(5):

                    word_column = pd.DataFrame([word], columns=['word'])

                    # Sélection de la lettre à la position i dans chaque mot
                    df_letter = word_column['word'].str[i]
                    # Transformation en one-hot pour cette lettre
                    df_letter_one_hot = df_letter.str.get_dummies()
                    # Renommage des colonnes avec le numéro de la position
                    df_letter_one_hot = df_letter_one_hot.add_prefix(f'guess_{count}_letter_position_{i}_')
                    # Ajout des colonnes one-hot au DataFrame final
                    df_state_action_one_hot = pd.concat([df_state_action_one_hot, df_letter_one_hot], axis=1)

                count += 1

            # Boucle pour chaque array de couleur
            for i in range(6):

                colors_string = ','.join(map(str, word_output[i]))

                df_colors_one_hot = pd.DataFrame([colors_string], columns=[f'word_color_{i}'])

                df_colors_one_hot[
                    [
                        f'color_word_{i}_letter_1',
                        f'color_word_{i}_letter_2',
                        f'color_word_{i}_letter_3',
                        f'color_word_{i}_letter_4',
                        f'color_word_{i}_letter_5'
                    ]
                ] = df_colors_one_hot[f'word_color_{i}'].str.split(',', expand=True)

                df_state_action_one_hot = pd.concat([df_state_action_one_hot, df_colors_one_hot], axis=1)

            # Boucle pour chaque position dans le mot
            for i in range(5):
                # Sélection de la lettre à la position i dans chaque mot
                df_letter = df_state_action['action'].str[i]
                # Transformation en one-hot pour cette lettre
                df_letter_one_hot = df_letter.str.get_dummies()
                # Renommage des colonnes avec le numéro de la position
                df_letter_one_hot = df_letter_one_hot.add_prefix(f'action_letter_position_{i}_')
                # Ajout des colonnes one-hot au DataFrame final
                df_state_action_one_hot = pd.concat([df_state_action_one_hot, df_letter_one_hot], axis=1)

        return df_state_action_one_hot
    