import pygame
import sys
from config import WIDTH, HEIGHT, WHITE, BLACK, font, button_font
from castle_game import start_game  # Import the start_game function from castle_game.py


def draw_menu(screen, survival_button, sandbox_button, two_player_button,tutorial_button,  quit_button):
    screen.fill(WHITE)

    # Title
    title_text = font.render("Castle War Game", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # Buttons
    pygame.draw.rect(screen, BLACK, survival_button)
    pygame.draw.rect(screen, BLACK, sandbox_button)
    pygame.draw.rect(screen, BLACK, two_player_button)
    pygame.draw.rect(screen, BLACK, tutorial_button)
    pygame.draw.rect(screen, BLACK, quit_button)

    survival_text = button_font.render("Survival Game", True, WHITE)
    sandbox_text = button_font.render("Single Player", True, WHITE)
    two_player_text = button_font.render("Two Players", True, WHITE)
    tutorial_button_text = button_font.render("Tutorial", True, WHITE)
    quit_text = button_font.render("Quit", True, WHITE)

    screen.blit(survival_text, (survival_button.x + 15, survival_button.y + 10))
    screen.blit(sandbox_text, (sandbox_button.x + 15, sandbox_button.y + 10))
    screen.blit(two_player_text, (two_player_button.x + 15, two_player_button.y + 10))
    screen.blit(tutorial_button_text, (tutorial_button.x + 15, tutorial_button.y + 10))
    screen.blit(quit_text, (quit_button.x + 15, quit_button.y + 10))

    pygame.display.flip()


def get_player_names(screen, two_player=False):
    """Prompt the user to enter player name(s)."""
    running = True
    player1_name = ""
    player2_name = ""
    active_input = "player1"  # Which input is currently active

    input_font = pygame.font.Font(None, 36)
    text_color = BLACK
    input_rect_player1 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 40)
    input_rect_player2 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 40) if two_player else None

    while running:
        screen.fill(WHITE)

        # Display instructions for player 1
        instruction_text1 = input_font.render("Enter Player 1 name:", True, text_color)
        screen.blit(instruction_text1, (WIDTH // 2 - instruction_text1.get_width() // 2, HEIGHT // 2 - 100))

        # Display player 1 input box
        pygame.draw.rect(screen, BLACK, input_rect_player1, 2)
        name_text1 = input_font.render(player1_name, True, text_color)
        screen.blit(name_text1, (input_rect_player1.x + 10, input_rect_player1.y + 10))

        # If two player mode, show second input box
        if two_player:
            instruction_text2 = input_font.render("Enter Player 2 name:", True, text_color)
            screen.blit(instruction_text2, (WIDTH // 2 - instruction_text2.get_width() // 2, HEIGHT // 2))

            pygame.draw.rect(screen, BLACK, input_rect_player2, 2)
            name_text2 = input_font.render(player2_name, True, text_color)
            screen.blit(name_text2, (input_rect_player2.x + 10, input_rect_player2.y + 10))

        # Show which input is active
        if active_input == "player1":
            active_text = input_font.render("(typing...)", True, (0, 128, 0))
            screen.blit(active_text, (input_rect_player1.x + input_rect_player1.width + 10, input_rect_player1.y + 10))
        elif active_input == "player2":
            active_text = input_font.render("(typing...)", True, (0, 128, 0))
            screen.blit(active_text, (input_rect_player2.x + input_rect_player2.width + 10, input_rect_player2.y + 10))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check which input box was clicked
                if input_rect_player1.collidepoint(event.pos):
                    active_input = "player1"
                elif two_player and input_rect_player2.collidepoint(event.pos):
                    active_input = "player2"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if active_input == "player1" and player1_name:
                        if two_player:
                            if player2_name:  # Both names are entered
                                running = False
                            else:
                                active_input = "player2"  # Move to player 2 input
                        else:
                            running = False  # Single player mode
                    elif active_input == "player2" and player2_name:
                        running = False
                    else:
                        # Display a message if the input is invalid
                        error_text = input_font.render("Please enter a valid name.", True, (255, 0, 0))
                        screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT // 2 + 150))
                elif event.key == pygame.K_TAB:
                    # Switch between input fields with Tab
                    if two_player:
                        active_input = "player2" if active_input == "player1" else "player1"
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == "player1":
                        player1_name = player1_name[:-1]
                    elif active_input == "player2":
                        player2_name = player2_name[:-1]
                else:
                    if active_input == "player1" and len(player1_name) < 20:
                        player1_name += event.unicode
                    elif active_input == "player2" and len(player2_name) < 20:
                        player2_name += event.unicode

        pygame.display.flip()

    return (player1_name, player2_name) if two_player else player1_name


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Castle War Game Menu")

    # Define buttons
    button_y_start = HEIGHT // 2 - 60
    button_height = 40
    button_spacing = 20

    survival_button = pygame.Rect(WIDTH // 2 - 75, button_y_start, 150, button_height)
    sandbox_button = pygame.Rect(WIDTH // 2 - 75, button_y_start + button_height + button_spacing, 150, button_height)
    two_player_button = pygame.Rect(WIDTH // 2 - 75, button_y_start + 2 * (button_height + button_spacing), 150,
                                    button_height)
    tutorial_button = pygame.Rect(WIDTH // 2 - 75, button_y_start + 3 * (button_height + button_spacing), 150,
                                  button_height)
    quit_button = pygame.Rect(WIDTH // 2 - 75, button_y_start + 4 * (button_height + button_spacing), 150,
                              button_height)

    running = True
    while running:
        draw_menu(screen, survival_button, sandbox_button, two_player_button,tutorial_button, quit_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sandbox_button.collidepoint(event.pos):
                    # Single player mode
                    player_name = get_player_names(screen, False)
                    if player_name:  # Check if valid input
                        start_game(player_name)  # Start single player game
                    else:
                        print("Invalid input, please try again.")

                elif two_player_button.collidepoint(event.pos):
                    # Two player mode
                    player1_name, player2_name = get_player_names(screen, True)
                    if player1_name and player2_name:  # Check if valid input
                        start_game(player1_name, player2_name)  # Start two player game
                    else:
                        print("Invalid input, please try again.")

                elif survival_button.collidepoint(event.pos):
                    print("Survival mode is not implemented yet.")

                elif quit_button.collidepoint(event.pos):
                    running = False  # Exit the game


if __name__ == "__main__":
    main_menu()
