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
pygame.font.init() # Explicitly init font just in case

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
        self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_menu = pygame.font.SysFont("Arial", 36)
        
        self.menu_items = ["ARCADE", "QUIT"]
        self.selected_index = 0
        
        # Load Assets
        self.bg_image = None
        self.logo_main = None
        self.logo_esiea = None
        self.logo_inria = None
        self.logo_digital = None
        
        try:
            # Background
            bg_path = os.path.join("cryptris", "img", "bg-circuits.png")
            self.bg_image = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Logos
            self.logo_main = pygame.image.load(os.path.join("cryptris", "img", "logo-cryptris-large.png")).convert_alpha()
            self.logo_esiea = pygame.image.load(os.path.join("cryptris", "img", "logo-esiea.png")).convert_alpha()
            self.logo_inria = pygame.image.load(os.path.join("cryptris", "img", "logo-inria-medium.png")).convert_alpha()
            self.logo_digital = pygame.image.load(os.path.join("cryptris", "img", "logo-digital-cuisine-medium.png")).convert_alpha()

            # Rescale ESIEA logo if too big (e.g., max width 200)
            if self.logo_esiea.get_width() > 250:
                scale = 250 / self.logo_esiea.get_width()
                new_size = (int(self.logo_esiea.get_width() * scale), int(self.logo_esiea.get_height() * scale))
                self.logo_esiea = pygame.transform.scale(self.logo_esiea, new_size)
                
        except Exception as e:
            print(f"Error loading menu assets: {e}")

    def draw(self, screen):
        # Background
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)
            
        # 1. Main Logo (Top Center)
        if self.logo_main:
            # Position at y=100 centered
            rect = self.logo_main.get_rect(center=(SCREEN_WIDTH//2, 150))
            screen.blit(self.logo_main, rect)
        else:
            # Fallback text
            title = self.font_large.render("CRYPTRIS", True, (0, 255, 255))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

        # 2. ESIEA Logo (Top Right)
        if self.logo_esiea:
            # Padding from edges
            margin = 30
            # Position: Top Right
            x = SCREEN_WIDTH - self.logo_esiea.get_width() - margin
            y = margin
            screen.blit(self.logo_esiea, (x, y))

        # 3. Footer Logos (Bottom Center/Sides)
        if self.logo_inria and self.logo_digital:
            margin_bottom = 40
            spacing = 50
            
            # Group width
            total_w = self.logo_inria.get_width() + self.logo_digital.get_width() + spacing
            start_x = (SCREEN_WIDTH - total_w) // 2
            y = SCREEN_HEIGHT - self.logo_inria.get_height() - margin_bottom
            
            screen.blit(self.logo_digital, (start_x, y)) # Digital Cuisine first?
            screen.blit(self.logo_inria, (start_x + self.logo_digital.get_width() + spacing, y))

        # 4. Vertical Menu
        menu_start_y = 450
        item_spacing = 60
        
        for i, item in enumerate(self.menu_items):
            is_selected = (i == self.selected_index)
            
            text_str = item
            if is_selected:
                text_str = f"> {item} <"
                color = (0, 255, 255) # Cyan
            else:
                color = (0, 100, 150) # Dim Blue
                
            text = self.font_menu.render(text_str, True, color)
            
            # Center
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            y = menu_start_y + i * item_spacing
            
            # Selected Glow
            if is_selected:
                # Draw simple shadow/glow
                shadow = self.font_menu.render(text_str, True, (0, 50, 50))
                screen.blit(shadow, (x+2, y+2))
            
            screen.blit(text, (x, y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                self.trigger_menu_action()

    def trigger_menu_action(self):
        selection = self.menu_items[self.selected_index]
        if selection == "ARCADE":
             # Go to Name/Difficulty Config
             self.manager.switch_to(ConfigScene())
        elif selection == "QUIT":
            pygame.quit()
            sys.exit()

class ConfigScene(Scene):
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
        title = self.font.render("CONFIGURATION", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        # Name Input
        name_label = self.small_font.render("Enter Your Name:", True, (200, 200, 200))
        screen.blit(name_label, (SCREEN_WIDTH//2 - name_label.get_width()//2, 250))
        
        name_surface = self.font.render(self.player_name + "_", True, (0, 255, 255))
        screen.blit(name_surface, (SCREEN_WIDTH//2 - name_surface.get_width()//2, 290))

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
            elif event.key == pygame.K_ESCAPE:
                self.manager.switch_to(MenuScene())
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                # Limit name length
                if len(self.player_name) < 12 and event.unicode.isprintable():
                    self.player_name += event.unicode
        
        # Difficulty Selection (Draw method continued)
        # Because we replaced the whole class content incorrectly in previous step by omitting lines, I need to be careful with replace_file_content logic.
        # But wait, I am replacing from top of file. This is risky if I don't provide the whole chunk correctly.
        # Let's target specific blocks.

# RE-STRATEGIZING:
# I will make smaller targeted edits.


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
        self.font_large = pygame.font.SysFont("Arial", 48, bold=True)
        self.font_menu = pygame.font.SysFont("Arial", 36)
        
        self.menu_items = ["ARCADE", "QUITTER"]
        self.selected_index = 0
        
        # Load Assets
        self.bg_image = None
        self.logo_main = None
        self.logo_esiea = None
        self.logo_inria = None
        self.logo_digital = None
        
        try:
            # Background
            bg_path = os.path.join("cryptris", "img", "bg-circuits.png")
            self.bg_image = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Logos
            self.logo_main = pygame.image.load(os.path.join("cryptris", "img", "logo-cryptris-large.png")).convert_alpha()
            self.logo_esiea = pygame.image.load(os.path.join("cryptris", "img", "logo-esiea.png")).convert_alpha()
            self.logo_inria = pygame.image.load(os.path.join("cryptris", "img", "logo-inria-medium.png")).convert_alpha()
            self.logo_digital = pygame.image.load(os.path.join("cryptris", "img", "logo-digital-cuisine-medium.png")).convert_alpha()

            # Rescale ESIEA logo if too big (e.g., max width 200)
            if self.logo_esiea.get_width() > 250:
                scale = 250 / self.logo_esiea.get_width()
                new_size = (int(self.logo_esiea.get_width() * scale), int(self.logo_esiea.get_height() * scale))
                self.logo_esiea = pygame.transform.scale(self.logo_esiea, new_size)
                
        except Exception as e:
            print(f"Error loading menu assets: {e}")

    def draw(self, screen):
        # Background
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)
            
        # 1. Main Logo (Top Center)
        if self.logo_main:
            # Position at y=180 centered (Safe for 900p)
            rect = self.logo_main.get_rect(center=(SCREEN_WIDTH//2, 180))
            screen.blit(self.logo_main, rect)
        else:
            # Fallback text
            # Sized for 900p
            fallback_font = pygame.font.SysFont("Arial", 80, bold=True)
            title = fallback_font.render("CRYPTRIS", True, (0, 255, 255))
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))

        # 2. ESIEA Logo (Top Right)
        if self.logo_esiea:
            # Padding from edges
            margin = 30
            # Position: Top Right
            x = SCREEN_WIDTH - self.logo_esiea.get_width() - margin
            y = margin
            screen.blit(self.logo_esiea, (x, y))

        # 3. Footer Logos (Bottom Center/Sides)
        if self.logo_inria and self.logo_digital:
            margin_bottom = 40
            spacing = 50
            
            # Group width
            total_w = self.logo_inria.get_width() + self.logo_digital.get_width() + spacing
            start_x = (SCREEN_WIDTH - total_w) // 2
            y = SCREEN_HEIGHT - self.logo_inria.get_height() - margin_bottom
            
            screen.blit(self.logo_digital, (start_x, y)) # Digital Cuisine first?
            screen.blit(self.logo_inria, (start_x + self.logo_digital.get_width() + spacing, y))

        # 4. Vertical Menu
        menu_start_y = 450
        item_spacing = 60
        
        for i, item in enumerate(self.menu_items):
            is_selected = (i == self.selected_index)
            
            text_str = item
            if is_selected:
                text_str = f"> {item} <"
                color = (0, 255, 255) # Cyan
            else:
                color = (0, 100, 150) # Dim Blue
                
            text = self.font_menu.render(text_str, True, color)
            
            # Center
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            y = menu_start_y + i * item_spacing
            
            # Selected Glow
            if is_selected:
                # Draw simple shadow/glow
                shadow = self.font_menu.render(text_str, True, (0, 50, 50))
                screen.blit(shadow, (x+2, y+2))
            
            screen.blit(text, (x, y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                self.trigger_menu_action()

    def trigger_menu_action(self):
        selection = self.menu_items[self.selected_index]
        if selection == "ARCADE":
             # Go to Name/Difficulty Config
             self.manager.switch_to(ConfigScene())
        elif selection == "QUITTER":
            pygame.quit()
            sys.exit()

class ConfigScene(Scene):
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
        title = self.font.render("CONFIGURATION", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        # Name Input
        name_label = self.small_font.render("Entrez votre nom :", True, (200, 200, 200))
        screen.blit(name_label, (SCREEN_WIDTH//2 - name_label.get_width()//2, 250))
        
        name_surface = self.font.render(self.player_name + "_", True, (0, 255, 255))
        screen.blit(name_surface, (SCREEN_WIDTH//2 - name_surface.get_width()//2, 290))

        # Difficulty Selection
        sel_text = self.small_font.render("Selectionnez la difficulte (Colonnes) :", True, (200, 200, 200))
        screen.blit(sel_text, (SCREEN_WIDTH//2 - sel_text.get_width()//2, 400))
        
        # Draw options
        for i, length in enumerate(self.lengths):
            color = (0, 255, 0) if i == self.selected_length_index else (100, 100, 100)
            opt_text = self.font.render(str(length), True, color)
            x = SCREEN_WIDTH//2 + (i - len(self.lengths)//2) * 100 - opt_text.get_width()//2
            screen.blit(opt_text, (x, 450))

        # Instructions
        text = self.small_font.render("Tapez Nom, Fleches pour Difficulte, ENTREE pour Demarrer", True, (200, 200, 200))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 600))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_length_index = (self.selected_length_index - 1) % len(self.lengths)
            elif event.key == pygame.K_RIGHT:
                self.selected_length_index = (self.selected_length_index + 1) % len(self.lengths)
            elif event.key == pygame.K_RETURN:
                if self.player_name.strip() == "":
                    self.player_name = "Joueur"
                selected_length = self.lengths[self.selected_length_index]
                self.manager.switch_to(GameScene(selected_length, self.player_name))
            elif event.key == pygame.K_ESCAPE:
                self.manager.switch_to(MenuScene())
            elif event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                # Limit name length
                if len(self.player_name) < 12 and event.unicode.isprintable():
                    self.player_name += event.unicode

class VictoryPopup:
    def __init__(self, screen_width, screen_height, decrypted_code, on_menu, on_next):
        self.width = 600
        self.height = 300
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        self.on_menu = on_menu
        self.on_next = on_next
        self.code = decrypted_code
        
        # Couleurs
        self.bg_color = (255, 255, 255)
        self.header_color = (0, 113, 187) # Bleu du thème
        self.text_color = (50, 50, 50)
        self.btn_menu_color = (180, 0, 0)
        self.btn_next_color = (0, 113, 187)
        self.btn_hover_color = (100, 100, 100)
        
        # Polices
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.msg_font = pygame.font.SysFont("Courier New", 20, bold=True)
        self.btn_font = pygame.font.SysFont("Arial", 16, bold=True)
        
        # Boutons
        btn_w, btn_h = 200, 50
        spacing = 40
        total_btn_w = 2 * btn_w + spacing
        start_x = self.x + (self.width - total_btn_w) // 2
        btn_y = self.y + self.height - 80
        
        self.rect_menu = pygame.Rect(start_x, btn_y, btn_w, btn_h)
        self.rect_next = pygame.Rect(start_x + btn_w + spacing, btn_y, btn_w, btn_h)

    def draw(self, screen):
        # Overlay (Fond sombre)
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) 
        screen.blit(overlay, (0, 0))
        
        # Ombre de la Popup
        shadow_rect = pygame.Rect(self.x + 5, self.y + 5, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect)
        
        # Corps de la Popup
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, rect)
        
        # En-tête
        header_rect = pygame.Rect(self.x, self.y, self.width, 70)
        pygame.draw.rect(screen, self.header_color, header_rect)
        
        # Bordure
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)
        
        # Titre
        title_surf = self.title_font.render("CHALLENGE SOLVED", True, (255, 255, 255))
        screen.blit(title_surf, (self.x + 20, self.y + 15))
        
        # Contenu - Icône Cadenas (Gauche)
        lock_center_x = self.x + 100
        lock_center_y = self.y + 150
        # Dessin du cadenas (ouvert)
        pygame.draw.rect(screen, (80, 80, 80), (lock_center_x - 30, lock_center_y, 60, 45)) # Corps
        # Anse (Ouverte)
        pygame.draw.arc(screen, (80, 80, 80), (lock_center_x - 22, lock_center_y - 45, 44, 50), 3.14, 6.28, 6) # Arche
        pygame.draw.line(screen, (80, 80, 80), (lock_center_x + 22, lock_center_y - 20), (lock_center_x + 22, lock_center_y - 10), 6) # Tige
        
        # Contenu - Message (Droite)
        msg_x = self.x + 200
        msg_y = self.y + 120
        label = self.msg_font.render("DECRYPTED MESSAGE :", True, (100, 100, 100))
        screen.blit(label, (msg_x, msg_y))
        
        # Boîte de Code
        code_bg = pygame.Rect(msg_x, msg_y + 30, 300, 40)
        pygame.draw.rect(screen, (240, 240, 240), code_bg)
        code_surf = self.msg_font.render(f" {self.code} ", True, (0, 0, 0))
        screen.blit(code_surf, (msg_x + 10, msg_y + 38))
        
        # Buttons
        mx, my = pygame.mouse.get_pos()
        
        # Menu Button
        c_menu = self.btn_hover_color if self.rect_menu.collidepoint(mx, my) else self.btn_menu_color
        pygame.draw.rect(screen, c_menu, self.rect_menu)
        txt_menu = self.btn_font.render("ARCADE MENU", True, (255, 255, 255))
        screen.blit(txt_menu, (self.rect_menu.centerx - txt_menu.get_width()//2, self.rect_menu.centery - txt_menu.get_height()//2))
        
        # Next Button
        c_next = self.btn_hover_color if self.rect_next.collidepoint(mx, my) else self.btn_next_color
        pygame.draw.rect(screen, c_next, self.rect_next)
        txt_next = self.btn_font.render("NEXT CHALLENGE", True, (255, 255, 255))
        screen.blit(txt_next, (self.rect_next.centerx - txt_next.get_width()//2, self.rect_next.centery - txt_next.get_height()//2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect_menu.collidepoint(event.pos):
                    self.on_menu()
                elif self.rect_next.collidepoint(event.pos):
                    self.on_next()

class GameScene(Scene):
    def __init__(self, length=MIN_BOARD_LENGTH, player_name="Joueur"):
        super().__init__()
        self.current_length = length
        self.player_name = player_name
        self.key_info = get_key_info()
        self.victory_popup = None
        
        # Override removed to restore original difficulty


        self.target_message = self.generate_solvable_message(self.current_length)
        
        # Layout: Player Left, AI Right with Central Gap
        # Replicating original game layout:
        # - Wide central gap for controls/timer
        # - Boxes on sides
        # - Space at bottom
        
        # Layout: Player Left, AI Right with Central Gap
        center_width = 300  # Slightly reduced gap to give more space to boxes while keeping margin
        side_margin = 150   # HUGE margin to prevent left cut-off
        
        # Total width available for boxes
        available_width = SCREEN_WIDTH - center_width - 2 * side_margin
        box_width = available_width // 2
        
        # Vertical Layout
        top_margin = 120 
        bottom_margin = 80 # Leave space for numbers at bottom
        box_height = SCREEN_HEIGHT - top_margin - bottom_margin
        
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
        self.start_time = pygame.time.get_ticks() # Start Timer
        self.game_over_message = ""
        self.game_over_color = (255, 255, 255)

    def generate_solvable_message(self, length):
        # Generate a message that is a linear combination of the player's key
        # Improved logic: Ensure the "greedy strategy" (attacking the highest column) works.
        # We do this by constructing the puzzle using the "Spike" of the key.
        
        player_key_vector = self.key_info['private_key'][length]['key']
        
        # Find the "Spike" (Max absolute value index) in the key
        # This allows us to align the generator's moves with the player's optimal moves
        spike_val = max(player_key_vector, key=abs)
        spike_index = player_key_vector.index(spike_val)
        
        # Start with zero vector
        message_vector = [0] * length
        
        # Balanced: Increase steps for higher levels to create "tall" boards
        # Level 16 needs many steps because the key is "simple" (mostly zeros)
        # So we need to stack it many times to fill the board.
        if length <= 10:
            steps = 4 
        elif length <= 12:
            steps = 6
        elif length <= 14:
            steps = 10
        else: # 16
            steps = 15 # Much denser board for level 16
        
        for _ in range(steps):
            # Pick a random target column to raise
            target_col = random.randint(0, length - 1)
            
            # Calculate rotation needed to bring the Spike to the Target Column
            # rotate(l, k) shift left by k. new = (old - k) % mod
            # target = (spike - k) % mod  =>  k = (spike - target) % mod
            rot = (spike_index - target_col) % length
            
            rotated_key = rotate(length, player_key_vector, rot)
            
            # Pick a random direction
            direction = 1 if random.random() > 0.5 else -1
            
            # Add to message
            weighted_key = mult_vector(direction, rotated_key)
            message_vector = sum_vectors(message_vector, weighted_key)
            
        return create_a_data_message(message_vector, length)

    def on_enter(self):
        # Pass screen to boxes if needed, but we can pass it in draw
        pass

    def handle_event(self, event):
        if self.victory_popup:
            self.victory_popup.handle_event(event) # Delegate to popup
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_to(MenuScene())
            elif not self.game_over:
                self.player_box.handle_input(event)

    def update(self, current_time):
        if self.game_over:
            # Continue updating visuals (effects) but stop logic that affects game state if needed
            self.player_box.update()
            self.ai_box.update()
            
            # Stop AI
            # self.ai.update(current_time) 
            
            # Check for auto-exit ONLY if lost (no popup)
            # If Win, we wait for user interaction via popup
            if self.victory_popup is None and self.game_over_message == "ECHEC...":
                 if current_time - self.game_over_timer > 5000:
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
            
            # Trigger Popup
            if self.victory_popup is None:
                # Generate random hex code or use level info
                code = f"{random.randint(10,99)} A{random.randint(1,9)} F{random.randint(1,9)}"
                self.victory_popup = VictoryPopup(SCREEN_WIDTH, SCREEN_HEIGHT, code, self.go_to_menu, self.go_to_next)

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
        title_font = pygame.font.SysFont("Arial", 60, bold=True)
        title = title_font.render("CRYPTRIS", True, (0, 255, 255)) # Cyan glow
        # Add a glow effect (simple shadow)
        title_shadow = title_font.render("CRYPTRIS", True, (0, 100, 100))
        # Center title horizontally, place it comfortably at y=50
        screen.blit(title_shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 3, 43))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 40))

        # --- TIMER ---
        if not self.game_over:
            elapsed_ms = pygame.time.get_ticks() - self.start_time
        else:
            elapsed_ms = self.game_over_timer - self.start_time

        total_seconds = elapsed_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_font = pygame.font.SysFont("Arial", 60, bold=True) # Larger font for 1080p
        
        # Glow effect for timer
        timer_surf_shadow = timer_font.render(timer_text, True, (0, 100, 0))
        timer_surf = timer_font.render(timer_text, True, (0, 255, 0)) # Green

        # Position: Absolute Center of the screen (in the gap)
        # Vertical center of the screen is SCREEN_HEIGHT // 2 = 540
        # Check box vertical center: (top=150, bottom=100 from bottom => 980) -> mid = 565
        timer_rect = timer_surf.get_rect(center=(SCREEN_WIDTH//2, 470))
        
        screen.blit(timer_surf_shadow, (timer_rect.x + 3, timer_rect.y + 3))
        screen.blit(timer_surf, timer_rect)
        # -------------

        # Draw Player Name Box
        self.draw_name_box(screen, self.player_name, self.player_box.rect.centerx, 80, is_player=True)

        # Draw AI Name Box
        self.draw_name_box(screen, "LOGICIEL ESPION", self.ai_box.rect.centerx, 80, is_player=False)

        # We need to manually inject screen into boxes if they store it
        self.player_box.screen = screen
        self.ai_box.screen = screen
        
        self.player_box.draw()
        self.ai_box.draw()

        # Draw Popup LAST to ensure it is on top
        if self.victory_popup:
            self.victory_popup.draw(screen)

    def go_to_menu(self):
        self.manager.switch_to(MenuScene())

    def go_to_next(self):
        from settings import AUTHORIZED_LENGTH
        try:
            current_idx = AUTHORIZED_LENGTH.index(self.current_length)
            if current_idx < len(AUTHORIZED_LENGTH) - 1:
                next_len = AUTHORIZED_LENGTH[current_idx + 1]
                self.manager.switch_to(GameScene(next_len, self.player_name))
            else:
                self.manager.switch_to(MenuScene()) # Finished all
        except ValueError:
            self.manager.switch_to(MenuScene())

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

        # Decorative dots like in the screenshot
        pygame.draw.circle(screen, border_color, (rect.left - 10, rect.centery), 4)
        pygame.draw.circle(screen, border_color, (rect.right + 10, rect.centery), 4)

        if self.game_over and not self.victory_popup:
            # Check delay for overlay
            current_ticks = pygame.time.get_ticks()
            if current_ticks - self.game_over_timer > 1000: # 1 second delay
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
