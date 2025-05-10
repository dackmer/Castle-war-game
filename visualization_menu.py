"""
Data Visualization Menu System for Castle War Game
This file adds a visualization dashboard to the main menu with scrolling functionality
"""

import pygame
import sys
import os
from config import WIDTH, HEIGHT, WHITE, BLACK, COLORS, font, button_font

class VisualizationDashboard:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.active_category = None
        self.visualizations_path = "game_stats_visualizations"

        # Scrolling variables
        self.scroll_y = 0
        self.max_scroll = 0
        self.scroll_speed = 20

        # Check if visualizations directory exists
        if not os.path.exists(self.visualizations_path):
            self.vis_available = False
        else:
            self.vis_available = any(file.endswith('.png') for file in os.listdir(self.visualizations_path))

        # Define menu categories
        self.categories = [
            {"name": "Player Stats", "images": ["win_loss_distribution.png", "player_improvement.png"]},
            {"name": "Unit Analysis", "images": ["unit_allocation_comparison.png", "unit_allocation_pie_chart.png"]},
            {"name": "Battle Stats", "images": ["battle_count_chart.png", "hearts_lost_histogram.png", "hearts_lost_per_game.png"]},
            {"name": "Game Length", "images": ["game_duration_trend.png", "game_duration_box_plot.png"]},
            {"name": "Action Types", "images": ["action_type_distribution.png"]},
            {"name": "Summary", "images": ["statistical_table.png"]}
        ]

        # Load font for buttons and headings
        self.menu_font = pygame.font.Font(None, 28)
        self.heading_font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)

        # Preload background for buttons
        self.button_bg = pygame.Surface((200, 40))
        self.button_bg.fill(COLORS["blue"])

        # Setup menu buttons area
        self.menu_width = 220
        self.menu_area = pygame.Rect(0, 0, self.menu_width, HEIGHT)

        # Content area for visualizations
        self.content_area = pygame.Rect(self.menu_width, 100, WIDTH - self.menu_width, HEIGHT - 150)

        # Back button
        self.back_button = pygame.Rect(WIDTH - 120, HEIGHT - 50, 100, 40)

        # Scroll buttons
        self.scroll_up_button = pygame.Rect(WIDTH - 50, 110, 40, 40)
        self.scroll_down_button = pygame.Rect(WIDTH - 50, HEIGHT - 100, 40, 40)

        # Preload images if available
        self.images = {}
        if self.vis_available:
            self.preload_images()

    def preload_images(self):
        """Preload all visualization images"""
        for category in self.categories:
            for image_name in category["images"]:
                image_path = os.path.join(self.visualizations_path, image_name)
                if os.path.exists(image_path):
                    try:
                        img = pygame.image.load(image_path)
                        # Scale image to fit in visualization area
                        max_width = WIDTH - self.menu_width - 80  # 40px padding on each side
                        max_height = HEIGHT - 200  # Leave space for title and bottom area

                        # Calculate scaling factor
                        width_ratio = max_width / img.get_width()
                        height_ratio = max_height / img.get_height()
                        scale_factor = min(width_ratio, height_ratio, 1.0)  # Don't upscale if smaller

                        new_width = int(img.get_width() * scale_factor)
                        new_height = int(img.get_height() * scale_factor)

                        scaled_img = pygame.transform.smoothscale(img, (new_width, new_height))
                        self.images[image_name] = scaled_img
                    except pygame.error as e:
                        print(f"Error loading image {image_name}: {e}")
                        self.images[image_name] = None

    def run(self):
        """Main loop for the visualization dashboard"""
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if back button was clicked
                if self.back_button.collidepoint(event.pos):
                    self.running = False
                    return

                # Check if a category button was clicked
                mouse_pos = pygame.mouse.get_pos()
                if self.menu_area.collidepoint(mouse_pos):
                    for i, category in enumerate(self.categories):
                        button_rect = pygame.Rect(10, 100 + i * 50, self.menu_width - 20, 40)
                        if button_rect.collidepoint(mouse_pos):
                            if self.vis_available:
                                self.active_category = category["name"]
                                self.scroll_y = 0  # Reset scroll position when changing categories
                            break

                # Check for scroll button clicks
                if self.scroll_up_button.collidepoint(event.pos):
                    self.scroll_y = max(0, self.scroll_y - self.scroll_speed * 3)
                elif self.scroll_down_button.collidepoint(event.pos):
                    self.scroll_y = min(self.max_scroll, self.scroll_y + self.scroll_speed * 3)

                # Mouse wheel scrolling in content area
                if self.content_area.collidepoint(mouse_pos):
                    if event.button == 4:  # Scroll up
                        self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
                    elif event.button == 5:  # Scroll down
                        self.scroll_y = min(self.max_scroll, self.scroll_y + self.scroll_speed)

            # Handle keyboard scrolling
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.scroll_y = max(0, self.scroll_y - self.scroll_speed)
                elif event.key == pygame.K_DOWN:
                    self.scroll_y = min(self.max_scroll, self.scroll_y + self.scroll_speed)
                elif event.key == pygame.K_PAGEUP:
                    self.scroll_y = max(0, self.scroll_y - self.scroll_speed * 5)
                elif event.key == pygame.K_PAGEDOWN:
                    self.scroll_y = min(self.max_scroll, self.scroll_y + self.scroll_speed * 5)
                elif event.key == pygame.K_HOME:
                    self.scroll_y = 0
                elif event.key == pygame.K_END:
                    self.scroll_y = self.max_scroll
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    return

    def draw(self):
        """Draw the visualization dashboard"""
        # Fill background
        self.screen.fill(WHITE)

        # Draw menu area with light gray background
        pygame.draw.rect(self.screen, (240, 240, 240), self.menu_area)
        pygame.draw.line(self.screen, BLACK, (self.menu_width, 0), (self.menu_width, HEIGHT), 2)

        # Draw dashboard title
        title_text = self.title_font.render("Game Statistics Dashboard", True, BLACK)
        self.screen.blit(title_text, (self.menu_width + (WIDTH - self.menu_width - title_text.get_width())//2, 20))

        # Draw menu title
        menu_title = self.heading_font.render("Categories", True, BLACK)
        self.screen.blit(menu_title, (self.menu_width//2 - menu_title.get_width()//2, 50))

        # Draw category buttons
        for i, category in enumerate(self.categories):
            button_rect = pygame.Rect(10, 100 + i * 50, self.menu_width - 20, 40)

            # Highlight active category
            if self.active_category == category["name"]:
                button_color = COLORS["green"]
            else:
                button_color = COLORS["blue"]

            pygame.draw.rect(self.screen, button_color, button_rect)

            # Add button text
            button_text = self.menu_font.render(category["name"], True, WHITE)
            text_pos = (button_rect.centerx - button_text.get_width()//2,
                         button_rect.centery - button_text.get_height()//2)
            self.screen.blit(button_text, text_pos)

        # Create a clipping rectangle for the content area
        content_surface = pygame.Surface((self.content_area.width, self.content_area.height))
        content_surface.fill(WHITE)

        # Draw active category content onto the content surface
        if self.active_category:
            self.draw_category_content(content_surface)
        else:
            # Draw welcome message if no category selected
            if self.vis_available:
                msg_text = self.heading_font.render("Select a category from the menu", True, BLACK)
                content_surface.blit(msg_text, ((self.content_area.width - msg_text.get_width())//2,
                                          self.content_area.height//2 - msg_text.get_height()//2))
            else:
                msg_text1 = self.heading_font.render("No visualization data available", True, BLACK)
                msg_text2 = self.menu_font.render("Play more games to generate statistics", True, BLACK)

                content_surface.blit(msg_text1, ((self.content_area.width - msg_text1.get_width())//2,
                                          self.content_area.height//2 - 30))
                content_surface.blit(msg_text2, ((self.content_area.width - msg_text2.get_width())//2,
                                          self.content_area.height//2 + 10))

        # Blit the content surface to the screen
        self.screen.blit(content_surface, self.content_area)

        # Draw a border around the content area
        pygame.draw.rect(self.screen, BLACK, self.content_area, 1)

        # Draw scroll buttons if scrolling is needed
        if self.max_scroll > 0:
            # Up button (only shown if not at the top)
            if self.scroll_y > 0:
                pygame.draw.rect(self.screen, COLORS["blue"], self.scroll_up_button)
                up_text = self.menu_font.render("▲", True, WHITE)
                self.screen.blit(up_text, (self.scroll_up_button.centerx - up_text.get_width()//2,
                                        self.scroll_up_button.centery - up_text.get_height()//2))

            # Down button (only shown if not at the bottom)
            if self.scroll_y < self.max_scroll:
                pygame.draw.rect(self.screen, COLORS["blue"], self.scroll_down_button)
                down_text = self.menu_font.render("▼", True, WHITE)
                self.screen.blit(down_text, (self.scroll_down_button.centerx - down_text.get_width()//2,
                                          self.scroll_down_button.centery - down_text.get_height()//2))

            # Draw scroll bar
            scroll_bar_height = 200
            scroll_bar_width = 10
            scroll_bar_x = WIDTH - 20
            scroll_bar_y = 160

            # Draw scroll track
            pygame.draw.rect(self.screen, (200, 200, 200),
                            (scroll_bar_x, scroll_bar_y, scroll_bar_width, HEIGHT - 260))

            # Draw scroll thumb
            scroll_ratio = self.scroll_y / self.max_scroll if self.max_scroll > 0 else 0
            thumb_height = max(30, (HEIGHT - 260) * (self.content_area.height / (self.content_area.height + self.max_scroll)))
            thumb_pos = scroll_bar_y + scroll_ratio * (HEIGHT - 260 - thumb_height)

            pygame.draw.rect(self.screen, COLORS["blue"],
                            (scroll_bar_x, thumb_pos, scroll_bar_width, thumb_height))

            # Draw scroll indicators
            scroll_info = self.menu_font.render(f"Scroll to see more", True, BLACK)
            self.screen.blit(scroll_info, (self.menu_width + 20, HEIGHT - 80))

            # Keyboard shortcuts
            keys_info = self.menu_font.render("Use arrow keys, PgUp, PgDn, Home, End to scroll", True, BLACK)
            self.screen.blit(keys_info, (self.menu_width + 20, HEIGHT - 50))

        # Draw back button
        pygame.draw.rect(self.screen, COLORS["red"], self.back_button)
        back_text = self.menu_font.render("Back", True, WHITE)
        self.screen.blit(back_text, (self.back_button.centerx - back_text.get_width()//2,
                                    self.back_button.centery - back_text.get_height()//2))

    def draw_category_content(self, surface):
        """Draw the content for the active category onto the given surface"""
        # Find the selected category
        selected_category = next((cat for cat in self.categories if cat["name"] == self.active_category), None)
        if not selected_category:
            return

        # Display category title
        category_title = self.heading_font.render(selected_category["name"], True, BLACK)
        surface.blit(category_title, (20, 10 - self.scroll_y))

        # Check if there are images for this category
        if not selected_category["images"]:
            no_data_text = self.menu_font.render("No visualizations available for this category", True, BLACK)
            surface.blit(no_data_text, (40, 60 - self.scroll_y))
            return

        # Keep track of total content height to determine if scrolling is needed
        total_height = 60  # Start after the title

        # Display images for this category
        for image_name in selected_category["images"]:
            if image_name in self.images and self.images[image_name]:
                img = self.images[image_name]

                # Center image horizontally in the visualization area
                img_x = (surface.get_width() - img.get_width())//2
                img_y = total_height - self.scroll_y

                # Only draw the image if it's in the visible area
                if (img_y + img.get_height() > 0) and (img_y < surface.get_height()):
                    # Draw image
                    surface.blit(img, (img_x, img_y))

                # Draw image caption
                caption = image_name.replace(".png", "").replace("_", " ").title()
                caption_text = self.menu_font.render(caption, True, BLACK)
                caption_y = img_y + img.get_height() + 5

                # Only draw the caption if it's in the visible area
                if (caption_y + caption_text.get_height() > 0) and (caption_y < surface.get_height()):
                    surface.blit(caption_text, ((surface.get_width() - caption_text.get_width())//2, caption_y))

                # Update total height
                total_height += img.get_height() + 40  # Image height + spacing
            else:
                missing_text = self.menu_font.render(f"Image not found: {image_name}", True, COLORS["red"])
                missing_y = total_height - self.scroll_y

                # Only draw the message if it's in the visible area
                if (missing_y + missing_text.get_height() > 0) and (missing_y < surface.get_height()):
                    surface.blit(missing_text, (40, missing_y))

                total_height += 30  # Text height + spacing

        # Update max scroll value based on content height
        self.max_scroll = max(0, total_height - surface.get_height())

# Function to be called from main menu
def show_visualization_dashboard(screen):
    """Show the visualization dashboard"""
    dashboard = VisualizationDashboard(screen)
    dashboard.run()
    return  # Return to main menu when dashboard is closed