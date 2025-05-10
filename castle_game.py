import pygame
import sys
import random
from config import WIDTH, HEIGHT, WHITE, BLACK, COLORS, font, button_font, Button_COLORS
from card_system import CardSystem, Card  # Import your card system
from game_stats import GameStats


class Player:
    def __init__(self, name, initial_population, color):
        self.name = name
        self.population = initial_population
        self.soldier_count = 0
        self.farmer_count = 0
        self.hearts = 20
        self.color = color
        self.damage_bonus = 0
        self.allocated_this_round = False  # Track if population has been allocated this round
        # Card system attributes
        self.cards = []  # List to store player's cards
        self.has_counter_shield = False
        self.has_rebirth = False
        self.has_trap = False
        self.trap_duration = 0
        self.double_draw = False
        self.lucky_boost = 0

    def assign_population(self, soldier_count):
        """Assign population between soldiers and farmers"""
        if soldier_count > self.population:
            soldier_count = self.population

        self.soldier_count = soldier_count
        self.farmer_count = self.population - soldier_count

    def attack(self, opponent):
        """Attack the opponent with soldiers"""
        if self.soldier_count > 0:
            # Calculate damage (1 per soldier + any damage bonus)
            damage = self.soldier_count + self.damage_bonus  # Changed from multiplication to addition
            opponent.hearts -= damage
            if opponent.hearts < 0:
                opponent.hearts = 0
            return damage
        return 0

    def heal_soldiers(self):
        """Use farmers to heal hearts"""
        if self.farmer_count > 0:
            healing = min(self.farmer_count, 30 - self.hearts)
            self.hearts += healing
            return healing
        return 0

    def increase_damage(self):
        """Use farmers to increase attack damage"""
        if self.farmer_count > 0:
            bonus = 1 * self.farmer_count
            self.damage_bonus += bonus
            return bonus
        return 0


# Use Player as the base class for Enemy instead of having a separate class
class Enemy(Player):
    """Enemy class that inherits from Player but can have AI behavior"""

    def __init__(self, name, initial_population, color):
        super().__init__(name, initial_population, color)


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player1_rect = pygame.Rect(0, 0, width // 2, height)
        self.player2_rect = pygame.Rect(width // 2, 0, width // 2, height)

        # Draw simple castle representations
        self.castle_width = 100
        self.castle_height = 150

        # Load castle image for player 1
        try:
            self.castle1_image = pygame.image.load('castle_icon.png').convert_alpha()
            # Resize the image to match the castle dimensions
            self.castle1_image = pygame.transform.scale(self.castle1_image, (self.castle_width, self.castle_height))
            self.has_custom_castle = True
        except Exception as e:
            print(f"Error loading castle image: {e}")
            self.has_custom_castle = False

        try:
            self.castle2_image = pygame.image.load('castle_icon.png').convert_alpha()
            # Resize the image to match the castle dimensions
            self.castle2_image = pygame.transform.scale(self.castle2_image, (self.castle_width, self.castle_height))
            self.has_custom_castle = True
        except Exception as e:
            print(f"Error loading castle image: {e}")
            self.has_custom_castle = False

    def draw(self, screen, player1, player2):
        # Draw player1 side
        pygame.draw.rect(screen, player1.color, self.player1_rect)

        # Draw player2 side
        pygame.draw.rect(screen, player2.color, self.player2_rect)

        # Draw dividing line
        pygame.draw.line(screen, BLACK, (self.width // 2, 0), (self.width // 2, self.height), 3)

        # Draw simple castle representations
        castle_width = 100
        castle_height = 150

        # Player 1 castle (left side)
        castle1_pos = (self.width // 5, self.height // 2 - castle_height // 2)
        # Player 2 castle (right side)
        castle2_pos = (self.width // 2 + self.width // 5, self.height // 2 - castle_height // 2)

        # Player 1 castle (left side) - use custom image if available
        if self.has_custom_castle:
            screen.blit(self.castle1_image, castle1_pos)
        else:
            # Fallback to the original rectangle if image fails to load
            pygame.draw.rect(screen, (100, 100, 100),
                             (castle1_pos[0], castle1_pos[1], self.castle_width, self.castle_height))
            # Add simple castle details
            pygame.draw.rect(screen, (50, 50, 50),
                             (castle1_pos[0] + 30, castle1_pos[1] - 30, 40, 30))

        if self.has_custom_castle:
            screen.blit(self.castle2_image, castle2_pos)
        else:
            # Player 2 castle (left side) - use custom image if available
            pygame.draw.rect(screen, (100, 100, 100),
                             (castle2_pos[0], castle2_pos[1], castle_width, castle_height))
            # Add simple castle details
            pygame.draw.rect(screen, (50, 50, 50),
                             (castle2_pos[0] + 30, castle2_pos[1] - 30, 40, 30))

        # Draw health bars above the castles
        # Player 1 health bar
        health_bar_width = castle_width
        health_bar_height = 20
        health_bar_x = castle1_pos[0]
        health_bar_y = castle1_pos[1] - health_bar_height - 10

        # Background of health bar (empty)
        pygame.draw.rect(screen, (100, 100, 100),
                         (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Filled portion of health bar (green to red based on health)
        health_percentage = player1.hearts / 20.0
        fill_width = int(health_bar_width * health_percentage)

        # Color gradient from red to green based on health
        if health_percentage > 0.6:
            color = (0, 255, 0)  # Green
        elif health_percentage > 0.3:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red

        pygame.draw.rect(screen, color,
                         (health_bar_x, health_bar_y, fill_width, health_bar_height))

        # Player 2 health bar
        health_bar_x = castle2_pos[0]
        health_bar_y = castle2_pos[1] - health_bar_height - 10

        # Background of health bar
        pygame.draw.rect(screen, (100, 100, 100),
                         (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

        # Filled portion
        health_percentage = player2.hearts / 20.0
        fill_width = int(health_bar_width * health_percentage)

        # Color gradient
        if health_percentage > 0.6:
            color = (0, 255, 0)  # Green
        elif health_percentage > 0.3:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red

        pygame.draw.rect(screen, color,
                         (health_bar_x, health_bar_y, fill_width, health_bar_height))


class UIManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fonts = {
            'large': pygame.font.Font(None, 36),
            'medium': pygame.font.Font(None, 28),
            'small': pygame.font.Font(None, 24)
        }

        # Define UI elements
        self.soldier_slider = pygame.Rect(50, height - 100, 300, 20)
        self.soldier_slider_handle = pygame.Rect(50, height - 105, 10, 30)
        self.dragging = False

        # Action buttons
        button_width = 110
        button_height = 40
        button_margin = 20

        self.attack_button = pygame.Rect(width - button_width - button_margin,
                                         height - 4 * (button_height + button_margin),
                                         # Moved up to make room for card button
                                         button_width, button_height)

        self.heal_button = pygame.Rect(width - button_width - button_margin,
                                       height - 3 * (button_height + button_margin),
                                       button_width, button_height)

        self.damage_button = pygame.Rect(width - button_width - button_margin,
                                         height - 2 * (button_height + button_margin),
                                         button_width, button_height)

        # Add a button for playing cards
        self.play_card_button = pygame.Rect(width - button_width - button_margin,
                                            height - (button_height + button_margin),
                                            button_width, button_height)

        self.next_turn_button = pygame.Rect(width // 2 - button_width // 2,
                                            height - button_height - button_margin,
                                            button_width, button_height)

        self.soldier_percentage = 40  # Default to 40%

        # Card display area
        self.card_area_height = 120
        self.card_width = 80
        self.card_height = 100
        self.card_spacing = 10
        self.card_area = pygame.Rect(10, height - self.card_area_height - 150, width - 20, self.card_area_height)
        self.selected_card_index = None
        self.current_player_cards = []  # Store reference to current player's cards

    def draw_player_info(self, screen, player, x, y):
        """Draw player information"""
        # Draw player name
        name_text = self.fonts['large'].render(f"{player.name}", True, BLACK)
        screen.blit(name_text, (x, y))

        # Draw hearts
        hearts_text = self.fonts['medium'].render(f"Hearts: {player.hearts}", True, BLACK)
        screen.blit(hearts_text, (x, y + 40))

        # Draw population info
        pop_text = self.fonts['medium'].render(f"Population: {player.population}", True, BLACK)
        screen.blit(pop_text, (x, y + 70))

        # Draw soldier and farmer counts
        soldier_text = self.fonts['small'].render(f"Soldiers: {player.soldier_count}", True, BLACK)
        screen.blit(soldier_text, (x, y + 100))

        farmer_text = self.fonts['small'].render(f"Farmers: {player.farmer_count}", True, BLACK)
        screen.blit(farmer_text, (x, y + 130))

        # Draw damage bonus if any
        if player.damage_bonus > 0:
            bonus_text = self.fonts['small'].render(f"Damage Bonus: +{player.damage_bonus:.1f}", True, BLACK)
            screen.blit(bonus_text, (x, y + 160))

    # New method to draw player's cards
    def draw_cards(self, screen, player):
        # Store reference to current player's cards
        self.current_player_cards = player.cards

        # Draw card area background
        pygame.draw.rect(screen, (220, 220, 220), self.card_area, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.card_area, 2, border_radius=5)

        # Draw label
        cards_label = self.fonts['medium'].render("Your Cards:", True, BLACK)
        screen.blit(cards_label, (self.card_area.x + 10, self.card_area.y - 30))

        # Draw cards
        if not player.cards:
            no_cards_text = self.fonts['small'].render("No cards available", True, BLACK)
            screen.blit(no_cards_text, (self.card_area.x + 20, self.card_area.y + 40))
            return

        # Calculate how many cards to display (max based on width)
        max_cards_per_row = (self.card_area.width - 20) // (self.card_width + self.card_spacing)
        cards_to_display = min(len(player.cards), max_cards_per_row)

        # Calculate starting x position to center cards
        start_x = self.card_area.x + (self.card_area.width - (
                cards_to_display * (self.card_width + self.card_spacing) - self.card_spacing)) // 2

        # Draw each card
        for i, card in enumerate(player.cards[:cards_to_display]):
            card_x = start_x + i * (self.card_width + self.card_spacing)
            card_y = self.card_area.y + 10

            # Define card rect for click detection
            card_rect = pygame.Rect(card_x, card_y, self.card_width, self.card_height)

            # Draw card background (color based on rarity)
            card_color = self._get_rarity_color(card.rarity)

            # Highlight selected card
            if i == self.selected_card_index:
                # Draw selection highlight
                highlight_rect = pygame.Rect(card_x - 3, card_y - 3, self.card_width + 6, self.card_height + 6)
                pygame.draw.rect(screen, (255, 215, 0), highlight_rect, border_radius=5)  # Gold highlight

            # Draw card
            pygame.draw.rect(screen, card_color, card_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, card_rect, 2, border_radius=5)

            # Draw card name
            name_text = self.fonts['small'].render(card.name.split(' ')[0], True, BLACK)  # First word only
            if len(card.name.split(' ')) > 1:
                # If name has more than one word, draw second word on next line
                screen.blit(name_text, (card_x + (self.card_width - name_text.get_width()) // 2, card_y + 10))
                name_text2 = self.fonts['small'].render(card.name.split(' ')[1], True, BLACK)
                screen.blit(name_text2, (card_x + (self.card_width - name_text2.get_width()) // 2, card_y + 30))
            else:
                screen.blit(name_text, (card_x + (self.card_width - name_text.get_width()) // 2, card_y + 20))

            # Draw rarity indicator
            rarity_text = self.fonts['small'].render(card.rarity[0], True, BLACK)  # Just the first letter
            screen.blit(rarity_text, (card_x + 5, card_y + 5))

    def _get_rarity_color(self, rarity):
        """Return color based on card rarity"""
        if rarity == "LEGENDARY":
            return (255, 215, 0)  # Gold
        elif rarity == "EPIC":
            return (160, 32, 240)  # Purple
        elif rarity == "RARE":
            return (30, 144, 255)  # Blue
        else:  # COMMON
            return (192, 192, 192)  # Silver

    # Method to check if a card was clicked
    def check_card_click(self, pos):
        if not self.card_area.collidepoint(pos):
            return None

        if not self.current_player_cards:
            return None

        # Calculate how many cards can be displayed
        max_cards_per_row = (self.card_area.width - 20) // (self.card_width + self.card_spacing)
        cards_to_display = min(len(self.current_player_cards), max_cards_per_row)

        # Calculate starting x position for card row
        start_x = self.card_area.x + (self.card_area.width - (
                cards_to_display * (self.card_width + self.card_spacing) - self.card_spacing)) // 2

        # Check each card
        for i in range(cards_to_display):
            card_x = start_x + i * (self.card_width + self.card_spacing)
            card_y = self.card_area.y + 10
            card_rect = pygame.Rect(card_x, card_y, self.card_width, self.card_height)

            if card_rect.collidepoint(pos):
                print(f"Card {i} clicked!")  # Debug print
                return i

        return None

    def draw_ui(self, screen, player, current_turn, action_taken=False):
        """Draw all UI elements"""
        # Draw cards first
        self.draw_cards(screen, player)

        # Only show allocation UI if we're past the first round and player hasn't allocated yet
        if player.population > 0 and not player.allocated_this_round:
            # Draw slider for soldier allocation
            pygame.draw.rect(screen, BLACK, self.soldier_slider)

            # Calculate handle position based on percentage
            handle_x = self.soldier_slider.x + (self.soldier_slider.width * self.soldier_percentage // 100)
            self.soldier_slider_handle.x = handle_x - self.soldier_slider_handle.width // 2
            pygame.draw.rect(screen, Button_COLORS["white"], self.soldier_slider_handle)

            # Draw labels for slider (switched places)
            farmers_label = self.fonts['small'].render("Farmers", True, BLACK)
            soldiers_label = self.fonts['small'].render("Soldiers", True, BLACK)
            screen.blit(farmers_label, (self.soldier_slider.x, self.soldier_slider.y - 30))
            screen.blit(soldiers_label, (self.soldier_slider.x + self.soldier_slider.width - soldiers_label.get_width(),
                                         self.soldier_slider.y - 30))

            # Draw allocation text for the current population unit
            if player.population == 1:
                # For simplicity in Round 2, just show a binary choice
                allocation_text = self.fonts['small'].render(
                    f"Allocate new population unit as: {'Soldier' if self.soldier_percentage >= 50 else 'Farmer'}",
                    True, BLACK)
            else:
                # Show regular percentage for later rounds
                allocation_text = self.fonts['small'].render(
                    f"{self.soldier_percentage}% Soldiers, {100 - self.soldier_percentage}% Farmers",
                    True, BLACK)

            screen.blit(allocation_text,
                        (self.soldier_slider.x + (self.soldier_slider.width - allocation_text.get_width()) // 2,
                         self.soldier_slider.y + 30))

        # Draw action buttons if it's player's turn
        if current_turn == "player1" or current_turn == "player2":
            # Attack button - grayed out if action already taken
            button_color = COLORS["gray"] if action_taken else COLORS["red"]
            pygame.draw.rect(screen, button_color, self.attack_button)
            attack_text = self.fonts['small'].render("ATTACK", True, WHITE)
            screen.blit(attack_text, (self.attack_button.x + (self.attack_button.width - attack_text.get_width()) // 2,
                                      self.attack_button.y + (
                                              self.attack_button.height - attack_text.get_height()) // 2))

            # Heal button - grayed out if action already taken
            button_color = COLORS["gray"] if action_taken else COLORS["green"]
            pygame.draw.rect(screen, button_color, self.heal_button)
            heal_text = self.fonts['small'].render("HEAL", True, BLACK if not action_taken else WHITE)
            screen.blit(heal_text, (self.heal_button.x + (self.heal_button.width - heal_text.get_width()) // 2,
                                    self.heal_button.y + (self.heal_button.height - heal_text.get_height()) // 2))

            # Damage boost button - grayed out if action already taken
            button_color = COLORS["gray"] if action_taken else COLORS["blue"]
            pygame.draw.rect(screen, button_color, self.damage_button)
            damage_text = self.fonts['small'].render("BOOST DMG", True, WHITE)
            screen.blit(damage_text, (self.damage_button.x + (self.damage_button.width - damage_text.get_width()) // 2,
                                      self.damage_button.y + (
                                              self.damage_button.height - damage_text.get_height()) // 2))

            # Play card button - grayed out if action already taken or no card selected
            card_button_color = COLORS["gray"] if action_taken or self.selected_card_index is None else COLORS["purple"]
            pygame.draw.rect(screen, card_button_color, self.play_card_button)
            card_text = self.fonts['small'].render("PLAY CARD", True, WHITE)
            screen.blit(card_text,
                        (self.play_card_button.x + (self.play_card_button.width - card_text.get_width()) // 2,
                         self.play_card_button.y + (self.play_card_button.height - card_text.get_height()) // 2))

        # Draw next turn button
        pygame.draw.rect(screen, COLORS["blue"], self.next_turn_button)
        next_text = self.fonts['small'].render("NEXT TURN", True, WHITE)
        screen.blit(next_text, (self.next_turn_button.x + (self.next_turn_button.width - next_text.get_width()) // 2,
                                self.next_turn_button.y + (self.next_turn_button.height - next_text.get_height()) // 2))


class Game:
    def __init__(self, screen, player1_name, player2_name=None):
        self.screen = screen
        self.running = True
        self.current_round = 1
        self.current_turn = "player1"  # player1 or player2
        self.round_actions = []
        self.game_over = False
        self.winner = None
        self.waiting_for_next_player = False
        self.action_taken = False  # Flag to track if an action has been taken this turn
        self.message_queue = []  # Queue for multiple messages
        self.stats = GameStats()
        self.stats_saved = False

        # Create players
        player1_color = random.choice(list(COLORS.values()))
        player2_colors = [color for color in COLORS.values() if color != player1_color]
        player2_color = random.choice(player2_colors)

        # Two-player mode
        if player2_name:
            self.mode = "two_player"
            self.player1 = Player(player1_name, 1, player1_color)
            self.player2 = Player(player2_name, 1, player2_color)
        # Single-player mode with AI
        else:
            self.mode = "single_player"
            self.player1 = Player(player1_name, 1, player1_color)
            self.player2 = Enemy("Enemy Castle", 1, player2_color)

        # Initial round has no soldiers or farmers yet
        self.player1.soldier_count = 0
        self.player1.farmer_count = 0
        self.player2.soldier_count = 0
        self.player2.farmer_count = 0

        # Create map and UI manager
        self.map = Map(WIDTH, HEIGHT)
        self.ui = UIManager(WIDTH, HEIGHT)

        # Initialize card system
        self.card_system = CardSystem(self.player1, self.player2)

        # Setup initial message
        self.message = f"Game started! {self.player1.name}'s turn!"
        self.message_timer = 0

    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            # If waiting for player switch confirmation
            if self.waiting_for_next_player:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.waiting_for_next_player = False

                    # Switch player turn immediately
                    self.current_turn = "player2" if self.current_turn == "player1" else "player1"

                    # Process start-of-turn card effects
                    self.process_turn_start()

                    # Check if we've completed a full round (both players have taken turns)
                    if self.current_turn == "player1":
                        # Both players have taken their turns, proceed to next round
                        self.prepare_next_round()
                return

            # Handle UI events if game is not over
            if not self.game_over:
                player = self.get_current_player()

                # Handle slider events separate from action buttons
                if event.type == pygame.MOUSEMOTION and self.ui.dragging and not player.allocated_this_round:
                    # Update soldier percentage based on slider position
                    mouse_x = event.pos[0]
                    slider_start = self.ui.soldier_slider.x
                    slider_end = self.ui.soldier_slider.x + self.ui.soldier_slider.width

                    if mouse_x < slider_start:
                        self.ui.soldier_percentage = 0
                    elif mouse_x > slider_end:
                        self.ui.soldier_percentage = 100
                    else:
                        self.ui.soldier_percentage = int(
                            ((mouse_x - slider_start) / self.ui.soldier_slider.width) * 100)

                if event.type == pygame.MOUSEBUTTONUP and self.ui.dragging:
                    self.ui.dragging = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if slider handle is clicked
                    if not player.allocated_this_round and self.ui.soldier_slider_handle.collidepoint(event.pos):
                        self.ui.dragging = True

                    # Check if a card is clicked
                    card_clicked = self.ui.check_card_click(event.pos)
                    if card_clicked is not None and card_clicked < len(player.cards):
                        self.ui.selected_card_index = card_clicked
                        selected_card = player.cards[card_clicked]
                        print(f"Selected card: {selected_card.name}")  # Debug print
                        self.message = f"Selected: {selected_card.name} - {selected_card.description}"
                        self.message_timer = 120

                    # Check for button clicks
                    action = None

                    # Action buttons - only if not already taken action
                    if not self.action_taken:
                        if self.ui.attack_button.collidepoint(event.pos):
                            action = "attack"
                        elif self.ui.heal_button.collidepoint(event.pos):
                            action = "heal"
                        elif self.ui.damage_button.collidepoint(event.pos):
                            action = "damage"
                        elif self.ui.play_card_button.collidepoint(
                                event.pos) and self.ui.selected_card_index is not None:
                            action = "play_card"

                    # Next turn button always available
                    if self.ui.next_turn_button.collidepoint(event.pos):
                        action = "next_turn"

                    if action:
                        self.process_action(action)

    def process_turn_start(self):
        """Process turn start effects (Battle Chest and Endangered Mode)"""
        player = self.get_current_player()

        # Check for double draw effect
        if player.double_draw:
            card1 = self.card_system.check_battle_chest(player)
            if card1:
                player.cards.append(card1)
                self.message = f"{player.name} drew {card1.name} from Double Draw effect!"
                self.message_timer = 120

            card2 = self.card_system.check_battle_chest(player)
            if card2:
                player.cards.append(card2)
                self.message_queue.append(f"{player.name} drew {card2.name} from Double Draw effect!")

            # Reset double draw
            player.double_draw = False

        # Check Battle Chest (10% chance)
        card = self.card_system.check_battle_chest(player)
        if card:
            player.cards.append(card)
            if not self.message:
                self.message = f"{player.name} drew {card.name} from Battle Chest!"
                self.message_timer = 120
            else:
                self.message_queue.append(f"{player.name} drew {card.name} from Battle Chest!")

        # Check Endangered Mode
        if player.hearts < 10:
            card = self.card_system.check_endangered_mode(player)
            if card:
                player.cards.append(card)
                self.message_queue.append(f"{player.name} is in danger! Drew {card.name} from Endangered Mode!")

    def get_current_player(self):
        """Return the current player based on turn"""
        return self.player1 if self.current_turn == "player1" else self.player2

    def get_opponent(self):
        """Return the opponent of the current player"""
        return self.player2 if self.current_turn == "player1" else self.player1

    def process_action(self, action):
        """Process player actions"""
        current_player = self.get_current_player()
        opponent = self.get_opponent()

        self.stats.increment_turn()

        # Special case for first round, can only end turn
        if self.current_round == 1 and action == "next_turn":
            if self.mode == "two_player":
                self.switch_player()
            else:
                self.current_turn = "player2"
                self.ai_turn()
            self.round_actions.append("First round - no actions taken")
            return
        elif self.current_round == 1:
            self.message = "First round - only end turn is allowed."
            self.message_timer = 120
            return

        # Allocate population when first action is taken
        if not current_player.allocated_this_round and self.current_round > 1:
            # First allocate the population based on the slider
            soldier_count = int(current_player.population * self.ui.soldier_percentage / 100)
            current_player.soldier_count = soldier_count
            current_player.farmer_count = current_player.population - soldier_count
            current_player.allocated_this_round = True

            self.stats.record_unit_allocation(current_player.soldier_count, current_player.farmer_count)

        # Regular actions for round 2 and beyond
        if action == "attack":
            self.stats.record_action("attack")
            self.stats.record_battle()

            damage_dealt = current_player.soldier_count + current_player.damage_bonus

            # Check for counter shield
            if opponent.has_counter_shield:
                reflected_damage = int(damage_dealt * 0.5)
                current_player.hearts -= reflected_damage
                opponent.has_counter_shield = False  # Used up

                self.message = f"{current_player.name}'s attack was blocked by Counter Shield! {reflected_damage} damage reflected back!"
                self.message_timer = 120
                self.round_actions.append(f"{current_player.name}'s attack was countered and reflected")

                # TRACK HEARTS LOST BY CURRENT PLAYER
                current_player_type = "player1" if self.current_turn == "player1" else "player2"
                self.stats.record_hearts_lost(current_player_type, reflected_damage)

            # Check for trap card
            elif opponent.has_trap:
                trap_damage = 10
                current_player.hearts -= trap_damage
                current_player.damage_bonus -= int(current_player.soldier_count * 0.2)  # 20% less damage
                if current_player.damage_bonus < 0:
                    current_player.damage_bonus = 0

                # Apply damage to opponent
                opponent.hearts -= damage_dealt

                # TRACK HEARTS LOST BY BOTH PLAYERS
                current_player_type = "player1" if self.current_turn == "player1" else "player2"
                opponent_type = "player2" if self.current_turn == "player1" else "player1"
                self.stats.record_hearts_lost(current_player_type, trap_damage)
                self.stats.record_hearts_lost(opponent_type, damage_dealt)

                # Reset trap
                opponent.has_trap = False

                self.message = f"{current_player.name} attacked for {damage_dealt} damage but triggered a Trap Card!"
                self.message_queue.append(
                    f"{current_player.name} took {trap_damage} damage and will deal less damage for 2 turns!")
                self.message_timer = 120
                self.round_actions.append(f"{current_player.name} attacked and triggered a Trap Card")

                # Track hearts lost by both players
                self.stats.record_hearts_lost(self.current_turn, trap_damage)
                opponent_turn = "player2" if self.current_turn == "player1" else "player1"
                self.stats.record_hearts_lost(opponent_turn, damage_dealt)

                # Track hearts lost
                opponent_turn = "player2" if self.current_turn == "player1" else "player1"
                self.stats.record_hearts_lost(opponent_turn, damage_dealt)

            else:
                # Regular attack
                opponent.hearts -= damage_dealt

                # TRACK HEARTS LOST BY OPPONENT
                opponent_type = "player2" if self.current_turn == "player1" else "player1"
                self.stats.record_hearts_lost(opponent_type, damage_dealt)

                player_name = current_player.name
                self.message = f"{player_name} attacked for {damage_dealt} damage!"
                self.message_timer = 120
                self.round_actions.append(f"{player_name} attacked for {damage_dealt} damage")

            self.action_taken = True  # Mark that an action has been taken
            self.check_victory()

        elif action == "heal":
            healing = current_player.heal_soldiers()
            player_name = current_player.name
            self.message = f"{player_name} healed {healing} hearts!"
            self.message_timer = 120
            self.round_actions.append(f"{player_name} healed {healing} hearts")
            self.action_taken = True  # Mark that an action has been taken

            self.stats.record_action("heal")

        elif action == "damage":
            bonus = current_player.increase_damage()
            player_name = current_player.name
            self.message = f"{player_name} increased damage by {bonus:.1f}!"
            self.message_timer = 120
            self.round_actions.append(f"{player_name} increased damage by {bonus:.1f}")
            self.action_taken = True  # Mark that an action has been taken

            self.stats.record_action("damage")

        elif action == "play_card":
            # Play selected card
            print("Attempting to play card...")  # Debug print
            if self.ui.selected_card_index is not None and self.ui.selected_card_index < len(current_player.cards):
                card = current_player.cards[self.ui.selected_card_index]

                # Debug prints
                print(f"Trying to play card: {card.name}")
                print(f"Selected card index: {self.ui.selected_card_index}")
                print(f"Player has {len(current_player.cards)} cards")

                # Apply card effect
                result = card.use(current_player, opponent)
                print(f"Card use result: {result}")  # Debug print

                if result:
                    # Remove card from player's hand
                    current_player.cards.pop(self.ui.selected_card_index)

                    # Track card action
                    self.stats.record_action("play_card")

                    self.message = f"{current_player.name} used {card.name}!"
                    self.message_timer = 120
                    self.round_actions.append(f"{current_player.name} used {card.name}")
                    self.action_taken = True
                else:
                    self.message = f"Card couldn't be used in the current situation."
                    self.message_timer = 120

                # Reset selected card
                self.ui.selected_card_index = None
            else:
                print("No card selected or invalid index")  # Debug print

            self.stats.record_action("play_card")

        elif action == "next_turn":
            # In rounds after first, require an action
            if self.current_round > 1 and len(self.round_actions) == 0:
                self.message = "You must take an action before ending your turn!"
                self.message_timer = 120
                return

            # Reset action_taken flag for the next player
            self.action_taken = False

            # Reset selected card
            self.ui.selected_card_index = None

            # In two-player mode, switch to other player
            if self.mode == "two_player":
                self.switch_player()
            else:
                self.current_turn = "player2"
                self.ai_turn()

    def switch_player(self):
        """Switch to the other player with a confirmation screen"""
        # Set up the player switch
        next_player = "Player 2" if self.current_turn == "player1" else "Player 1"
        self.message = f"{next_player}'s turn. Press ENTER when ready."
        self.waiting_for_next_player = True

    def ai_turn(self):
        """Handle AI turn in single-player mode"""
        # Special case for first round
        if self.current_round == 1:
            self.message = "Enemy ended their first turn."
            self.message_timer = 120
            self.round_actions.append("Enemy first round - no actions taken")

            # If game is not over, prepare for next round
            if not self.game_over:
                self.prepare_next_round()
            return

        # Process card effects at turn start
        self.process_turn_start()

        # For rounds 2+, allocate population
        if not self.player2.allocated_this_round:
            # Enemy AI decides how to allocate population
            soldier_ratio = 0.7 if self.player2.hearts > 15 else 0.3
            soldier_count = int(self.player2.population * soldier_ratio)
            self.player2.soldier_count = soldier_count
            self.player2.farmer_count = self.player2.population - soldier_count
            self.player2.allocated_this_round = True

        # First decide if AI will use a card
        if self.player2.cards and random.random() < 0.6:  # 60% chance to use a card if available
            # Select a random card
            card_index = random.randint(0, len(self.player2.cards) - 1)
            card = self.player2.cards[card_index]

            # Use the card
            result = card.use(self.player2, self.player1)

            if result:
                # Remove card from AI's hand
                self.player2.cards.pop(card_index)

                self.message = f"Enemy used {card.name}!"
                self.message_timer = 120
                self.round_actions.append(f"Enemy used {card.name}")
            else:
                # If card couldn't be used, make a different action
                self.ai_action()
        else:
            # Make a regular action
            self.ai_action()

        # Check for victory
        self.check_victory()

        # Reset action_taken flag for the next player
        self.action_taken = False

        # If game is not over, prepare for next round
        if not self.game_over:
            self.prepare_next_round()

    def ai_action(self):
        """AI performs a regular action (attack, heal, or boost damage)"""
        ai_choice = random.random()

        if ai_choice < 0.3:  # 30% chance to heal
            # Track heal action
            self.stats.record_action("heal")

            healing = self.player2.heal_soldiers()
            self.message = f"Enemy healed {healing} hearts!"
            self.round_actions.append(f"Enemy healed {healing} hearts")

        elif ai_choice < 0.6:  # 30% chance to boost damage
            # Track damage boost action
            self.stats.record_action("damage")

            bonus = self.player2.increase_damage()
            self.message = f"Enemy increased damage by {bonus:.1f}!"
            self.round_actions.append(f"Enemy increased damage by {bonus:.1f}")

        else:  # 40% chance to attack
            # Track battle and attack action
            self.stats.record_battle()
            self.stats.record_action("attack")

            # Attack with card effects consideration
            damage_dealt = self.player2.soldier_count + self.player2.damage_bonus

            # Check for counter shield
            if self.player1.has_counter_shield:
                reflected_damage = int(damage_dealt * 0.5)
                self.player2.hearts -= reflected_damage
                self.player1.has_counter_shield = False  # Used up

                # TRACK HEARTS LOST BY ENEMY
                self.stats.record_hearts_lost("player2", reflected_damage)

                self.message = f"Enemy's attack was blocked by Counter Shield! {reflected_damage} damage reflected back!"
                self.message_timer = 120
                self.round_actions.append(f"Enemy's attack was countered and reflected")
            # Check for trap card
            elif self.player1.has_trap:
                trap_damage = 10
                self.player2.hearts -= trap_damage
                self.player2.damage_bonus -= int(self.player2.soldier_count * 0.2)  # 20% less damage
                if self.player2.damage_bonus < 0:
                    self.player2.damage_bonus = 0

                # Apply damage to player
                self.player1.hearts -= damage_dealt

                # TRACK HEARTS LOST BY BOTH PLAYERS
                self.stats.record_hearts_lost("player2", trap_damage)
                self.stats.record_hearts_lost("player1", damage_dealt)

                # Reset trap
                self.player1.has_trap = False

                self.message = f"Enemy attacked for {damage_dealt} damage but triggered a Trap Card!"
                self.message_queue.append(f"Enemy took {trap_damage} damage and will deal less damage for 2 turns!")
                self.message_timer = 120
                self.round_actions.append(f"Enemy attacked and triggered a Trap Card")

            else:
                # Regular attack
                self.player1.hearts -= damage_dealt

                # TRACK HEARTS LOST BY PLAYER
                self.stats.record_hearts_lost("player1", damage_dealt)

                self.message = f"Enemy attacked for {damage_dealt} damage!"
                self.message_timer = 120
                self.round_actions.append(f"Enemy attacked for {damage_dealt} damage")

    def check_victory(self):
        """Check if either player has won"""
        # Check for rebirth card effect first
        if self.player1.hearts <= 0 and self.player1.has_rebirth:
            self.player1.hearts = 10
            self.player1.has_rebirth = False
            self.message = f"{self.player1.name} was revived by Rebirth Card with 10 hearts!"
            self.message_timer = 120
            return

        if self.player2.hearts <= 0 and self.player2.has_rebirth:
            self.player2.hearts = 10
            self.player2.has_rebirth = False
            self.message = f"{self.player2.name} was revived by Rebirth Card with 10 hearts!"
            self.message_timer = 120
            return

        # Normal victory check
        if self.player1.hearts <= 0:
            self.game_over = True
            self.winner = "player2"
            self.message = f"Game Over! {self.player2.name} has defeated {self.player1.name}!"
            # Save game stats
            self.stats.save_game_stats(self.player1.name, self.player2.name, self.player2.name)
            self.stats_saved = True
        elif self.player2.hearts <= 0:
            self.game_over = True
            self.winner = "player1"
            self.message = f"Game Over! {self.player1.name} has defeated {self.player2.name}!"
            # Save game stats
            self.stats.save_game_stats(self.player1.name, self.player2.name, self.player1.name)
            self.stats_saved = True

    def prepare_next_round(self):
        """Prepare for the next round"""
        self.current_round += 1
        self.current_turn = "player1"
        self.round_actions = []
        self.action_taken = False  # Reset action taken flag for the new round

        # Set population to match the round number
        # This ensures Round 1 = 1 population, Round 2 = 2 population, Round 3 = 3 population, etc.
        self.player1.population = self.current_round
        self.player2.population = self.current_round

        # Reset allocation tracking
        self.player1.allocated_this_round = False
        self.player2.allocated_this_round = False

        # Update lucky charm counter
        if hasattr(self.player1, "lucky_boost") and self.player1.lucky_boost > 0:
            self.player1.lucky_boost -= 1

        if hasattr(self.player2, "lucky_boost") and self.player2.lucky_boost > 0:
            self.player2.lucky_boost -= 1

        self.message = f"Round {self.current_round} - {self.player1.name}'s turn! Allocate your new population."
        self.message_timer = 120

    def draw(self):
        """Draw the game"""
        # Clear screen
        self.screen.fill(WHITE)

        # If waiting for player switch, show only the transition screen
        if self.waiting_for_next_player:
            next_player = self.player2.name if self.current_turn == "player1" else self.player1.name
            transition_text = self.ui.fonts['large'].render(f"{next_player}'s Turn", True, BLACK)
            instruction_text = self.ui.fonts['medium'].render("Press ENTER when ready", True, BLACK)

            self.screen.blit(transition_text, (WIDTH // 2 - transition_text.get_width() // 2, HEIGHT // 2 - 50))
            self.screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 20))

            pygame.display.flip()
            return

        # Draw map
        self.map.draw(self.screen, self.player1, self.player2)

        # Draw player and enemy info
        self.ui.draw_player_info(self.screen, self.player1, 20, 20)
        self.ui.draw_player_info(self.screen, self.player2, WIDTH - 200, 20)

        # Draw UI elements if game is not over
        if not self.game_over:
            current_player = self.get_current_player()
            self.ui.draw_ui(self.screen, current_player, self.current_turn, self.action_taken)

        # Draw current round
        round_text = font.render(f"Round: {self.current_round}", True, BLACK)
        self.screen.blit(round_text, (WIDTH // 2 - round_text.get_width() // 2, 10))

        # Draw current turn
        current_player_name = self.player1.name if self.current_turn == "player1" else self.player2.name
        turn_text = font.render(f"Turn: {current_player_name}", True, BLACK)
        self.screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, 50))

        # Draw action status
        if self.current_round > 1:
            current_player = self.get_current_player()
            if not current_player.allocated_this_round:
                status_text = "Allocate your population!"
            elif not self.action_taken:
                status_text = "Choose an action!"
            else:
                status_text = "Action taken - End turn"

            action_text = font.render(status_text, True, BLACK)
            self.screen.blit(action_text, (WIDTH // 2 - action_text.get_width() // 2, 90))

        # Draw active card effects for both players
        y_offset = 190
        if self.player1.has_counter_shield:
            effect_text = self.ui.fonts['small'].render(f"{self.player1.name} has Counter Shield active", True,
                                                        (0, 100, 200))
            self.screen.blit(effect_text, (20, y_offset))
            y_offset += 25

        if self.player1.has_rebirth:
            effect_text = self.ui.fonts['small'].render(f"{self.player1.name} has Rebirth protection", True,
                                                        (255, 100, 100))
            self.screen.blit(effect_text, (20, y_offset))
            y_offset += 25

        if self.player1.has_trap:
            effect_text = self.ui.fonts['small'].render(f"{self.player1.name} has a Trap Card set", True, (200, 50, 50))
            self.screen.blit(effect_text, (20, y_offset))
            y_offset += 25

        if hasattr(self.player1, "lucky_boost") and self.player1.lucky_boost > 0:
            effect_text = self.ui.fonts['small'].render(f"{self.player1.name} has Lucky Charm active", True,
                                                        (100, 200, 100))
            self.screen.blit(effect_text, (20, y_offset))

        # Player 2 effects
        y_offset = 190
        if self.player2.has_counter_shield:
            effect_text = self.ui.fonts['small'].render(f"{self.player2.name} has Counter Shield active", True,
                                                        (0, 100, 200))
            self.screen.blit(effect_text, (WIDTH - 250, y_offset))
            y_offset += 25

        if self.player2.has_rebirth:
            effect_text = self.ui.fonts['small'].render(f"{self.player2.name} has Rebirth protection", True,
                                                        (255, 100, 100))
            self.screen.blit(effect_text, (WIDTH - 250, y_offset))
            y_offset += 25

        if self.player2.has_trap:
            effect_text = self.ui.fonts['small'].render(f"{self.player2.name} has a Trap Card set", True, (200, 50, 50))
            self.screen.blit(effect_text, (WIDTH - 250, y_offset))
            y_offset += 25

        if hasattr(self.player2, "lucky_boost") and self.player2.lucky_boost > 0:
            effect_text = self.ui.fonts['small'].render(f"{self.player2.name} has Lucky Charm active", True,
                                                        (100, 200, 100))
            self.screen.blit(effect_text, (WIDTH - 250, y_offset))

        # Draw message if timer is active
        if self.message_timer > 0:
            message_text = font.render(self.message, True, BLACK)
            self.screen.blit(message_text, (WIDTH // 2 - message_text.get_width() // 2, HEIGHT - 150))
            self.message_timer -= 1

            # If message timer expired and we have messages in queue, show the next one
            if self.message_timer <= 0 and self.message_queue:
                self.message = self.message_queue.pop(0)
                self.message_timer = 120

        # Draw game over message if game is over
        if self.game_over:
            game_over_text = self.ui.fonts['large'].render("GAME OVER", True, BLACK)
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))

            winner_name = self.player1.name if self.winner == "player1" else self.player2.name
            winner_text = self.ui.fonts['large'].render(f"Winner: {winner_name}", True, BLACK)
            self.screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))

            # Show return to menu button
            return_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 40)
            pygame.draw.rect(self.screen, COLORS["blue"], return_button)
            return_text = self.ui.fonts['small'].render("RETURN TO MENU", True, WHITE)
            self.screen.blit(return_text, (return_button.x + (return_button.width - return_text.get_width()) // 2,
                                           return_button.y + (return_button.height - return_text.get_height()) // 2))

            # Check for click on return button
            if pygame.mouse.get_pressed()[0]:
                if return_button.collidepoint(pygame.mouse.get_pos()):
                    # Save game stats before quitting if the game wasn't already over
                    if not self.stats_saved:
                        winner_name = self.player1.name if self.winner == "player1" else self.player2.name if self.winner == "player2" else "Game Abandoned"
                        self.stats.save_game_stats(self.player1.name, self.player2.name, winner_name)
                        self.stats_saved = True
                    self.running = False

        # Update display
        pygame.display.flip()

    def run(self):
        """Run the game loop"""
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(60)


def start_game(player1_name, player2_name=None):
    """Start the castle war game

    Args:
        player1_name: Name of the first player
        player2_name: Name of the second player (None for single-player mode)
    """
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Castle War Game")

    game = Game(screen, player1_name, player2_name)
    game.run()
