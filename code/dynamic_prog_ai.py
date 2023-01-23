import random

from utils import WordDictionary


class DynamicProgAI:
    """This class aims to re-implement the work from Bertsimas and Paskov
in their paper: "An Exact and Interpretable Solution to Wordle".
    """

    def __init__(self, WORD_TO_GUESS, GUESSES,state_t):
        """
        Initialize the computer player.
        
        Args:
            WORD_TO_GUESS (str): the word that the computer is trying to guess.
            GUESSES (list): a list to store the guesses made by the computer. 
            state_t (int): int between 1 and 6 corresponding to the turn
        """

        self.CHANCES = 6
        self.letters_not_to_touch = []
        self.WIN = False
        self.DEFEAT = False
        self.words_file = "dictionary_words_5.txt"
        self.words_to_keep = WordDictionary().load_words(self.words_file)
        self.WORD_TO_GUESS = WORD_TO_GUESS
        self.GUESSES = GUESSES

    def is_valid_solution(action,tile_coloring,temp_solution):
        if tile_coloring==22222:
            return True
        else :
            return False

    def get_transition_information(state,action):
        transition_info= dict()
        for solution in state:
            tile_coloring=.check_word(action,solution)
            temp_state=set()
            for temp_solution in state:
                if is_valid_solution(action,tile_coloring,temp_solution):
                    temp_state.add(solution)
            transition_info[temp_state]+=1/len(state)
        return transition_info  


    def optimal_value(state,t,dictionary):
        if t==6 or t==5 and len(state)>1:
            return float("inf")
        elif t==5:
            return 1
        elif len(state)==1:
            return 1
        elif len(state)==2:
            return 1.5
        elif (state,t) in dictionary:
            return dictionary[(state,t)]
        state_value=float("inf")
        for action in initial_state:
            temp=1
            next_states=get_transition_information(state,action)
            if next_states.size ==1 and state in next_states:
                continue
            for next_state in next_states:
                temp=temp+(2*len(next_state)-1)/len(next_state)
            for next_state in next_states:
                if temp >= state_value:
                    break
                elif next_state == action:
                    continue
                temp_dict={
                    "pair":(next_state,t+1),
                    "value":state_value

                }
                new_dictionary=dictionary.append(temp_dict)
                temp = temp+optimal_value(next_state,t+1,new_dictionary)
            if temp <state_value:
                state_value=temp
        return state_value
    def dynamic_programming_ai(self, turn_number):
        """
        Perform the different turns of the AI.
        
        Args:
            turn_number (int): the number of attempts of the AI
        
        Returns:
            tuple: A tuple containing the following elements:
                - list: the guesses made by the computer so far
                - bool: whether the computer has won the game
                - bool: whether the computer has lost the game
        """
        if turn_number==1:
            self.GUESSES.append("SALET")
            self.state=self.words_to_keep
        else:
            
        

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
