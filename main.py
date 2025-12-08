import pygame
import sys
import os
import random
from settings import APP_URL, AUTHORIZED_LENGTH, MIN_BOARD_LENGTH, PLAYER_BOARD_COLORS, IA_BOARD_COLORS
from game_box import GameBox
from cryptris_logic import get_key_info, create_a_data_message, gen_public_key, score, PREGENERATED_PRIVATE_KEYS, REPEAT_GEN_PUBLIC_KEY_LIST, rotate, mult_vector, sum_vectors
from ai import AI

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FPS = 60
BACKGROUND_COLOR = (20, 20, 20)

class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_scene = None

    def switch_to(self, scene):
        self.current_scene = scene
        self.current_scene.manager = self
        self.current_scene.on_enter()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.current_scene.handle_event(event)
            
            self.current_scene.update(pygame.time.get_ticks())
            self.current_scene.draw(self.screen)
            
            pygame.display.flip()

class Scene:
    def __init__(self):
        self.manager = None

    def on_enter(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, current_time):
        pass

    def draw(self, screen):
        pass

class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 48)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.selected_length_index = 0
        self.lengths = AUTHORIZED_LENGTH
        self.player_name = ""
        
        # Load background
        try:
            bg_path = os.path.join("cryptris", "img", "bg-circuits.png")
            self.bg_image = pygame.image.load(bg_path).convert()
            # Scale background to new resolution
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.bg_image = None

    def draw(self, screen):
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)
        
        # Title
        title = self.font.render("CRYPTRIS", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        # Name Input
        name_label = self.small_font.render("Enter Your Name:", True, (200, 200, 200))
        screen.blit(name_label, (SCREEN_WIDTH//2 - name_label.get_width()//2, 250))
        
        name_surface = self.font.render(self.player_name + "_", True, (0, 255, 255))
        screen.blit(name_surface, (SCREEN_WIDTH//2 - name_surface.get_width()//2, 290))

        # Difficulty Selection
        sel_text = self.small_font.render("Select Difficulty (Columns):", True, (200, 200, 200))
        screen.blit(sel_text, (SCREEN_WIDTH//2 - sel_text.get_width()//2, 400))
        
        # Draw options
        for i, length in enumerate(self.lengths):
            color = (0, 255, 0) if i == self.selected_length_index else (100, 100, 100)
            opt_text = self.font.render(str(length), True, color)
            x = SCREEN_WIDTH//2 + (i - len(self.lengths)//2) * 100 - opt_text.get_width()//2
            screen.blit(opt_text, (x, 450))

        # Instructions
        text = self.small_font.render("Type Name, Use Arrows for Difficulty, ENTER to Start", True, (200, 200, 200))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 600))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_length_index = (self.selected_length_index - 1) % len(self.lengths)
            elif event.key == pygame.K_RIGHT:
                self.selected_length_index = (self.selected_length_index + 1) % len(self.lengths)
            elif event.key == pygame.K_RETURN:
                if self.player_name.strip() == "":
                    self.player_name = "Player"
                selected_length = self.lengths[self.selected_length_index]
                self.manager.switch_to(GameScene(selected_length, self.player_name))
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                # Limit name length
                if len(self.player_name) < 12 and event.unicode.isprintable():
                    self.player_name += event.unicode

class GameScene(Scene):
    def __init__(self, length=MIN_BOARD_LENGTH, player_name="Player"):
        super().__init__()
        self.current_length = length
        self.player_name = player_name
        self.key_info = get_key_info()
        
        # Override removed to restore original difficulty


        self.target_message = self.generate_solvable_message(self.current_length)
        
        # Layout: Player Left, AI Right with Central Gap
        # Calculate required width for the columns
        
        # Total width available
        center_width = 300
        side_margin = 50
        available_width = SCREEN_WIDTH - center_width - 2 * side_margin
        box_width = available_width // 2
        
        # Move boxes down to make room for headers
        top_margin = 150 
        box_height = SCREEN_HEIGHT - top_margin - 50
        
        self.player_box = GameBox(
            None, # Screen passed in draw
            x=side_margin, 
            y=top_margin, 
            width=box_width, 
            height=box_height,
            current_length=self.current_length,
            key_info=self.key_info,
            my_message=self.target_message,
            player=True
        )
        
        self.ai_box = GameBox(
            None,
            x=side_margin + box_width + center_width,
            y=top_margin,
            width=box_width,
            height=box_height,
            current_length=self.current_length,
            key_info=self.key_info,
            my_message=self.target_message, 
            player=False
        )
        
        self.ai = AI(self.ai_box, {'waitingIATime': 1000, 'keyFirstMoveTime': 500})
        self.ai.start()
        
        self.game_over = False
        self.game_over_timer = 0
        self.game_over_message = ""
        self.game_over_color = (255, 255, 255)

    def generate_solvable_message(self, length):
        # Generate a message that is a linear combination of the player's key
        # This ensures it is solvable.
        
        player_key_vector = self.key_info['public_key'][length]['key']
        
        # Start with zero vector
        message_vector = [0] * length
        
        # Number of steps (complexity)
        # For easy (8), use fewer steps. For hard (16), use more.
        # Original: steps = length // 2 + 2
        # New: Much easier for small lengths
        if length <= 8:
            steps = 3 # Minimum 3 moves to win
        elif length <= 10:
            steps = 2
        elif length <= 12:
            steps = 3
        else:
            steps = length // 3 + 2
        
        for _ in range(steps):
            # Pick a random rotation
            rot = random.randint(0, length - 1)
            rotated_key = rotate(length, player_key_vector, rot)
            
            # Pick a random direction (add or subtract)
            direction = 1 if random.random() > 0.5 else -1
            
            # Add to message
            weighted_key = mult_vector(direction, rotated_key)
            message_vector = sum_vectors(message_vector, weighted_key)
            
        return create_a_data_message(message_vector, length)

    def on_enter(self):
        # Pass screen to boxes if needed, but we can pass it in draw
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_to(MenuScene())
            elif not self.game_over:
                self.player_box.handle_input(event)

    def update(self, current_time):
        if self.game_over:
            if current_time - self.game_over_timer > 3000: # Wait 3 seconds
                self.manager.switch_to(MenuScene())
            return

        self.player_box.update()
        self.ai_box.update()
        self.ai.update(current_time)
        
        # Check Win/Loss
        status = self.player_box.check_status()
        if status == "WIN":
            self.game_over = True
            self.game_over_timer = current_time
            self.game_over_message = "VICTOIRE !"
            self.game_over_color = (0, 255, 0)
        elif status == "LOSS":
            self.game_over = True
            self.game_over_timer = current_time
            self.game_over_message = "ECHEC..."
            self.game_over_color = (255, 0, 0)
            
        # Check AI Status
        ai_status = self.ai_box.check_status()
        if ai_status == "WIN":
            self.game_over = True
            self.game_over_timer = current_time
            self.game_over_message = "ECHEC..."
            self.game_over_color = (255, 0, 0)

    def draw(self, screen):
        # Draw shared background
        if self.player_box.bg_image:
             # Scale background to screen
             bg_rect = self.player_box.bg_image.get_rect(center=screen.get_rect().center)
             # Ensure it covers the whole screen
             screen.blit(pygame.transform.scale(self.player_box.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        else:
            screen.fill(BACKGROUND_COLOR)

        # Draw Title
        # Draw Title
        title_font = pygame.font.SysFont("Arial", 48, bold=True)
        title = title_font.render("CRYPTRIS", True, (0, 255, 255)) # Cyan glow
        # Add a glow effect (simple shadow)
        title_shadow = title_font.render("CRYPTRIS", True, (0, 100, 100))
        screen.blit(title_shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 2, 32))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))

        # Draw Player Name Box
        self.draw_name_box(screen, self.player_name, self.player_box.rect.centerx, 80, is_player=True)

        # Draw AI Name Box
        self.draw_name_box(screen, "LOGICIEL ESPION", self.ai_box.rect.centerx, 80, is_player=False)

        # We need to manually inject screen into boxes if they store it
        self.player_box.screen = screen
        self.ai_box.screen = screen
        
        self.player_box.draw()
        self.ai_box.draw()

    def draw_name_box(self, screen, name, center_x, y, is_player):
        font = pygame.font.SysFont("Arial", 24, bold=True)
        text = font.render(name, True, (255, 255, 255))
        
        padding_x = 40
        padding_y = 10
        box_width = max(200, text.get_width() + 2 * padding_x)
        box_height = text.get_height() + 2 * padding_y
        
        rect = pygame.Rect(0, 0, box_width, box_height)
        rect.centerx = center_x
        rect.centery = y
        
        # Draw Box Background (Dark with border)
        pygame.draw.rect(screen, (10, 10, 10), rect)
        
        # Border Color
        border_color = (0, 255, 255) if is_player else (255, 0, 255) # Cyan vs Magenta
        pygame.draw.rect(screen, border_color, rect, 2)
        
        # Draw Text
        screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))
        
        # Decorative dots like in the screenshot
        pygame.draw.circle(screen, border_color, (rect.left - 10, rect.centery), 4)
        pygame.draw.circle(screen, border_color, (rect.right + 10, rect.centery), 4)

        if self.game_over:
            # Draw overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # Draw Message
            msg_font = pygame.font.SysFont("Arial", 96, bold=True)
            msg_surf = msg_font.render(self.game_over_message, True, self.game_over_color)
            screen.blit(msg_surf, (SCREEN_WIDTH//2 - msg_surf.get_width()//2, SCREEN_HEIGHT//2 - msg_surf.get_height()//2))

if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cryptris")
    
    manager = SceneManager(screen)
    manager.switch_to(MenuScene())
    manager.run()
