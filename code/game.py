import pygame
import random
import time

from utils import WordDictionary
from random_ia import RandomIA
from algorithmic_ia import AlgorithmicIA


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

        # Randomly choose a word to find in the game
        self.WORD_TO_GUESS = random.choice(
            self.ENGLISH_WORDS_5_LETTERS
        ).upper()

        # Init pygame
        pygame.init()
        pygame.font.init()

        # Init the window dimensions
        self.WINDOW_HEIGHT = 920
        self.WINDOW_WIDTH = 950
        self.WINDOW_GRID_WIDTH = 600

        # Margins
        self.MARGIN = 10
        self.TOP_MARGIN = 100
        self.LEFT_MARGIN = 100

        # Colors
        self.GREY = (128,128,128)
        self.GREEN = (6, 214, 160)
        self.ORANGE = (255, 128, 0)

        # Squares size
        self.SQUARES_SIZE = (self.WINDOW_GRID_WIDTH - 4*self.MARGIN - 2*self.LEFT_MARGIN) // 5

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
            self.SQUARES_SIZE//3
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

        self.checkboxes = [
            checkbox1_pressed, 
            checkbox2_pressed,
            checkbox3_pressed,
            checkbox4_pressed
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
                    if i < j:
                        n_occurrence += 1
                    if letter == self.WORD_TO_GUESS[i]:
                        n_correct += 1

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
            x = self.WINDOW_WIDTH//5
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
        y = self.TOP_MARGIN//2 + 6 * (self.SQUARES_SIZE + self.MARGIN)  + self.TOP_MARGIN//2 + 50

        LETTERS_SIZE = (self.WINDOW_GRID_WIDTH - 4*self.MARGIN - 2*self.LEFT_MARGIN) // 7
        colors = self.determine_color_alphabet()

        for i in range(4):
            x = self.WINDOW_WIDTH//6
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
        checkbox1 = pygame.Rect(self.WINDOW_WIDTH-260, self.TOP_MARGIN//2 + 90, 20, 20)
        if not self.checkboxes[0]:
            pygame.draw.rect(self.screen, self.GREY, checkbox1, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox1, border_radius=3)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - RANDOM -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-160, self.TOP_MARGIN//2 + 100))
        self.screen.blit(ia, surface)

        # CheckBox 2
        checkbox2 = pygame.Rect(self.WINDOW_WIDTH-260, self.TOP_MARGIN//2 + 135, 20, 20)
        if not self.checkboxes[1]:
            pygame.draw.rect(self.screen, self.GREY, checkbox2, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox2, border_radius=3)
        pygame.draw.rect(self.screen, self.GREY, checkbox2, width=2)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - ALGORITHM -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-148, self.TOP_MARGIN//2 + 147))
        self.screen.blit(ia, surface)

        # CheckBox 3
        checkbox3 = pygame.Rect(self.WINDOW_WIDTH-260, self.TOP_MARGIN//2 + 180, 20, 20)
        if not self.checkboxes[2]:
            pygame.draw.rect(self.screen, self.GREY, checkbox3, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox3, border_radius=3)
        pygame.draw.rect(self.screen, self.GREY, checkbox3, width=2)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - MINIMAX -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-163, self.TOP_MARGIN//2 + 191))
        self.screen.blit(ia, surface)

        # CheckBox 3
        checkbox4 = pygame.Rect(self.WINDOW_WIDTH-260, self.TOP_MARGIN//2 + 225, 20, 20)
        if not self.checkboxes[3]:
            pygame.draw.rect(self.screen, self.GREY, checkbox4, width=2)
        else:
            pygame.draw.rect(self.screen, self.GREY, checkbox4, border_radius=3)
        pygame.draw.rect(self.screen, self.GREY, checkbox4, width=2)

        ia = self.LETTERS_FONT_VERY_SMALL.render("IA - DEEP LEARNING -", False, self.GREY)
        surface = ia.get_rect(center = (self.WINDOW_WIDTH-130, self.TOP_MARGIN//2 + 236))
        self.screen.blit(ia, surface)


    def show_correct_answer(self):
        """Show the correct answer on the screen after gameover"""

        if len(self.GUESSES) == 6 and self.GUESSES[5] != self.WORD_TO_GUESS:
            GAME_OVER = True
            letters = self.LETTERS_FONT.render(self.WORD_TO_GUESS, False, self.GREY)
            surface = letters.get_rect(center = (self.WINDOW_WIDTH//2.3, self.TOP_MARGIN//2 + 6 * (self.SQUARES_SIZE + self.MARGIN)  + self.TOP_MARGIN//2))
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

        self.checkboxes = [False, False, False, False]
        self.GAME_OVER = False
        self.WORD_TO_GUESS = random.choice(self.ENGLISH_WORDS_5_LETTERS).upper()
        self.GUESSES = []
        self.INPUT = ""

    
    def print_win_state(self):
        """Show a win message on the screen when an IA wins the game"""
        letters = self.LETTERS_FONT.render('IA WINS', False, self.GREY)
        surface = letters.get_rect(center = (self.WINDOW_WIDTH//2.3 - 10, self.TOP_MARGIN//2 + 6 * (self.SQUARES_SIZE + self.MARGIN)  + self.TOP_MARGIN//2))
        self.screen.blit(letters, surface)
        self.update_screen()


    def check_mouse_click_on_boxes(self, pos):
        """This function will be called when the user clicks on the grid of letters.
        It will check if the mouse click is inside an IA box, and if so, it will launch 
        the corresponding IA and update the game state accordingly.
        
        Args:
            pos: tuple, position of the cursor where the click is made.
        """

        # Random IA Box
        if pos[0] > self.WINDOW_WIDTH-260 and pos[0] < self.WINDOW_WIDTH-240:
            if pos[1] > 140 and pos[1] < 160:
                self.checkboxes = [self.checkboxes[0], False, False, False]
                self.checkboxes[0] = not self.checkboxes[0]

                if self.checkboxes[0]:

                    random_ia = RandomIA(self.WORD_TO_GUESS, self.GUESSES)

                    for chance_number in range(1, random_ia.CHANCES+1):
                        
                        self.GUESSES, WIN, DEFEAT = random_ia.random_IA(
                            chance_number
                        )

                        self.draw_window()
                        
                        if WIN:
                            self.print_win_state()

                        if WIN or DEFEAT:
                            time.sleep(5)
                            self.restart_game()
                            break

                        self.update_screen()

                        # Random wait time - To humanize the input of values
                        time.sleep(random.uniform(0, 2))


        if pos[0] > self.WINDOW_WIDTH-260 and pos[0] < self.WINDOW_WIDTH-240:
            if pos[1] > 187 and pos[1] < 207:
                self.checkboxes = [False, self.checkboxes[1], False, False]
                self.checkboxes[1] = not self.checkboxes[1]

                if self.checkboxes[1]:

                    nb_win = 0
                    nb_words = []

                    for i in range(3000):

                        algorithmic_ia = AlgorithmicIA(self.WORD_TO_GUESS, self.GUESSES)

                        for chance_number in range(1, algorithmic_ia.CHANCES+1):
                            
                            self.GUESSES, WIN, DEFEAT, nb = algorithmic_ia.algorithmic_IA(
                                chance_number
                            )

                            self.draw_window()
                            
                            if WIN:
                                self.print_win_state()
                                nb_win += 1
                                nb_words.append(nb)

                            if WIN or DEFEAT:
                                #time.sleep(5)
                                self.restart_game()
                                break

                            self.update_screen()

                            # Random wait time - To humanize the input of values
                            #time.sleep(random.uniform(0, 2))

                    print('WIN :', nb_win)
                    print(nb_words)


        if pos[0] > self.WINDOW_WIDTH-260 and pos[0] < self.WINDOW_WIDTH-240:
            if pos[1] > 232 and pos[1] < 252:
                self.checkboxes = [False, False, self.checkboxes[2], False]
                self.checkboxes[2] = not self.checkboxes[2]

        if pos[0] > self.WINDOW_WIDTH-260 and pos[0] < self.WINDOW_WIDTH-240:
            if pos[1] > 277 and pos[1] < 297:
                self.checkboxes = [False, False, False, self.checkboxes[3]]
                self.checkboxes[3] = not self.checkboxes[3]
