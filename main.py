import pygame
import sys
import os
import random
from settings import APP_URL, AUTHORIZED_LENGTH, MIN_BOARD_LENGTH, PLAYER_BOARD_COLORS, IA_BOARD_COLORS, COLUMN_TYPE_1, COLUMN_TYPE_2, COLUMN_TYPE_3, REPEAT_GEN_PUBLIC_KEY_LIST
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
        
        self.menu_items = ["ARCADE", "DOCUMENTATION", "A PROPOS", "QUITTER"]
        self.selected_index = 0
        self.menu_rects = [] # Initialize here to prevent AttributeError in handle_event
        
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
        
        self.menu_rects = [] # Store rects for mouse interaction
        
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
            
            
            # Store rect for collision
            item_rect = text.get_rect(topleft=(x, y))
            self.menu_rects.append((item_rect, i))

            screen.blit(text, (x, y))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                self.trigger_menu_action()
        
        # Mouse support
        elif event.type == pygame.MOUSEMOTION:
            for rect, index in self.menu_rects:
                if rect.collidepoint(event.pos):
                    self.selected_index = index
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for rect, index in self.menu_rects:
                    if rect.collidepoint(event.pos):
                        self.selected_index = index
                        self.trigger_menu_action()

    def trigger_menu_action(self):
        selection = self.menu_items[self.selected_index]
        if selection == "ARCADE":
             # Go to Name/Difficulty Config
             self.manager.switch_to(ConfigScene())
        elif selection == "DOCUMENTATION":
             self.manager.switch_to(DocumentationScene())
        elif selection == "A PROPOS":
             self.manager.switch_to(AboutScene())
        elif selection == "QUIT" or selection == "QUITTER":
            pygame.quit()
            sys.exit()

import webbrowser

class DocumentationScene(Scene):
    def __init__(self):
        super().__init__()
        self.font_title = pygame.font.SysFont("Arial", 26, bold=True) # Increased from 20
        self.font_desc = pygame.font.SysFont("Arial", 18) # Increased from 14
        self.font_url = pygame.font.SysFont("Arial", 16) # Increased from 12 (now readable)
        
        self.resources = [
            {
                "title": "PGP: AN EMAIL ENCRYPTION SOFTWARE",
                "desc": "Why and how to use openPGP?",
                "url": "https://theprivacyguide.org/tutorials/pgp.html"
            },
            {
                "title": "SIGNAL",
                "desc": "An encrypted chat application",
                "url": "https://signal.org/"
            },
            {
                "title": "PUBLIC-KEY CRYPTOGRAPHY (PKC)",
                "desc": "Definition and explanation of Public-key Cryptography on Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Public-key_cryptography"
            },
            {
                "title": "PUBLIC KEY INFRASTRUCTURE",
                "desc": "Definition of Public-key infrastructure on Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Public_key_infrastructure"
            },
            {
                "title": "CRYPTOGRAPHY",
                "desc": "Definition of Cryptography on Wikipedia",
                "url": "https://en.wikipedia.org/wiki/Cryptography"
            },
            {
                "title": "HISTOIRE DE LA CRYPTOGRAPHIE",
                "desc": "L'histoire de la cryptographie sur Wikipédia",
                "url": "https://fr.wikipedia.org/wiki/Histoire_de_la_cryptographie"
            }
        ]
        
        self.click_rects = [] # Store rects for click detection
        self.bg_image = None
        
        # Try loading background
        try:
             bg_path = os.path.join("cryptris", "img", "bg-circuits.png")
             self.bg_image = pygame.image.load(bg_path).convert()
             self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            pass

    def draw(self, screen):
         # Background
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)
            
        # Main Title
        main_title = pygame.font.SysFont("Arial", 54, bold=True).render("CRYPTRIS", True, (0, 255, 255))
        title_rect = main_title.get_rect(center=(SCREEN_WIDTH//2, 50)) # Moved up from 60
        
        # Shadow
        shadow = pygame.font.SysFont("Arial", 54, bold=True).render("CRYPTRIS", True, (0, 100, 100))
        screen.blit(shadow, (title_rect.x+3, title_rect.y+3))
        screen.blit(main_title, title_rect)
        
        sub_title = pygame.font.SysFont("Arial", 24).render("RESSOURCES EXTERNES", True, (0, 180, 200))
        screen.blit(sub_title, (SCREEN_WIDTH//2 - sub_title.get_width()//2, 90)) # Moved up from 110

        # Draw List
        start_y = 125 # Adjusted slightly to ensure clearance
        item_height = 125 # Adjusted spacing
        
        # Need to re-init click rects list on each draw if layout changes, or just once. 
        # Doing it here handles resize naturally if we supported it.
        self.click_rects = [] 
        
        for i, res in enumerate(self.resources):
            y = start_y + i * item_height
            
            # Container Rect (for click detection)
            container_w = 800 # Wider container
            container_h = 115 # Compact container height
            container_x = (SCREEN_WIDTH - container_w) // 2
            
            # Store rect
            rect = pygame.Rect(container_x, y, container_w, container_h)
            self.click_rects.append((rect, res["url"]))
            
            # Draw Container Background (faint)
            s = pygame.Surface((container_w, container_h), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 20, 40, 150), s.get_rect(), border_radius=5)
            screen.blit(s, rect)
            
            # Border (Cyan thin) for the main container
            pygame.draw.rect(screen, (0, 100, 150), rect, 1, border_radius=5)
            
            # 1. Title (Boxed style from screenshot)
            title_surf = self.font_title.render(res["title"], True, (0, 255, 255))
            
            # Title Box logic
            title_padding_x = 20
            title_padding_y = 5
            title_box_w = title_surf.get_width() + title_padding_x * 2
            title_box_h = title_surf.get_height() + title_padding_y * 2
            
            title_box_rect = pygame.Rect(0, 0, title_box_w, title_box_h)
            title_box_rect.centerx = rect.centerx
            title_box_rect.top = rect.top + 15
            
            # Draw Title Box Background (Darker opacity)
            # s_title = pygame.Surface((title_box_w, title_box_h), pygame.SRCALPHA)
            # pygame.draw.rect(s_title, (0, 0, 0, 200), s_title.get_rect())
            # screen.blit(s_title, title_box_rect)
            
            # Draw Title Box Border (Cyan)
            pygame.draw.rect(screen, (0, 200, 255), title_box_rect, 2)
            
            # Draw Title Text centered in its box
            title_text_rect = title_surf.get_rect(center=title_box_rect.center)
            screen.blit(title_surf, title_text_rect)
            
            # 2. Desc
            desc_surf = self.font_desc.render(res["desc"], True, (220, 220, 220)) # Brighter white
            screen.blit(desc_surf, (rect.centerx - desc_surf.get_width()//2, title_box_rect.bottom + 10))
            
            # 3. URL
            url_surf = self.font_url.render(res["url"], True, (0, 255, 255)) # Cyan link
            screen.blit(url_surf, (rect.centerx - url_surf.get_width()//2, title_box_rect.bottom + 35))

        # Back Instruction
        # Back Button
        mx, my = pygame.mouse.get_pos()
        self.back_rect = pygame.Rect(20, 20, 120, 40)
        
        is_hover = self.back_rect.collidepoint(mx, my)
        color_bg = (0, 50, 50) if is_hover else (0, 20, 20)
        color_border = (0, 255, 255) if is_hover else (0, 100, 100)
        
        pygame.draw.rect(screen, color_bg, self.back_rect, border_radius=5)
        pygame.draw.rect(screen, color_border, self.back_rect, 2, border_radius=5)
        
        text_surf = self.font_desc.render("RETOUR", True, (0, 255, 255))
        text_rect = text_surf.get_rect(center=self.back_rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_to(MenuScene())
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left Click
                mouse_pos = event.pos
                for rect, url in self.click_rects:
                    if rect.collidepoint(mouse_pos):
                        try:
                            webbrowser.open(url)
                        except:
                            print(f"Could not open {url}")

            # Check Back Button
            if hasattr(self, 'back_rect') and self.back_rect.collidepoint(event.pos):
                self.manager.switch_to(MenuScene())

class AboutScene(Scene):
    def __init__(self):
        super().__init__()
        self.font_title = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 20)
        self.font_bold = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)
        
        self.bg_image = None
        self.logo_inria = None
        self.logo_digital = None
        self.logo_capmaths = None # Assuming we might want this if available, otherwise text
        
        try:
             # Reuse background
             bg_path = os.path.join("cryptris", "img", "bg-circuits.png")
             self.bg_image = pygame.image.load(bg_path).convert()
             self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
             
             # Reuse Logos
             self.logo_inria = pygame.image.load(os.path.join("cryptris", "img", "logo-inria-medium.png")).convert_alpha()
             self.logo_digital = pygame.image.load(os.path.join("cryptris", "img", "logo-digital-cuisine-medium.png")).convert_alpha()
        except:
            pass

    def draw(self, screen):
         # Background
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill(BACKGROUND_COLOR)
            
        # 1. Big Title "CRYPTRIS" (Reused code for consistency)
        main_title = pygame.font.SysFont("Arial", 80, bold=True).render("CRYPTRIS", True, (0, 255, 255))
        title_rect = main_title.get_rect(center=(SCREEN_WIDTH//2, 100))
        
        # Shadow/Glitch effect
        shadow = pygame.font.SysFont("Arial", 80, bold=True).render("CRYPTRIS", True, (200, 200, 200))
        screen.blit(shadow, (title_rect.x+4, title_rect.y+4))
        screen.blit(main_title, title_rect)
        
        # 2. Text Content
        # We will render line by line manually for key highlights
        start_y = 220 # Moved up slightly
        spacing = 40
        
        # Helper to draw centered text with colored keywords
        def draw_centered_text(y, parts):
            total_w = sum(font.render(text, True, color).get_width() for text, color, font in parts)
            curr_x = (SCREEN_WIDTH - total_w) // 2
            
            for text, color, font in parts:
                surf = font.render(text, True, color)
                screen.blit(surf, (curr_x, y))
                curr_x += surf.get_width()
        
        # Line 0: Author Credit
        draw_centered_text(start_y, [
            ("Cette version est une réécriture complète en ", (200, 200, 200), self.font_text),
            ("Python", (0, 255, 255), self.font_bold),
            (" réalisée par ", (200, 200, 200), self.font_text)
        ])
        draw_centered_text(start_y + 30, [
             ("Théo Ammour", (0, 255, 255), self.font_bold),
             (" pour le projet de ", (200, 200, 200), self.font_text),
             ("Cryptographie Appliquée", (0, 255, 255), self.font_bold),
             (" à l'", (200, 200, 200), self.font_text),
             ("ESIEA", (0, 255, 255), self.font_bold),
             (".", (200, 200, 200), self.font_text)
        ])

        # Line 1: Inspiration
        y_p1 = start_y + 80
        draw_centered_text(y_p1, [
            ("Elle s'inspire du jeu original Cryptris créé par ", (200, 200, 200), self.font_text),
            ("Inria", (0, 255, 255), self.font_bold),
            (" et ", (200, 200, 200), self.font_text),
            ("Digital Cuisine", (0, 255, 255), self.font_bold),
            (",", (200, 200, 200), self.font_text)
        ])
        
        draw_centered_text(y_p1 + 30, [
            ("avec le soutien de ", (200, 200, 200), self.font_text),
            ("Cap'Maths", (0, 255, 255), self.font_bold),
            (".", (200, 200, 200), self.font_text)
        ])
        
        # Paragraph 2
        y_p2 = y_p1 + 80
        draw_centered_text(y_p2, [
            ("L'objectif est d'illustrer la différence fondamentale entre clé publique et clé privée.", (220, 220, 220), self.font_text)
        ])
        draw_centered_text(y_p2 + 30, [
            ("Le joueur doit construire sa propre clé secrète pour décrypter les messages,", (220, 220, 220), self.font_text)
        ])
        draw_centered_text(y_p2 + 60, [
            ("tout en affrontant une IA qui tente de casser le code par force brute.", (220, 220, 220), self.font_text)
        ])
        
        # Paragraph 3
        y_p3 = y_p2 + 130
        draw_centered_text(y_p3, [
            ("Au fur et à mesure, votre clé se renforce. Bien qu'elle reste simple à manipuler", (220, 220, 220), self.font_text)
        ])
        draw_centered_text(y_p3 + 30, [
            ("pour vous, elle devient un véritable obstacle pour l'ordinateur.", (220, 220, 220), self.font_text)
        ])
        draw_centered_text(y_p3 + 60, [
             ("C'est là toute la puissance de la sécurité asymétrique !", (220, 220, 220), self.font_text)
        ])
        
        # Logos Footer
        footer_y = SCREEN_HEIGHT - 150
        spacing_logos = 60
        
        if self.logo_inria and self.logo_digital:
            w_inria = self.logo_inria.get_width()
            w_digital = self.logo_digital.get_width()
            total_w = w_inria + spacing_logos + w_digital
            
            start_x = (SCREEN_WIDTH - total_w) // 2
            
            screen.blit(self.logo_inria, (start_x, footer_y))
            screen.blit(self.logo_digital, (start_x + w_inria + spacing_logos, footer_y))
            
        # Back Instruction
        # Back Button
        mx, my = pygame.mouse.get_pos()
        self.back_rect = pygame.Rect(20, 20, 100, 35) # Slightly smaller/different
        
        is_hover = self.back_rect.collidepoint(mx, my)
        color_bg = (0, 50, 50) if is_hover else (0, 20, 20)
        color_border = (0, 255, 255) if is_hover else (0, 100, 100)
        
        pygame.draw.rect(screen, color_bg, self.back_rect, border_radius=5)
        pygame.draw.rect(screen, color_border, self.back_rect, 2, border_radius=5)
        
        text_surf = self.font_small.render("RETOUR", True, (0, 255, 255))
        text_rect = text_surf.get_rect(center=self.back_rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_to(MenuScene())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                 if hasattr(self, 'back_rect') and self.back_rect.collidepoint(event.pos):
                     self.manager.switch_to(MenuScene())

class KeyCreationScene(Scene):
    def __init__(self, player_name="Player"):
        super().__init__()
        self.player_name = player_name
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.length = 8
        self.key_vector = [0] * self.length # This will now represent the ACCUMULATED key (on board)
        self.selected_col = 0
        
        # Define areas
        self.grid_width = 800
        self.grid_height = 600
        self.grid_x = (SCREEN_WIDTH // 2) - (self.grid_width // 2) - 150 # Shift left
        self.grid_y = (SCREEN_HEIGHT - self.grid_height) // 2 + 50
        
        # Dummy data for GameBox
        dummy_key_info = get_key_info()
        
        # Initialiser avec une "Clé Joueur" (falling piece) VIDE pour l'instant
        # On va injecter des blocs un par un via spawn_new_block()
        dummy_key_info['private_key'][self.length] = {
            'key': [0] * self.length,
            'normal_key': [COLUMN_TYPE_3] * self.length,
            'reverse_key': [COLUMN_TYPE_3] * self.length,
            'number': [0] * self.length
        }
        
        # Le "Message" sera notre tableau vide qui se remplit (la clé en construction)
        dummy_message = create_a_data_message([0]*self.length, self.length)
        
        self.game_box = GameBox(
            None,
            self.grid_x,
            self.grid_y,
            self.grid_width,
            self.grid_height,
            self.length,
            dummy_key_info,
            dummy_message,
            player=True
        )
        
        self.timer_start = pygame.time.get_ticks()
        self.was_falling = False
        
        # Spawn first block
        self.spawn_new_block()

    def spawn_new_block(self):
        # Créer un bloc ou une pile de blocs (hauteur 1-3) à une position aléatoire
        # Pour simuler un bloc qui tombe, on met à jour la "Clé Privée" (falling key) du GameBox
        
        new_key_vector = [0] * self.length
        
        # Décider combien de colonnes sont actives (1, 2 ou 3)
        # Augmentation de la fréquence des colonnes multiples selon la demande
        num_cols = random.choices([1, 2, 3], weights=[0.2, 0.5, 0.3])[0]
        
        # Choisir des colonnes aléatoires
        indices = random.sample(range(self.length), num_cols)
        
        for idx in indices:
            # Hauteur aléatoire entre 1 et 3
            height = random.randint(1, 3)
            new_key_vector[idx] = height

        # Mettre à jour les données de la GameBox
        key_cols = self.game_box.key_columns
        
        for i in range(self.length):
            val = new_key_vector[i]
            col = key_cols[i]
            col.value = val
            col.reset() # Remettre en haut
            
            if val > 0:
                col.type = COLUMN_TYPE_1 # Bleu
            else:
                col.type = COLUMN_TYPE_3 # Vide
                
        # On réinitialise l'état chute
        self.was_falling = False

    def update(self, current_time):
        self.game_box.update()
        
        # Détection de fin de chute
        is_falling = any(col.is_falling for col in self.game_box.key_columns)
        
        if self.was_falling and not is_falling:
            # Vient de finir de tomber
            # On spawn le prochain bloc
            self.spawn_new_block()
            
        self.was_falling = is_falling
        
        # Mettre à jour notre key_vector interne basé sur le plateau (message_columns)
        # pour le passage à la scène suivante
        for i, col in enumerate(self.game_box.message_columns):
            val = col.value
            if col.type == COLUMN_TYPE_2: # Négatif/Foncé
                val *= -1
            elif col.type == COLUMN_TYPE_3: # Vide
                val = 0
            self.key_vector[i] = val

    def get_strength_info(self):
        try:
            rep = REPEAT_GEN_PUBLIC_KEY_LIST.get(self.length, 10)
        except:
            rep = 10
            
        pk = gen_public_key(self.length, self.key_vector, rep)
        s = score(pk)
        
        if s < 0.5:
            label = "FAIBLE"
            color = (255, 50, 50)
            level_pct = min(1.0, s / 0.5) * 0.33
        elif s < 1.5:
            label = "MOYEN"
            color = (255, 255, 0)
            level_pct = 0.33 + min(1.0, (s - 0.5) / 1.0) * 0.33
        else:
            label = "FORT"
            color = (0, 255, 0)
            level_pct = 0.66 + min(1.0, (s - 1.5) / 1.0) * 0.34
            
        return label, color, min(1.0, max(0.05, level_pct))

    def draw(self, screen):
        # Draw Background
        if self.game_box.bg_image:
             bg_rect = self.game_box.bg_image.get_rect(center=screen.get_rect().center)
             screen.blit(pygame.transform.scale(self.game_box.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        else:
            screen.fill(BACKGROUND_COLOR)
            
        # Draw Title
        title_font = pygame.font.SysFont("Arial", 40, bold=True)
        title = title_font.render("CREATION DE CLE PRIVEE", True, (0, 255, 255))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))

        # --- Draw GameBox (Grid) ---
        self.game_box.screen = screen
        self.game_box.draw()
        
        # --- Side Panel (Right) ---
        panel_x = self.grid_x + self.grid_width + 50
        panel_y = self.grid_y
        
        # 1. Player Info & Timer
        lbl_player = self.font.render(f"Joueur : {self.player_name}", True, (255, 255, 255))
        screen.blit(lbl_player, (panel_x, panel_y))
        
        elapsed = (pygame.time.get_ticks() - self.timer_start) // 1000
        m, s = divmod(elapsed, 60)
        lbl_timer = self.font.render(f"Temps : {m:02}:{s:02}", True, (0, 255, 0))
        screen.blit(lbl_timer, (panel_x, panel_y + 40))
        
        # 2. Security Level Visual
        str_lbl, str_color, str_pct = self.get_strength_info()
        
        sec_y = panel_y + 120
        lbl_sec = self.font.render("NIVEAU DE SECURITE", True, (0, 200, 255))
        screen.blit(lbl_sec, (panel_x, sec_y))
        
        # Bar
        bar_w = 200
        bar_h = 30
        pygame.draw.rect(screen, (50, 50, 50), (panel_x, sec_y + 40, bar_w, bar_h))
        pygame.draw.rect(screen, str_color, (panel_x, sec_y + 40, int(bar_w * str_pct), bar_h))
        pygame.draw.rect(screen, (200, 200, 200), (panel_x, sec_y + 40, bar_w, bar_h), 2)
        
        lbl_str = self.font.render(str_lbl, True, str_color)
        screen.blit(lbl_str, (panel_x + bar_w + 20, sec_y + 40))
        
        # 3. Controls / Instructions
        ctrl_y = sec_y + 150
        ctrl_text_y = ctrl_y + 80
        lines = [
            "GAUCHE/DROITE : Bouger",
            "ESPACE : Inverser Couleur",
            "BAS : Lâcher"
        ]
        for i, line in enumerate(lines):
            t = self.small_font.render(line, True, (180, 180, 180))
            screen.blit(t, (panel_x, ctrl_text_y + i * 25))
            
        # Validate Button
        btn_y = ctrl_text_y + len(lines) * 25 + 20
        self.btn_validate_rect = pygame.Rect(panel_x, btn_y, 200, 50)
        
        mx, my = pygame.mouse.get_pos()
        is_hover = self.btn_validate_rect.collidepoint(mx, my)
        
        # Button Colors
        c_bg = (0, 100, 0) if is_hover else (0, 50, 0)
        c_border = (0, 255, 0) if is_hover else (0, 150, 0)
        
        pygame.draw.rect(screen, c_bg, self.btn_validate_rect, border_radius=8)
        pygame.draw.rect(screen, c_border, self.btn_validate_rect, 2, border_radius=8)
        
        v_text = self.font.render("VALIDER", True, (255, 255, 255))
        v_rect = v_text.get_rect(center=self.btn_validate_rect.center)
        screen.blit(v_text, v_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Validate Key
                self.manager.switch_to(GameScene(self.length, player_name=self.player_name, custom_key=self.key_vector))
            elif event.key == pygame.K_ESCAPE:
                self.manager.switch_to(ConfigScene())
            else:
                # Delegate controls to GameBox (Left, Right, Down, Space)
                self.game_box.handle_input(event)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check Validate button
                 if hasattr(self, 'btn_validate_rect') and self.btn_validate_rect.collidepoint(event.pos):
                     self.manager.switch_to(GameScene(self.length, player_name=self.player_name, custom_key=self.key_vector))

class ConfigScene(Scene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont("Arial", 48)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.selected_length_index = 0
        self.lengths = ["CREER CLE"] + AUTHORIZED_LENGTH
        self.player_name = ""
        self.state = "NAME_INPUT" # States: "NAME_INPUT", "DIFFICULTY_SELECT"
        
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
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        if self.state == "NAME_INPUT":
            # Name Input UI
            name_label = self.small_font.render("Entrez votre nom :", True, (200, 200, 200))
            screen.blit(name_label, (SCREEN_WIDTH//2 - name_label.get_width()//2, 250))
            
            name_surface = self.font.render(self.player_name + "_", True, (0, 255, 255))
            screen.blit(name_surface, (SCREEN_WIDTH//2 - name_surface.get_width()//2, 290))
            
            instr = self.small_font.render("Appuyez sur ENTRÉE pour valider", True, (150, 150, 150))
            screen.blit(instr, (SCREEN_WIDTH//2 - instr.get_width()//2, 400))
            
        elif self.state == "DIFFICULTY_SELECT":
            # Greeting
            greet = self.small_font.render(f"Bonjour {self.player_name} !", True, (0, 255, 255))
            screen.blit(greet, (SCREEN_WIDTH//2 - greet.get_width()//2, 150))

            # Difficulty Selection
            sel_text = self.small_font.render("Sélectionnez la difficulté (Colonnes) :", True, (200, 200, 200))
            screen.blit(sel_text, (SCREEN_WIDTH//2 - sel_text.get_width()//2, 220))
            
            # Draw options VERTICALLY
            start_y = 300
            spacing_y = 60
            
            self.length_rects = []
            
            for i, length in enumerate(self.lengths):
                is_selected = (i == self.selected_length_index)
                color = (0, 255, 0) if is_selected else (100, 100, 100)
                
                # Add highlighting arrow/effect if selected
                text_str = str(length)
                if is_selected:
                    text_str = f"> {length} <"
                
                opt_text = self.font.render(text_str, True, color)
                
                x = SCREEN_WIDTH//2 - opt_text.get_width()//2
                y = start_y + i * spacing_y
                screen.blit(opt_text, (x, y))
                
                # Store rect (add some padding for easier clicking)
                r = opt_text.get_rect(topleft=(x,y))
                r.inflate_ip(40, 10)
                self.length_rects.append((r, i))

            # Instructions
            text = self.small_font.render("HAUT/BAS pour Choisir, ENTRÉE pour Jouer/Créer", True, (200, 200, 200))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 750))
            
            back = self.small_font.render("ECHAP pour revenir", True, (100, 100, 100))
            screen.blit(back, (SCREEN_WIDTH//2 - back.get_width()//2, 800))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == "NAME_INPUT":
                if event.key == pygame.K_RETURN:
                    if self.player_name.strip() == "":
                        self.player_name = "Player"
                    self.state = "DIFFICULTY_SELECT"
                elif event.key == pygame.K_ESCAPE:
                    self.manager.switch_to(MenuScene())
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    # Limit name length
                    if len(self.player_name) < 12 and event.unicode.isprintable():
                        self.player_name += event.unicode
                        
            elif self.state == "DIFFICULTY_SELECT":
                if event.key == pygame.K_UP:
                    self.selected_length_index = (self.selected_length_index - 1) % len(self.lengths)
                elif event.key == pygame.K_DOWN:
                    self.selected_length_index = (self.selected_length_index + 1) % len(self.lengths)
                elif event.key == pygame.K_RETURN:
                    selected = self.lengths[self.selected_length_index]
                    if selected == "CREER CLE":
                        self.manager.switch_to(KeyCreationScene(self.player_name))
                    else:
                        self.manager.switch_to(GameScene(selected, self.player_name))
                elif event.key == pygame.K_ESCAPE:
                    self.state = "NAME_INPUT"
                    
            # Mouse support for Difficulty Select
        if self.state == "DIFFICULTY_SELECT":
            if event.type == pygame.MOUSEMOTION:
                # Only checking inside the rects we stored
                if hasattr(self, 'length_rects'):
                    for rect, index in self.length_rects:
                        if rect.collidepoint(event.pos):
                            self.selected_length_index = index
                            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and hasattr(self, 'length_rects'):
                        for rect, index in self.length_rects:
                            if rect.collidepoint(event.pos):
                                self.selected_length_index = index
                                # Trigger same logic as ENTER
                                selected = self.lengths[self.selected_length_index]
                                if selected == "CREER CLE":
                                    self.manager.switch_to(KeyCreationScene(self.player_name))
                                else:
                                    self.manager.switch_to(GameScene(selected, self.player_name))

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
        title_surf = self.title_font.render("DEFI DEVERROUILLE", True, (255, 255, 255))
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
        label = self.msg_font.render("MESSAGE DECHIFFRE :", True, (100, 100, 100))
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
        txt_menu = self.btn_font.render("MENU PRINCIPAL", True, (255, 255, 255))
        screen.blit(txt_menu, (self.rect_menu.centerx - txt_menu.get_width()//2, self.rect_menu.centery - txt_menu.get_height()//2))
        
        # Next Button
        c_next = self.btn_hover_color if self.rect_next.collidepoint(mx, my) else self.btn_next_color
        pygame.draw.rect(screen, c_next, self.rect_next)
        txt_next = self.btn_font.render("PROCHAIN DEFI", True, (255, 255, 255))
        screen.blit(txt_next, (self.rect_next.centerx - txt_next.get_width()//2, self.rect_next.centery - txt_next.get_height()//2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect_menu.collidepoint(event.pos):
                    self.on_menu()
                elif self.rect_next.collidepoint(event.pos):
                    self.on_next()

class GameScene(Scene):
    def __init__(self, length=MIN_BOARD_LENGTH, player_name="Player", custom_key=None):
        super().__init__()
        self.current_length = length
        self.player_name = player_name
        
        # 1. Player Key Info (Always Standard)
        self.player_key_info = get_key_info()
        
        # 2. AI Key Info (Standard OR Custom)
        self.ai_key_info = get_key_info() # Start with standard copy
        
        if custom_key:
            # Inject Custom Key into AI Key Info (NOT Player)
            # 1. Private Key
            sk_entry = self.ai_key_info['private_key'][self.current_length]
            sk_entry['key'] = custom_key
            sk_entry['normal_key'] = []
            sk_entry['reverse_key'] = []
            sk_entry['number'] = []
            
            for val in custom_key:
                if val > 0:
                    sk_entry['normal_key'].append(COLUMN_TYPE_1)
                    sk_entry['reverse_key'].append(COLUMN_TYPE_2)
                    sk_entry['number'].append(val)
                elif val < 0:
                    sk_entry['normal_key'].append(COLUMN_TYPE_2)
                    sk_entry['reverse_key'].append(COLUMN_TYPE_1)
                    sk_entry['number'].append(-1 * val)
                else:
                    sk_entry['normal_key'].append(COLUMN_TYPE_3)
                    sk_entry['reverse_key'].append(COLUMN_TYPE_3)
                    sk_entry['number'].append(val)
            
            # 2. Public Key (Derived from Custom Private Key)
            rep = REPEAT_GEN_PUBLIC_KEY_LIST.get(self.current_length, 10)
            pk_vector = gen_public_key(self.current_length, custom_key, rep)
            
            pk_entry = self.ai_key_info['public_key'][self.current_length]
            pk_entry['key'] = pk_vector
            pk_entry['normal_key'] = []
            pk_entry['reverse_key'] = []
            pk_entry['number'] = []
            
            for val in pk_vector:
                if val > 0:
                    pk_entry['normal_key'].append(COLUMN_TYPE_1)
                    pk_entry['reverse_key'].append(COLUMN_TYPE_2)
                    pk_entry['number'].append(val)
                elif val < 0:
                    pk_entry['normal_key'].append(COLUMN_TYPE_2)
                    pk_entry['reverse_key'].append(COLUMN_TYPE_1)
                    pk_entry['number'].append(-1 * val)
                else:
                    pk_entry['normal_key'].append(COLUMN_TYPE_3)
                    pk_entry['reverse_key'].append(COLUMN_TYPE_3)
                    pk_entry['number'].append(val)

        # Generate Puzzles (Messages)
        # Player gets a puzzle based on PLAYER key
        self.player_target_message = self.generate_solvable_message(self.current_length, self.player_key_info)
        
        # AI gets a puzzle based on AI key
        self.ai_target_message = self.generate_solvable_message(self.current_length, self.ai_key_info)
        
        # Layout: Player Left, AI Right with Central Gap
        center_width = 300  
        side_margin = 150   
        
        available_width = SCREEN_WIDTH - center_width - 2 * side_margin
        box_width = available_width // 2
        
        top_margin = 120 
        bottom_margin = 80 
        box_height = SCREEN_HEIGHT - top_margin - bottom_margin
        
        self.player_box = GameBox(
            None, # Screen passed in draw
            x=side_margin, 
            y=top_margin, 
            width=box_width, 
            height=box_height,
            current_length=self.current_length,
            key_info=self.player_key_info,
            my_message=self.player_target_message,
            player=True
        )
        
        self.ai_box = GameBox(
            None,
            x=side_margin + box_width + center_width,
            y=top_margin,
            width=box_width,
            height=box_height,
            current_length=self.current_length,
            key_info=self.ai_key_info,
            my_message=self.ai_target_message, 
            player=False
        )
        
        self.ai = AI(self.ai_box, {'waitingIATime': 1000, 'keyFirstMoveTime': 500})
        self.ai.start()
        
        self.game_over = False
        self.game_over_timer = 0
        self.start_time = pygame.time.get_ticks() # Start Timer
        self.game_over_message = ""
        self.game_over_color = (255, 255, 255)
        self.victory_popup = None

    def generate_solvable_message(self, length, key_info_source):
        # Generate a message that is a linear combination of the PROVIDED key
        key_vector = key_info_source['private_key'][length]['key']
        
        # Find the "Spike" (Max absolute value index) in the key
        spike_val = max(key_vector, key=abs)
        spike_index = key_vector.index(spike_val)
        
        # Start with zero vector
        message_vector = [0] * length
        
        # Balanced steps
        if length <= 10:
            steps = 4 
        elif length <= 12:
            steps = 6
        elif length <= 14:
            steps = 10
        else: # 16
            steps = 15 
        
        for _ in range(steps):
            # Target a random column to "increase"
            target_col = random.randint(0, length - 1)
            
            # Calculate rotation needed to bring spike to target_col
            # rotate(l, k) shift left by k. new = (old - k) % mod
            # target = (spike - k) % mod  =>  k = (spike - target) % mod
            rot = (spike_index - target_col) % length
            
            rotated_key = rotate(length, key_vector, rot)
            
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
            if self.victory_popup is None and self.game_over_message == "DEFEAT...":
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
            self.game_over_message = "DEFAITE..."
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

        self.draw_key_indicators(screen)

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
        
        # Glow (Background)
        s = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 150), s.get_rect(), border_radius=10)
        screen.blit(s, rect)
        
        # Border
        color = (0, 255, 255) if is_player else (255, 0, 255)
        pygame.draw.rect(screen, color, rect, 2, border_radius=10)
        
        # Text
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        
        # Decorative dots
        pygame.draw.circle(screen, color, (rect.left - 10, rect.centery), 4)
        pygame.draw.circle(screen, color, (rect.right + 10, rect.centery), 4)

    def draw_key_indicators(self, screen):
        font = pygame.font.SysFont("Arial", 16, bold=True)
        
        # Player Indicator (PRIV) - Cyan
        indicator_y = self.player_box.rect.top - 25
        priv_text = font.render("CLE PRIV", True, (0, 255, 255))
        
        icon_x = self.player_box.rect.right - 20
        text_x = icon_x - priv_text.get_width() - 10
        
        screen.blit(priv_text, (text_x, indicator_y))
        
        # Icon (Player)
        pygame.draw.circle(screen, (0, 255, 255), (icon_x, indicator_y + 8), 6, 2)
        pygame.draw.line(screen, (0, 255, 255), (icon_x + 6, indicator_y + 8), (icon_x + 14, indicator_y + 8), 2)
        pygame.draw.line(screen, (0, 255, 255), (icon_x + 14, indicator_y + 8), (icon_x + 14, indicator_y + 12), 2)

        # AI Indicator (PUB) - Pink
        pub_text = font.render("CLE PUB", True, (255, 0, 255))
        
        icon_x_ai = self.ai_box.rect.left + 20
        text_x_ai = icon_x_ai + 20
        
        # Icon (AI)
        pygame.draw.circle(screen, (255, 0, 255), (icon_x_ai, indicator_y + 8), 6, 2)
        pygame.draw.line(screen, (255, 0, 255), (icon_x_ai + 6, indicator_y + 8), (icon_x_ai + 14, indicator_y + 8), 2)
        pygame.draw.line(screen, (255, 0, 255), (icon_x_ai + 14, indicator_y + 8), (icon_x_ai + 14, indicator_y + 12), 2)
        
        screen.blit(pub_text, (text_x_ai, indicator_y))

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
