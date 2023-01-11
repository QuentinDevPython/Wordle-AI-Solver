import random

from utils import WordDictionary


class RandomIA:

    def __init__(self, WORD_TO_GUESS, GUESSES):
        self.CHANCES = 6
        self.letters_not_to_touch = []
        self.WIN = False
        self.DEFEAT = False
        self.words_file = "dictionary_words_5.txt"
        self.words_to_keep = WordDictionary().load_words(self.words_file)
        self.WORD_TO_GUESS = WORD_TO_GUESS
        self.GUESSES = GUESSES


    def random_IA(self, chance_number):

        guess = random.choice(self.words_to_keep).upper()
        self.GUESSES.append(guess)

        # Si le mot est trouvé
        if guess == self.WORD_TO_GUESS:
            self.WIN = True
            return self.GUESSES, self.WIN, self.DEFEAT

        for i in range(len(guess)):

            # Si la lettre est à la bonne place et pas déjà trouvée
            if guess[i] == self.WORD_TO_GUESS[i] and i not in self.letters_not_to_touch:
                self.letters_not_to_touch.append(i)
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

        print(self.CHANCES)
        print(self.WORD_TO_GUESS)
        print(self.GUESSES)
        print('LETTERS :',self.letters_not_to_touch)
        print('WIN :',self.WIN)
        print('DEFEAT :',self.DEFEAT)
        print(len(self.words_to_keep))
        
        print('\n')

        if chance_number == 6:
            self.DEFEAT = True

        return self.GUESSES, self.WIN, self.DEFEAT
