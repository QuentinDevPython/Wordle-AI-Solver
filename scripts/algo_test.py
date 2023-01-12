WORD_TO_GUESS = "APPLE"

GREY = (128,128,128)
GREEN = (6, 214, 160)
ORANGE = (255, 128, 0)


def determine_color_for_ia(guess, j):
        """Determine the color of the letter based on whether the 
        guess is correct, partially correct, or incorrect.
        
        Args:
            guess (str): The current guess word
            j (int): The index of the letter in the word
        Returns:
            tuple: The RGB color code
        """

        letter = guess[j]
        if letter == WORD_TO_GUESS[j]:
            return "GREEN"
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
                return "ORANGE"
            else:
                return "GREY"
        else:
            return "GREY"

guess = "PANAN"

colors = []

for j in range(5):
    color = determine_color(guess, j)
    colors.append((j, color))

print(colors)