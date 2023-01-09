import random
import pygame

from random_ia import random_IA

def load_english_words(file_name):
    file = open(file_name)
    words = file.readlines()
    words = [word[:5].upper() for word in words]
    file.close()
    return words

ENGLISH_WORDS_5_LETTERS = load_english_words('dictionary_words_5.txt')

WORD_TO_GUESS = random.choice(ENGLISH_WORDS_5_LETTERS)

pygame.init()
pygame.font.init()

## Set up pygame window ##

# Dimensions
WINDOW_HEIGHT = 920
WINDOW_WIDTH = 950

WINDOW_GRID_WIDTH = 600

# Margins
MARGIN = 10
TOP_MARGIN = 100
LEFT_MARGIN = 100

# Colors
GREY = (128,128,128)
GREEN = (6, 214, 160)
ORANGE = (255, 128, 0)

# Letter squares
SQUARES_SIZE = (WINDOW_GRID_WIDTH - 4*MARGIN - 2*LEFT_MARGIN) // 5
LETTERS_FONT = pygame.font.SysFont("free sans bold", SQUARES_SIZE)
LETTERS_FONT_SMALL = pygame.font.SysFont("free sans bold", SQUARES_SIZE//2)
LETTERS_FONT_VERY_SMALL = pygame.font.SysFont("free sans bold", SQUARES_SIZE//3)

# User actions
INPUT = ""
GUESSES = []
ALPHABET = [['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            ['H', 'I', 'J', 'K', 'L', 'M', 'N'],
            ['O', 'P', 'Q', 'R', 'S', 'T', 'U'],
            [ 'V', 'W', 'X', 'Y', 'Z']]

GAME_OVER = False

checkbox1_pressed = False
checkbox2_pressed = False
checkbox3_pressed = False
checkbox4_pressed = False

checkboxes = [checkbox1_pressed, checkbox2_pressed, checkbox3_pressed, checkbox4_pressed]

def determine_color(guess, j):
    letter = guess[j]
    if letter == WORD_TO_GUESS[j]:
         return GREEN
    elif letter in WORD_TO_GUESS:
        n_target = WORD_TO_GUESS.count(letter)
        n_correct = 0
        n_occurrence = 0
        
        for i in range(5):
            if guess[i] == letter:
                if i <= j:
                    n_occurrence += 1
                if letter == WORD_TO_GUESS[i]:
                    n_correct += 1

        if n_target - n_correct - n_occurrence >= 0:
            return ORANGE
        else:
            return GREY
    else:
        return GREY

def determine_color_alphabet():
    LETTERS_TO_COLOR = []
    for word in GUESSES:
        if 'A' in word:
            if 'A' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(0,0), GREEN])
            else:
                LETTERS_TO_COLOR.append([(0,0), GREY])

        if 'B' in word:
            if 'B' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(0,1), GREEN])
            else:
                LETTERS_TO_COLOR.append([(0,1), GREY])

        if 'C' in word:
            if 'C' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(0,2), GREEN])
            else:
                LETTERS_TO_COLOR.append([(0,2), GREY])

        if 'D' in word:
            if 'D' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(0,3), GREEN])
            else:
                LETTERS_TO_COLOR.append([(0,3), GREY])

        if 'E' in word:
            if 'E' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(0,4), GREEN])
            else:
                LETTERS_TO_COLOR.append([(0,4), GREY])

        if 'F' in word:
            if 'F' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(0,5), GREEN])
            else:
                LETTERS_TO_COLOR.append([(0,5), GREY])

        if 'G' in word:
            if 'G' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(0,6), GREEN])
            else:
                LETTERS_TO_COLOR.append([(0,6), GREY])

        if 'H' in word:
            if 'H' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(1,0), GREEN])
            else:
                LETTERS_TO_COLOR.append([(1,0), GREY])

        if 'I' in word:
            if 'I' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(1,1), GREEN])
            else:
                LETTERS_TO_COLOR.append([(1,1), GREY])

        if 'J' in word:
            if 'J' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(1,2), GREEN])
            else:
                LETTERS_TO_COLOR.append([(1,2), GREY])

        if 'K' in word:
            if 'K' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(1,3), GREEN])
            else:
                LETTERS_TO_COLOR.append([(1,3), GREY])

        if 'L' in word:
            if 'L' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(1,4), GREEN])
            else:
                LETTERS_TO_COLOR.append([(1,4), GREY])

        if 'M' in word:
            if 'M' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(1,5), GREEN])
            else:
                LETTERS_TO_COLOR.append([(1,5), GREY])

        if 'N' in word:
            if 'N' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(1,6), GREEN])
            else:
                LETTERS_TO_COLOR.append([(1,6), GREY])

        if 'O' in word:
            if 'O' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(2,0), GREEN])
            else:
                LETTERS_TO_COLOR.append([(2,0), GREY])

        if 'P' in word:
            if 'P' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(2,1), GREEN])
            else:
                LETTERS_TO_COLOR.append([(2,1), GREY])

        if 'Q' in word:
            if 'Q' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(2,2), GREEN])
            else:
                LETTERS_TO_COLOR.append([(2,2), GREY])

        if 'R' in word:
            if 'R' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(2,3), GREEN])
            else:
                LETTERS_TO_COLOR.append([(2,3), GREY])

        if 'S' in word:
            if 'S' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(2,4), GREEN])
            else:
                LETTERS_TO_COLOR.append([(2,4), GREY])

        if 'T' in word:
            if 'T' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(2,5), GREEN])
            else:
                LETTERS_TO_COLOR.append([(2,5), GREY])

        if 'U' in word:
            if 'U' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(2,6), GREEN])
            else:
                LETTERS_TO_COLOR.append([(2,6), GREY])

        if 'V' in word:
            if 'V' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(3,1), GREEN])
            else:
                LETTERS_TO_COLOR.append([(3,1), GREY])

        if 'W' in word:
            if 'W' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(3,2), GREEN])
            else:
                LETTERS_TO_COLOR.append([(3,2), GREY])

        if 'X' in word:
            if 'X' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(3,3), GREEN])
            else:
                LETTERS_TO_COLOR.append([(3,3), GREY])

        if 'Y' in word:
            if 'Y' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(3,4), GREEN])
            else:
                LETTERS_TO_COLOR.append([(3,4), GREY])

        if 'Z' in word:
            if 'Z' in WORD_TO_GUESS:
                LETTERS_TO_COLOR.append([(3,5), GREEN])
            else:
                LETTERS_TO_COLOR.append([(3,5), GREY])

    return LETTERS_TO_COLOR

# Window title
pygame.display.set_caption("Wordle")

# Set up Screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Running loop
running = True
while running:

    # Background
    screen.fill("white")

    # Draw words guesses grid
    y = TOP_MARGIN//2
    for i in range(6):
        x = WINDOW_WIDTH//5
        for j in range(5):

            # Letter squares
            letter_square = pygame.Rect(x, y, SQUARES_SIZE, SQUARES_SIZE)
            pygame.draw.rect(screen, GREY, letter_square, width=2)

            # letters / words already guessed
            if i < len(GUESSES):
                color = determine_color(GUESSES[i], j)
                pygame.draw.rect(screen, color, letter_square, border_radius=3)
                letter = LETTERS_FONT.render(GUESSES[i][j], False, (255,255,255))
                surface = letter.get_rect(center = (x+SQUARES_SIZE//2, y+SQUARES_SIZE//2))
                screen.blit(letter, surface)

            # User input (next guess)
            if i == len(GUESSES) and j < len(INPUT):
                letter = LETTERS_FONT.render(INPUT[j], False, GREY)
                surface = letter.get_rect(center = (x+SQUARES_SIZE//2, y+SQUARES_SIZE//2))
                screen.blit(letter, surface)

            x += SQUARES_SIZE + MARGIN

        y += SQUARES_SIZE + MARGIN

    # Show correct answer after game over
    if len(GUESSES) == 6 and GUESSES[5] != WORD_TO_GUESS:
        GAME_OVER = True
        letters = LETTERS_FONT.render(WORD_TO_GUESS, False, GREY)
        surface = letters.get_rect(center = (WINDOW_WIDTH//2.3, TOP_MARGIN//2 + 6 * (SQUARES_SIZE + MARGIN)  + TOP_MARGIN//2))
        screen.blit(letters, surface)

    # Draw unguessed letters
    y = TOP_MARGIN//2 + 6 * (SQUARES_SIZE + MARGIN)  + TOP_MARGIN//2 + 50

    LETTERS_SIZE = (WINDOW_GRID_WIDTH - 4*MARGIN - 2*LEFT_MARGIN) // 7
    colors = determine_color_alphabet()

    for i in range(4):
        x = WINDOW_WIDTH//6
        if i != 3:
            for j in range(7):
                # Letter squares
                letter_square = pygame.Rect(x, y, LETTERS_SIZE, LETTERS_SIZE)
                color = (255,255,255)
                color_letter = GREY
                for item in colors:
                    if (i,j) == item[0]:
                        color = item[1]
                        color_letter = (255,255,255)
                pygame.draw.rect(screen, color, letter_square, border_radius=3)
                pygame.draw.rect(screen, GREY, letter_square, width=2)
                letter = LETTERS_FONT_SMALL.render(ALPHABET[i][j], False, color_letter)
                surface = letter.get_rect(center = (x+LETTERS_SIZE//2, y+LETTERS_SIZE//2))
                screen.blit(letter, surface)

                x += LETTERS_SIZE + 2*MARGIN

        else:
            for j in range(5):
                # Letter squares
                letter_square = pygame.Rect(x + (LETTERS_SIZE + 2*MARGIN), y, LETTERS_SIZE, LETTERS_SIZE)
                color = (255,255,255)
                color_letter = GREY
                for item in colors:
                    if (i,j) == item[0]:
                        color = item[1]
                        color_letter = (255,255,255)
                pygame.draw.rect(screen, color, letter_square, border_radius=3)
                pygame.draw.rect(screen, GREY, letter_square, width=2)
                letter = LETTERS_FONT_SMALL.render(ALPHABET[i][j], False, color_letter)
                surface = letter.get_rect(center = (x+ (LETTERS_SIZE + 2*MARGIN) + LETTERS_SIZE//2, y+LETTERS_SIZE//2))
                screen.blit(letter, surface)

                x += LETTERS_SIZE + 2*MARGIN

        y += LETTERS_SIZE + 2*MARGIN

    # Liste de choix - IA -

    # CheckBox 1
    checkbox1 = pygame.Rect(WINDOW_WIDTH-260, TOP_MARGIN//2 + 90, 20, 20)
    if not checkboxes[0]:
        pygame.draw.rect(screen, GREY, checkbox1, width=2)
    else:
        pygame.draw.rect(screen, GREY, checkbox1, border_radius=3)

    ia = LETTERS_FONT_VERY_SMALL.render("IA - RANDOM -", False, GREY)
    surface = ia.get_rect(center = (WINDOW_WIDTH-160, TOP_MARGIN//2 + 100))
    screen.blit(ia, surface)

    # CheckBox 2
    checkbox2 = pygame.Rect(WINDOW_WIDTH-260, TOP_MARGIN//2 + 135, 20, 20)
    if not checkboxes[1]:
        pygame.draw.rect(screen, GREY, checkbox2, width=2)
    else:
        pygame.draw.rect(screen, GREY, checkbox2, border_radius=3)
    pygame.draw.rect(screen, GREY, checkbox2, width=2)

    ia = LETTERS_FONT_VERY_SMALL.render("IA - ALGORITHM -", False, GREY)
    surface = ia.get_rect(center = (WINDOW_WIDTH-148, TOP_MARGIN//2 + 147))
    screen.blit(ia, surface)

    # CheckBox 3
    checkbox3 = pygame.Rect(WINDOW_WIDTH-260, TOP_MARGIN//2 + 180, 20, 20)
    if not checkboxes[2]:
        pygame.draw.rect(screen, GREY, checkbox3, width=2)
    else:
        pygame.draw.rect(screen, GREY, checkbox3, border_radius=3)
    pygame.draw.rect(screen, GREY, checkbox3, width=2)

    ia = LETTERS_FONT_VERY_SMALL.render("IA - MINIMAX -", False, GREY)
    surface = ia.get_rect(center = (WINDOW_WIDTH-163, TOP_MARGIN//2 + 191))
    screen.blit(ia, surface)

    # CheckBox 3
    checkbox4 = pygame.Rect(WINDOW_WIDTH-260, TOP_MARGIN//2 + 225, 20, 20)
    if not checkboxes[3]:
        pygame.draw.rect(screen, GREY, checkbox4, width=2)
    else:
        pygame.draw.rect(screen, GREY, checkbox4, border_radius=3)
    pygame.draw.rect(screen, GREY, checkbox4, width=2)

    ia = LETTERS_FONT_VERY_SMALL.render("IA - DEEP LEARNING -", False, GREY)
    surface = ia.get_rect(center = (WINDOW_WIDTH-130, TOP_MARGIN//2 + 236))
    screen.blit(ia, surface)

    

    # Update screen
    pygame.display.flip()

    # User interaction
    for event in pygame.event.get():

        # Quit game
        if event.type == pygame.QUIT:
            running = False

        # Detect user mouse
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            if pos[0] > WINDOW_WIDTH-260 and pos[0] < WINDOW_WIDTH-240:
                if pos[1] > 140 and pos[1] < 160:
                    checkboxes = [checkboxes[0], False, False, False]
                    checkboxes[0] = not checkboxes[0]

                    # Lancer l'IA Random
                    GUESSES = random_IA(WORD_TO_GUESS)

            if pos[0] > WINDOW_WIDTH-260 and pos[0] < WINDOW_WIDTH-240:
                if pos[1] > 187 and pos[1] < 207:
                    checkboxes = [False, checkboxes[1], False, False]
                    checkboxes[1] = not checkboxes[1]

            if pos[0] > WINDOW_WIDTH-260 and pos[0] < WINDOW_WIDTH-240:
                if pos[1] > 232 and pos[1] < 252:
                    checkboxes = [False, False, checkboxes[2], False]
                    checkboxes[2] = not checkboxes[2]

            if pos[0] > WINDOW_WIDTH-260 and pos[0] < WINDOW_WIDTH-240:
                if pos[1] > 277 and pos[1] < 297:
                    checkboxes = [False, False, False, checkboxes[3]]
                    checkboxes[3] = not checkboxes[3]

        # User presses a key
        elif event.type == pygame.KEYDOWN:

            # ESC to quit the game
            if event.key == pygame.K_ESCAPE:
                running = False


            # Write back
            if event.key == pygame.K_BACKSPACE:
                if len(INPUT) > 0:
                    INPUT = INPUT[:len(INPUT)-1]

            elif event.key == pygame.K_RETURN:
                if len(INPUT) == 5 and INPUT in ENGLISH_WORDS_5_LETTERS:
                    GUESSES.append(INPUT)
                    GAME_OVER = True if INPUT == WORD_TO_GUESS else False
                    INPUT = ""
                else:
                    INPUT = ""

            elif event.key == pygame.K_SPACE:
                GAME_OVER = False
                WORD_TO_GUESS = random.choice(ENGLISH_WORDS_5_LETTERS)
                GUESSES = []
                INPUT = ""

            elif len(INPUT) < 5 and not GAME_OVER:
                INPUT = INPUT + event.unicode.upper()
