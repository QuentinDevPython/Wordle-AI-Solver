import random

from utils import WordDictionary
import pandas as pd
import numpy as np

class RandomIA:
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
        self.WORD_TO_GUESS = WORD_TO_GUESS
        self.GUESSES = GUESSES


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


    def random_IA(self, chance_number):
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

        if chance_number == 1:
            guess = "SLATE"
        else:
            guess = random.choice(self.WORDLE_ANSWERS_5_LETTERS).upper()
        self.GUESSES.append(guess)

        # Connaître les couleurs renvoyées par le jeu
        colors = []
        for j in range(5):
            color = self.determine_color_for_ia(guess, j)
            colors.append((guess[j], color))

        # Si le mot est trouvé
        if guess == self.WORD_TO_GUESS:
            self.WIN = True
            return self.GUESSES, self.WIN, self.DEFEAT

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

        return self.GUESSES, self.WIN, self.DEFEAT


    # Can be implemented to save data for Deep Learning
    def save_state_action(self, all_colors):
        """
        this function builds a dataframe with the current game guesses and results.
        this data will be later used to train a deep learning model based on this algorithmic ai results.
        We therefore store the guess, the colored result and the reulting action a each turn of the game.
        """
        #list of guesses
        guesses = self.GUESSES
        
        #get the colored version of each guess
        word_output = np.array([[-1 for _ in range(5)] for _ in range(6)])

        df_state_action_one_hot_final = pd.DataFrame(columns={"guess": np.array([]),"colored": np.array([]),"action": np.array([]), "answer": np.array([])})

        # Créer toutes les colonnes guess possibles de cette dataframe
        for i in range(6):
            for j in range(5):
                for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
                    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:

                    df_state_action_one_hot_final[f'guess_{i}_letter_position_{j}_{letter}'] = None

        # Créer toutes les colonnes color possibles de cette dataframe
        for i in range(6):
            for j in range(1,6):
                df_state_action_one_hot_final[f'color_word_{i}_letter_{j}'] = None
        
        # Créer toutes les colonnes action possibles de cette dataframe
        for i in range(5):
            for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:

                df_state_action_one_hot_final[f'action_letter_position_{i}_{letter}'] = None


        for x in range(len(guesses)):
            
            if x != len(guesses)-1:
                action = guesses[x+1]
            
            colors = []
            for i in range(len(all_colors[x])):
                if all_colors[x][i][1] == "GREEN":
                    colors.append(2)
                elif all_colors[x][i][1] == "ORANGE":
                    colors.append(1)
                elif all_colors[x][i][1] == "GREY":
                    colors.append(0)
            word_output[x] = colors


            # création d'un dictionnaire vide
            new_row = pd.Series(index = df_state_action_one_hot_final.columns)
            df_state_action_one_hot_final = df_state_action_one_hot_final.append(new_row, ignore_index=True)

            # Boucle sur les mots dans guesses
            for j in range(len(guesses[:x+1])):
                
                word = guesses[:x+1][j]

                for i in range(5):

                    letter = word[i]
                    df_state_action_one_hot_final.at[x, f'guess_{j}_letter_position_{i}_{letter}'] = 1

            # Boucle pour chaque array de couleur
            for i in range(6):

                colors_string = ','.join(map(str, word_output[i]))

                colors_string = colors_string.split(",")

                df_state_action_one_hot_final.at[x, f'color_word_{i}_letter_1'] = colors_string[0]
                df_state_action_one_hot_final.at[x, f'color_word_{i}_letter_2'] = colors_string[1]
                df_state_action_one_hot_final.at[x, f'color_word_{i}_letter_3'] = colors_string[2]
                df_state_action_one_hot_final.at[x, f'color_word_{i}_letter_4'] = colors_string[3]
                df_state_action_one_hot_final.at[x, f'color_word_{i}_letter_5'] = colors_string[4]

            if x != len(guesses)-1:
                for i in range(5):
                    
                    letter = action[i]
                    df_state_action_one_hot_final.at[x, f'action_letter_position_{i}_{letter}'] = 1

        return df_state_action_one_hot_final
    