import pygame
from game import Game


if __name__ == "__main__":

    game = Game()

    # Running game loop
    running = True
    while running:

        game.draw_window()

        # User interaction
        for event in pygame.event.get():

            # Quit game
            if event.type == pygame.QUIT:
                running = False

            # Detect user mouse
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                game.check_mouse_click_on_boxes(pos)        

            # User presses a key
            elif event.type == pygame.KEYDOWN:

                # ESC to quit the game
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_BACKSPACE:
                    game.erase_letter()

                elif event.key == pygame.K_RETURN:
                    game.validate_guess_word()

                elif event.key == pygame.K_SPACE:
                    game.restart_game()

                else:
                    game.write_letter(event)
