import random
from collections import defaultdict
import math

from utils import WordDictionary



class AlgorithmicIAV4:
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
        self.words_to_keep = set(WordDictionary().load_words(self.words_file))
        self.response_words_file = "dictionary_words_answers.txt"
        self.WORDLE_ANSWERS_5_LETTERS = set(WordDictionary().load_words(self.response_words_file))
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

    
    def entropy_logic(self):

        # Pour chaque mot
        DICT_ENGLISH_POSSIBLE_WORDS = set(self.WORDLE_ANSWERS_5_LETTERS.copy())
        POSSIBLE_COLORS = ["GREEN", "GREY", "ORANGE"]
        colors = []
        score = 0
        best_score = -1
        best_word = ""
        for vocab in DICT_ENGLISH_POSSIBLE_WORDS:
            vocab = vocab.upper()
            # Pour chaque possibilité de couleur pour la première lettre
            for color1 in POSSIBLE_COLORS:
                try:
                    colors[0] = ((vocab[0], color1))
                except:
                    colors.append((vocab[0], color1))
                # Pour chaque possibilité de couleur pour la deuxième lettre
                for color2 in POSSIBLE_COLORS:
                    try:
                        colors[1] = ((vocab[1], color2))
                    except:
                        colors.append((vocab[1], color2))

                    # Pour chaque possibilité de couleur pour la troisième lettre
                    for color3 in POSSIBLE_COLORS:
                        try:
                            colors[2] = ((vocab[2], color3))
                        except:
                            colors.append((vocab[2], color3))

                        # Pour chaque possibilité de couleur pour la quatrième lettre
                        for color4 in POSSIBLE_COLORS:
                            try:
                                colors[3] = ((vocab[3], color3))
                            except:
                                colors.append((vocab[3], color4))

                            # Pour chaque possibilité de couleur pour la quatrième lettre
                            for color5 in POSSIBLE_COLORS:
                                try:
                                    colors[4] = ((vocab[4], color5))
                                except:
                                    colors.append((vocab[4], color5))

                                # Boucle sur le mot suggéré
                                for i in range(len(vocab)):
                                    # Si Vert
                                    if colors[i][1] == "GREEN" and i not in self.letters_not_to_touch:
                                        # Garder tous les mots contenant la lettre à cette position
                                        DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if word[i] == vocab[i].lower()]

                                    # Si gris
                                    if colors[i][1] == "GREY":
                                        nb_letter_occurrence = vocab.count(vocab[i])
                                        # Si seule occurrence de la lettre dans guess
                                        if nb_letter_occurrence == 1:
                                            # Enlever touts les mots contenant cette lettre
                                            DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if vocab[i].lower() not in word]
                                        # Si deux occurrences de la lettre dans guess
                                        elif nb_letter_occurrence == 2:
                                            index_occurrence = [j for j in range(len(vocab)) if vocab[i] == vocab[j] and i != j][0]
                                            # si cette autre occurrence est en vert
                                            if colors[index_occurrence][1] == "GREEN":
                                                # Enlever tous les mots contenant cette lettre aux autres positions
                                                DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if word[index_occurrence] == vocab[i].lower() and word.count(vocab[i].lower()) == 1]
                                            # Si cette autre occurrence est en orange
                                            elif colors[index_occurrence][1] == "ORANGE":
                                                # Enlever tous les mots contenant cette lettre à cette position
                                                DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if word[i] != vocab[i].lower()]
                                            # si cette autre occurrence est en gris
                                            elif colors[index_occurrence][1] == "GREY":
                                                # Enlever touts les mots contenant cette lettre
                                                DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if vocab[i].lower() not in word]
                                        # Si trois occurrences de la lettre dans guess
                                        elif nb_letter_occurrence == 3:
                                            index_occurrence = [j for j in range(len(vocab)) if vocab[i] == vocab[j] and i != j]  
                                            # Si les deux occurrences sont vertes
                                            if colors[index_occurrence[0]][1] == "GREEN" and colors[index_occurrence[1]][1] == "GREEN":
                                                # Enlever tous les mots contenant cette lettre aux autres positions
                                                DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if word[index_occurrence[0]] == vocab[i].lower() and word[index_occurrence[1]] == vocab[i].lower() and word.count(vocab[i].lower()) == 2]
                                            # Si la première occurrence est verte
                                            elif colors[index_occurrence[0]][1] == "GREEN":
                                                DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if word[index_occurrence[0]] == vocab[i].lower() and word.count(vocab[i].lower()) == 1]
                                            # Si la deuxième occurrence est verte
                                            elif colors[index_occurrence[1]][1] == "GREEN":
                                                DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if word[index_occurrence[1]] == vocab[i].lower() and word.count(vocab[i].lower()) == 1]
                                            # Si les deux autres occurrences sont grises
                                            elif colors[index_occurrence[0]][1] == "GREY" and colors[index_occurrence[1]][1] == "GREY":
                                                DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if vocab[i].lower() not in word]

                                    # Si orange
                                    if colors[i][1] == "ORANGE":
                                        # Garder uniquement les mots contenant cette lettre
                                        DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if vocab[i].lower() in word]
                                        # Enlever tous les mots contenant la lettre à cette position
                                        DICT_ENGLISH_POSSIBLE_WORDS = [word for word in DICT_ENGLISH_POSSIBLE_WORDS if word[i] != vocab[i].lower()]


                                p = len(DICT_ENGLISH_POSSIBLE_WORDS)/len(self.WORDLE_ANSWERS_5_LETTERS)
                                try:
                                    score += (p * math.log2(1/p))
                                except:
                                    score += 0
                                # Remise du dictionnaire à l'état courant
                                DICT_ENGLISH_POSSIBLE_WORDS = set(self.WORDLE_ANSWERS_5_LETTERS.copy())


            if score > best_score:
                best_score = score
                best_word = vocab

            score = 0

        return best_word

    
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

        if chance_number ==1:
            guess = "SALET"
        else:
            guess = self.entropy_logic()

        #print('GUESS :', guess)
        self.GUESSES.append(guess)
        
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
                        self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if word[index_occurrence[0]] == guess[i].lower() and word.count(guess[i].lower()) == 1]
                    # Si la deuxième occurrence est verte
                    elif colors[index_occurrence[1]][1] == "GREEN":
                        self.WORDLE_ANSWERS_5_LETTERS = [word for word in self.WORDLE_ANSWERS_5_LETTERS if word[index_occurrence[1]] == guess[i].lower() and word.count(guess[i].lower()) == 1]
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

        return self.GUESSES, self.WIN, self.DEFEAT, chance_number
