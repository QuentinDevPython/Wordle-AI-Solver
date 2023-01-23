from utils import WordDictionary
import torch
import torch.optim as optim
import torch.nn as nn

import neural_network
class deep_reinforcement_learing:
    """
    This class contains all the deep reinforcement learning approach required functions
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
        self.words_file = "../../dictionary_words_5.txt"
        self.words_to_keep = WordDictionary().load_words(self.words_file)
        self.WORD_TO_GUESS = WORD_TO_GUESS
        self.GUESSES = GUESSES

        #one hot encoding words
        letter_to_index = {letter: index for index, letter in enumerate('abcdefghijklmnopqrstuvwxyz')}
        word_indices = [[letter_to_index[letter] for letter in self.words_to_keep] for word in self.words_to_keep]
        # one-hot encode the indices
        one_hot_words = torch.eye(26)[word_indices]


    def train_model(self,data):
        model = neural_network.NeuralNetwork()
        criterion = nn.MSELoss()

        # Define the optimizer
        optimizer = optim.SGD(model.parameters(), lr=0.01)

        # Iterate through the dataset
        for inputs, labels in dataset:
            # Zero the gradients
            optimizer = optim.Adam(self.net.parameters(), lr=self.hparams.lr, weight_decay=self.hparams.weight_decay)
            # Forward pass
            outputs = model(inputs)
            # Compute the loss
            loss = criterion(outputs, labels)
            # Backward pass and optimize
            loss.backward()
            optimizer.step()




