import pygame
import random
import time
import pandas as pd
import numpy as np

from utils import WordDictionary, check_word
from ia.random_ia import RandomIA
from ia.algorithmic_ia_v1 import AlgorithmicIAV1
from ia.algorithmic_ia_v2 import AlgorithmicIAV2
from ia.algorithmic_ia_v3 import AlgorithmicIAV3
from minimax_ia import IAMiniMax
from multiprocessing import cpu_count


if __name__ != "__main__":
    pass


class Game:
    """The Game class is the main driver of the Wordle game. It sets up the game, 
    handles user input and controls the game loop. 
    """

    def __init__(self):
        """The initializer sets up the basic structure of the game, 
        initializing variables and pygame library. Also it sets up 
        the window size, colors, font, guesses, letters, etc.
        """

        # Get English dictionary
        self.words_file = "dictionary_words_5.txt"
        self.ENGLISH_WORDS_5_LETTERS = WordDictionary().load_words(self.words_file)

        self.response_words_file = "dictionary_words_answers.txt"
        self.WORDLE_ANSWERS_5_LETTERS = WordDictionary().load_words(self.response_words_file)

        # Randomly choose a word to find in the game
        self.WORD_TO_GUESS = random.choice(
            self.WORDLE_ANSWERS_5_LETTERS
        ).upper()

        # Init pygame
        pygame.init()
        pygame.font.init()

        # Init the window dimensions
        self.WINDOW_HEIGHT = 750
        self.WINDOW_WIDTH = 950
        self.WINDOW_GRID_WIDTH = 550

        # Margins
        self.MARGIN = 10
        self.TOP_MARGIN = 60
        self.LEFT_MARGIN = 100

        # Colors
        self.GREY = (128,128,128)
        self.GREEN = (6, 214, 160)
        self.ORANGE = (255, 128, 0)

        # Squares size
        self.SQUARES_SIZE = (self.WINDOW_GRID_WIDTH - 4*self.MARGIN - 2*self.LEFT_MARGIN) // 5 - 5

        # Letter fonts
        self.LETTERS_FONT = pygame.font.SysFont(
            "free sans bold",
            self.SQUARES_SIZE
        )
        self.LETTERS_FONT_SMALL = pygame.font.SysFont(
            "free sans bold",
            self.SQUARES_SIZE//2
        )
        self.LETTERS_FONT_VERY_SMALL = pygame.font.SysFont(
            "free sans bold",
            self.SQUARES_SIZE//2 - 5
        )

        # Guesses
        self.INPUT = ""
        self.GUESSES = []
        self.ALPHABET = [['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    ['H', 'I', 'J', 'K', 'L', 'M', 'N'],
                    ['O', 'P', 'Q', 'R', 'S', 'T', 'U'],
                    [ 'V', 'W', 'X', 'Y', 'Z']]

        # Game
        self.GAME_OVER = False

        # IA boxes
        checkbox1_pressed = False
        checkbox2_pressed = False
        checkbox3_pressed = False
        checkbox4_pressed = False
        checkbox5_pressed = False
        checkbox6_pressed = False

        self.checkboxes = [
            checkbox1_pressed, 
            checkbox2_pressed,
            checkbox3_pressed,
            checkbox4_pressed,
            checkbox5_pressed,
            checkbox6_pressed
        ]

        # Window title
        pygame.display.set_caption("Wordle")

        # Set up Screen
        self.screen = pygame.display.set_mode(
            (
                self.WINDOW_WIDTH,
                self.WINDOW_HEIGHT
            )
        )

        # Dataframe that stores all games states and results
        self.df_state_action=pd.DataFrame(columns={"guess": np.array([]),"colored": np.array([]),"action": np.array([]), "answer": np.array([])})

        # Créer toutes les colonnes guess possibles de cette dataframe
        for i in range(6):
            for j in range(5):
                for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
                    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:

                    self.df_state_action[f'guess_{i}_letter_position_{j}_{letter}'] = None

        # Créer toutes les colonnes color possibles de cette dataframe
        for i in range(6):
            for j in range(1,6):
                self.df_state_action[f'color_word_{i}_letter_{j}'] = None
        
        # Créer toutes les colonnes action possibles de cette dataframe
        for i in range(5):
            for letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 
                'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:

                self.df_state_action[f'action_letter_position_{i}_{letter}'] = None


    def determine_color(self, guess, j):
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
            return self.GREEN
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
                return self.ORANGE
            else:
                return self.GREY
        else:
            return self.GREY


    def determine_color_alphabet(self):
        """Determine the color of the letters in alphabet based 
        on the letters that have been guessed correctly 
        and the letters that are present in the word to guess.

        Returns:
            list: position letters with their assigned color
        """

        ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ALPHABET_POSITIONS = []
        count = 0
        positions = []

        for i in range(4):
            j_range = 7
            if i == 3:
                for j in range(1,6):
                    ALPHABET_POSITIONS.append(((i,j), ALPHABET[count]))
                    count += 1
            else:
                for j in range(7):
                    ALPHABET_POSITIONS.append(((i,j), ALPHABET[count]))
                    count += 1

        for i in range(len(ALPHABET_POSITIONS)):
            for word in self.GUESSES:
                if ALPHABET_POSITIONS[i][1] in word and ALPHABET_POSITIONS[i][1] in self.WORD_TO_GUESS:
                    positions.append((ALPHABET_POSITIONS[i][0], self.GREEN))
                elif ALPHABET_POSITIONS[i][1] in word:
                    positions.append((ALPHABET_POSITIONS[i][0], self.GREY))
                    
        return positions

    
    def draw_word_guesses(self):
        """Draw the current guesses as a grid of letter squares on the screen"""

        y = self.TOP_MARGIN//2
        for i in range(6):
            x = self.WINDOW_WIDTH//6
            for j in range(5):

                # Letter squares
                letter_square = pygame.Rect(x, y, self.SQUARES_SIZE, self.SQUARES_SIZE)
                pygame.draw.rect(self.screen, self.GREY, letter_square, width=2)

                # letters / words already guessed
                if i < len(self.GUESSES):
                    color = self.determine_color(self.GUESSES[i], j)
                    pygame.draw.rect(self.screen, color, letter_square, border_radius=3)
                    letter = self.LETTERS_FONT.render(self.GUESSES[i][j], False, (255,255,255))
                    surface = letter.get_rect(center = (x+self.SQUARES_SIZE//2, y+self.SQUARES_SIZE//2))
                    self.screen.blit(letter, surface)

                # User input (next guess)
                if i == len(self.GUESSES) and j < len(self.INPUT):
                    letter = self.LETTERS_FONT.render(self.INPUT[j], False, self.GREY)
                    surface = letter.get_rect(center = (x+self.SQUARES_SIZE//2, y+self.SQUARES_SIZE//2))
                    self.screen.blit(letter, surface)

                x += self.SQUARES_SIZE + self.MARGIN

            y += self.SQUARES_SIZE + self.MARGIN


    def draw_letters_guesses(self):
        """Draw the alphabet letters as a grid of letter squares on the screen"""
        
        # Draw unguessed letters
        y = self.TOP_MARGIN//2 + 6 * (self.SQUARES_SIZE + self.MARGIN)  + self.TOP_MARGIN//2 + 30

        LETTERS_SIZE = (self.WINDOW_GRID_WIDTH - 4*self.MARGIN - 2*self.LEFT_MARGIN) // 7
        colors = self.determine_color_alphabet()

        for i in range(4):
            x = self.WINDOW_WIDTH//9
            if i != 3:
                for j in range(7):
                    # Letter squares
                    letter_square = pygame.Rect(x, y, LETTERS_SIZE, LETTERS_SIZE)
                    color = (255,255,255)
                    color_letter = self.GREY
                    for item in colors:
                        if (i,j) == item[0]:
                            color = item[1]
                            color_letter = (255,255,255)
                    pygame.draw.rect(self.screen, color, letter_square, border_radius=3)
                    pygame.draw.rect(self.screen, self.GREY, letter_square, width=2)
                    letter = self.LETTERS_FONT_SMALL.render(self.ALPHABET[i][j], False, color_letter)
                    surface = letter.get_rect(center = (x+LETTERS_SIZE//2, y+LETTERS_SIZE//2))
                    self.screen.blit(letter, surface)

                    x += LETTERS_SIZE + 2*self.MARGIN

            else:
                for j in range(5):
                    # Letter squares
                    letter_square = pygame.Rect(x + (LETTERS_SIZE + 2*self.MARGIN), y, LETTERS_SIZE, LETTERS_SIZE)
                    color = (255,255,255)
                    color_letter = self.GREY
                    for item in colors:
                        if (i,j) == item[0]:
                            color = item[1]
                            color_letter = (255,255,255)
                    pygame.draw.rect(self.screen, color, letter_square, border_radius=3)
                    pygame.draw.rect(self.screen, self.GREY, letter_square, width=2)
                    letter = self.LETTERS_FONT_SMALL.render(self.ALPHABET[i][j], False, color_letter)
                    surface = letter.get_rect(center = (x+ (LETTERS_SIZE + 2*self.MARGIN) + LETTERS_SIZE//2, y+LETTERS_SIZE//2))
                    self.screen.blit(letter, surface)

                    x += LETTERS_SIZE + 2*self.MARGIN

            y += LETTERS_SIZE + 2*self.MARGIN


    def draw_checkbox_IA(self):
        """Draw the checkboxes on the screen and fill them if they are pressed"""

        # CheckBox 1
        checkbox1 = pygame.Rect(self.WINDOW_WIDTH-300, self.TOP_MARGIN//2 + 50, 20, 20)
        if not self.checkboxes[0]:
            pygame.draw.rect(self.screen, self.GREY, checkbox1, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox1, border_radius=3)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - RANDOM -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-200, self.TOP_MARGIN//2 + 60))
        self.screen.blit(ia, surface)

        # CheckBox 2
        checkbox2 = pygame.Rect(self.WINDOW_WIDTH-300, self.TOP_MARGIN//2 + 95, 20, 20)
        if not self.checkboxes[1]:
            pygame.draw.rect(self.screen, self.GREY, checkbox2, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox2, border_radius=3)
        pygame.draw.rect(self.screen, self.GREY, checkbox2, width=2)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - ALGORITHM V1 -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-177, self.TOP_MARGIN//2 + 107))
        self.screen.blit(ia, surface)

        # CheckBox 3
        checkbox3 = pygame.Rect(self.WINDOW_WIDTH-300, self.TOP_MARGIN//2 + 140, 20, 20)
        if not self.checkboxes[2]:
            pygame.draw.rect(self.screen, self.GREY, checkbox3, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox3, border_radius=3)
        pygame.draw.rect(self.screen, self.GREY, checkbox3, width=2)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - ALGORITHM V2 -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-177, self.TOP_MARGIN//2 + 151))
        self.screen.blit(ia, surface)

        # CheckBox 4
        checkbox4 = pygame.Rect(self.WINDOW_WIDTH-300, self.TOP_MARGIN//2 + 185, 20, 20)
        if not self.checkboxes[3]:
            pygame.draw.rect(self.screen, self.GREY, checkbox4, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox4, border_radius=3)
        pygame.draw.rect(self.screen, self.GREY, checkbox4, width=2)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - ALGORITHM V3 -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-177, self.TOP_MARGIN//2 + 196))
        self.screen.blit(ia, surface)

        # CheckBox 5
        checkbox5 = pygame.Rect(self.WINDOW_WIDTH-300, self.TOP_MARGIN//2 + 230, 20, 20)
        if not self.checkboxes[4]:
            pygame.draw.rect(self.screen, self.GREY, checkbox5, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox5, border_radius=3)
        pygame.draw.rect(self.screen, self.GREY, checkbox5, width=2)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - MINIMAX -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-201, self.TOP_MARGIN//2 + 241))
        self.screen.blit(ia, surface)

        # CheckBox 6
        checkbox6 = pygame.Rect(self.WINDOW_WIDTH-300, self.TOP_MARGIN//2 + 275, 20, 20)
        if not self.checkboxes[5]:
            pygame.draw.rect(self.screen, self.GREY, checkbox6, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox6, border_radius=3)
        pygame.draw.rect(self.screen, self.GREY, checkbox6, width=2)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - DEEP LEARNING -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-172, self.TOP_MARGIN//2 + 287))
        self.screen.blit(ia, surface)

        # Restart button
        restart_logo = pygame.image.load("restart_logo.png")
        self.screen.blit(restart_logo, (self.WINDOW_WIDTH-230, self.TOP_MARGIN//2 + 370))


    def show_correct_answer(self):
        """Show the correct answer on the screen after gameover"""

        if len(self.GUESSES) == 6 and self.GUESSES[5] != self.WORD_TO_GUESS:
            GAME_OVER = True
            letters = self.LETTERS_FONT.render(self.WORD_TO_GUESS, False, self.GREY)
            surface = letters.get_rect(center = (self.WINDOW_WIDTH//3 + 5, self.TOP_MARGIN//2 + 6 * (self.SQUARES_SIZE + self.MARGIN)  + self.TOP_MARGIN//2 - 5))
            self.screen.blit(letters, surface)


    def update_screen(self):
        """Updates the screen to reflect the current state of the game"""
        
        pygame.display.flip()


    def draw_window(self):
        """This function is responsible for drawing the window of the game and 
        updating its contents.
        """

        # Background
        self.screen.fill("white")

        # Apply all draw functions
        self.draw_word_guesses()
        self.draw_letters_guesses()  
        self.draw_checkbox_IA()

        # Show correct answer if Defeat
        self.show_correct_answer()

        self.update_screen()


    def validate_guess_word(self):
        """This function add the guess word to the guesses list if the word is validated, 
        and reinitialize the input
        """

        if len(self.INPUT) == 5 and self.INPUT.lower() in self.ENGLISH_WORDS_5_LETTERS:
            self.GUESSES.append(self.INPUT)
            self.GAME_OVER = True if self.INPUT == self.WORD_TO_GUESS else False
            self.INPUT = ""
        else:
            self.INPUT = ""


    def write_letter(self, event):
        """This function adds the letter associated with the key pressed to the input string.
        Args:
            event: pygame.event, event that contains the key pressed
        """

        if len(self.INPUT) < 5 and not self.GAME_OVER:
            self.INPUT = self.INPUT + event.unicode.upper()


    def erase_letter(self):
        """Erases the last letter from the input string"""

        if len(self.INPUT) > 0:
            self.INPUT = self.INPUT[:len(self.INPUT)-1]

    
    def restart_game(self):
        """Restart the game by reseting the game state"""

        self.checkboxes = [False, False, False, False, False, False]
        self.GAME_OVER = False
        self.WORD_TO_GUESS = random.choice(self.WORDLE_ANSWERS_5_LETTERS).upper()
        self.GUESSES = []
        self.INPUT = ""

    
    def print_win_state(self):
        """Show a win message on the screen when an IA wins the game"""
        letters = self.LETTERS_FONT.render('IA WINS', False, self.GREY)
        surface = letters.get_rect(center = (self.WINDOW_WIDTH//3 + 5, self.TOP_MARGIN//2 + 6 * (self.SQUARES_SIZE + self.MARGIN)  + self.TOP_MARGIN//2 - 5))
        self.screen.blit(letters, surface)
        self.update_screen()


    def check_mouse_click_on_boxes(self, pos):
        """This function will be called when the user clicks on the grid of letters.
        It will check if the mouse click is inside an IA box, and if so, it will launch 
        the corresponding IA and update the game state accordingly.
        
        Args:
            pos: tuple, position of the cursor where the click is made.
        """
        print(pos)
        # Random IA Box
        if pos[0] > self.WINDOW_WIDTH-300 and pos[0] < self.WINDOW_WIDTH-280:
            if pos[1] > 80 and pos[1] < 100:
                self.checkboxes = [self.checkboxes[0], False, False, False, False, False]
                self.checkboxes[0] = not self.checkboxes[0]

                if self.checkboxes[0]:

                    nb_win = 0
                    nb_words = []

                    for j in range(1):

                        for i in range(len(self.WORDLE_ANSWERS_5_LETTERS)):

                            self.WORD_TO_GUESS = self.WORDLE_ANSWERS_5_LETTERS[i].upper()

                            random_ia = RandomIA(self.WORD_TO_GUESS, self.GUESSES)

                            all_colors = []

                            for chance_number in range(1, random_ia.CHANCES+1):
                                
                                self.GUESSES, WIN, DEFEAT, nb, colors = random_ia.random_IA(
                                    chance_number
                                )

                                all_colors.append(colors)

                                self.draw_window()
                                
                                if WIN:
                                    self.print_win_state()
                                    nb_win += 1
                                    nb_words.append(nb)
                                    try:
                                        self.df_state_action = pd.concat([self.df_state_action,random_ia.save_state_action(all_colors)])
                                    except:
                                        pass

                                if WIN or DEFEAT:
                                    #time.sleep(5)
                                    self.restart_game()
                                    break

                                self.update_screen()

                                # Random wait time - To humanize the input of values
                                #time.sleep(random.uniform(0, 2))

                    self.df_state_action.fillna(-1, inplace=True)
                    
                    # liste des noms de colonnes à supprimer
                    cols_to_drop = [
                        'action',
                        'guess',
                        'colored',
                        'answer'
                    ]

                    # suppression des colonnes
                    self.df_state_action = self.df_state_action.drop(columns=cols_to_drop)

                    self.df_state_action.to_csv("ia/RL_ia/data/training_set_random_ia_v1.csv")

                    print('WIN :', nb_win)
                    print(nb_words)


        # Algorithmic IA V1
        if pos[0] > self.WINDOW_WIDTH-300 and pos[0] < self.WINDOW_WIDTH-280:
            if pos[1] > 127 and pos[1] < 147:
                self.checkboxes = [False, self.checkboxes[1], False, False, False, False]
                self.checkboxes[1] = not self.checkboxes[1]

                if self.checkboxes[1]:


                    nb_win = 0
                    nb_words = []

                    algorithmic_ia = AlgorithmicIAV1(self.WORD_TO_GUESS, self.GUESSES)

                    for chance_number in range(1, algorithmic_ia.CHANCES+1):
                        
                        self.GUESSES, WIN, DEFEAT, nb = algorithmic_ia.algorithmic_IA(
                            chance_number
                        )

                        self.draw_window()
                        
                        if WIN:
                            self.print_win_state()
                            nb_win += 1
                            nb_words.append(nb)

                        # if DEFEAT:
                        #     print(self.WORD_TO_GUESS)

                        if WIN or DEFEAT:
                            time.sleep(5)
                            self.restart_game()
                            break

                        self.update_screen()

                        # Random wait time - To humanize the input of values
                        time.sleep(random.uniform(0, 2))

                    print('WIN :', nb_win)
                    print(nb_words)


        # Algorithmic IA V2
        if pos[0] > self.WINDOW_WIDTH-300 and pos[0] < self.WINDOW_WIDTH-280:
            if pos[1] > 171 and pos[1] < 191:
                self.checkboxes = [False, False, self.checkboxes[2], False, False, False]
                self.checkboxes[2] = not self.checkboxes[2]

                if self.checkboxes[2]:


                    nb_win = 0
                    nb_words = []

                    algorithmic_ia = AlgorithmicIAV2(self.WORD_TO_GUESS, self.GUESSES)

                    for chance_number in range(1, algorithmic_ia.CHANCES+1):
                        
                        self.GUESSES, WIN, DEFEAT, nb = algorithmic_ia.algorithmic_IA(
                            chance_number
                        )

                        self.draw_window()
                        
                        if WIN:
                            self.print_win_state()
                            nb_win += 1
                            nb_words.append(nb)

                        # if DEFEAT:
                        #     print(self.WORD_TO_GUESS)

                        if WIN or DEFEAT:
                            time.sleep(5)
                            self.restart_game()
                            break

                        self.update_screen()

                        # Random wait time - To humanize the input of values
                        time.sleep(random.uniform(0, 2))

                    print('WIN :', nb_win)
                    print(nb_words)


        # Algorithmic IA V3
        if pos[0] > self.WINDOW_WIDTH-300 and pos[0] < self.WINDOW_WIDTH-280:
            if pos[1] > 216 and pos[1] < 236:
                self.checkboxes = [False, False, False, self.checkboxes[3], False, False]
                self.checkboxes[3] = not self.checkboxes[3]

                if self.checkboxes[3]:


                    nb_win = 0
                    nb_words = []

                    algorithmic_ia = AlgorithmicIAV3(self.WORD_TO_GUESS, self.GUESSES)

                    for chance_number in range(1, algorithmic_ia.CHANCES+1):
                        
                        self.GUESSES, WIN, DEFEAT, nb = algorithmic_ia.algorithmic_IA(
                            chance_number
                        )

                        self.draw_window()
                        
                        if WIN:
                            self.print_win_state()
                            nb_win += 1
                            nb_words.append(nb)

                        # if DEFEAT:
                        #     print(self.WORD_TO_GUESS)

                        if WIN or DEFEAT:
                            time.sleep(5)
                            self.restart_game()
                            break

                        self.update_screen()

                        # Random wait time - To humanize the input of values
                        time.sleep(random.uniform(0, 2))

                    print('WIN :', nb_win)
                    print(nb_words)


        # Minimax
        if pos[0] > self.WINDOW_WIDTH-300 and pos[0] < self.WINDOW_WIDTH-280:
            if pos[1] > 262 and pos[1] < 282:
                self.checkboxes = [False, False, False, False, self.checkboxes[4], False]
                self.checkboxes[4] = not self.checkboxes[4]

                if self.checkboxes[4]:

                    cpu = int(cpu_count()*0.75)

                    nb_win = 0
                    nb_words = []
                    

                    ia = IAMiniMax(
                        5,
                        'dictionary_words_5.txt',
                        'dictionary_words_answers.txt',
                        self.GUESSES,
                        self.WORD_TO_GUESS,
                        fast_mode=False,
                        proc_count=cpu
                    )

                    for chance_number in range(1, ia.CHANCES+1):

                        self.GUESSES, WIN, DEFEAT, nb = ia.guess(
                            chance_number
                        )
                        self.draw_window()

                        if WIN:
                            self.print_win_state()
                            nb_win += 1
                            nb_words.append(nb)
                            print(self.GUESSES)
                            print('NB_WORDS :', nb)
                            print('\n')
                            self.restart_game()
                            time.sleep(15)
                            break

                        if DEFEAT:
                            print(self.GUESSES)
                            print('NB_WORDS :', nb)
                            print('\n')
                            self.restart_game()
                            time.sleep(15)

                        rslt = check_word(self.WORD_TO_GUESS.lower(), self.GUESSES[-1].lower())                            
                        ia.save_result(self.GUESSES[-1].lower(), rslt)
                        self.update_screen()

                    print('WIN :', nb_win)
                    print(nb_words)


        if pos[0] > self.WINDOW_WIDTH-300 and pos[0] < self.WINDOW_WIDTH-280:
            if pos[1] > 307 and pos[1] < 327:
                self.checkboxes = [False, False, False, False, False, self.checkboxes[5]]
                self.checkboxes[5] = not self.checkboxes[5]


        # Restart button
        if pos[0] > 720 and pos[0] < 790:
            if pos[1] > 395 and pos[1] < 470:
                self.restart_game()
