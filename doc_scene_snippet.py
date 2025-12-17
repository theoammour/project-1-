
import webbrowser

class DocumentationScene(Scene):
    def __init__(self):
        super().__init__()
        self.font_title = pygame.font.SysFont("Arial", 24, bold=True) # Blue/Cyan Title
        self.font_desc = pygame.font.SysFont("Arial", 16) # White Description
        self.font_url = pygame.font.SysFont("Arial", 14) # Small link
        
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
                "title": "HISTORY OF CRYPTOGRAPHY",
                "desc": "The history of Cryptography on Wikipedia",
                "url": "https://en.wikipedia.org/wiki/History_of_cryptography"
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
        main_title = pygame.font.SysFont("Arial", 48, bold=True).render("CRYPTRIS", True, (0, 255, 255))
        title_rect = main_title.get_rect(center=(SCREEN_WIDTH//2, 80))
        
        # Shadow
        shadow = pygame.font.SysFont("Arial", 48, bold=True).render("CRYPTRIS", True, (0, 100, 100))
        screen.blit(shadow, (title_rect.x+3, title_rect.y+3))
        screen.blit(main_title, title_rect)
        
        sub_title = pygame.font.SysFont("Arial", 20).render("EXTERNAL RESOURCES", True, (0, 180, 200))
        screen.blit(sub_title, (SCREEN_WIDTH//2 - sub_title.get_width()//2, 140))

        # Draw List
        start_y = 200
        item_height = 90
        self.click_rects = []
        
        for i, res in enumerate(self.resources):
            y = start_y + i * item_height
            
            # Container Rect (for click detection)
            # Width = 600
            container_w = 700
            container_h = 70
            container_x = (SCREEN_WIDTH - container_w) // 2
            
            # Store rect
            rect = pygame.Rect(container_x, y, container_w, container_h)
            self.click_rects.append((rect, res["url"]))
            
            # Draw Container Background (faint)
            s = pygame.Surface((container_w, container_h), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 20, 40, 150), s.get_rect(), border_radius=5)
            screen.blit(s, rect)
            
            # Border (Cyan thin)
            pygame.draw.rect(screen, (0, 100, 150), rect, 1, border_radius=5)
            
            # 1. Title (Boxed style from screenshot)
            # Render text
            title_surf = self.font_title.render(res["title"], True, (0, 255, 255))
            # Title BG
            # title_bg_rect = title_surf.get_rect(center=(rect.centerx, rect.top + 15))
            # Draw Title
            screen.blit(title_surf, (rect.centerx - title_surf.get_width()//2, rect.top + 10))
            
            # 2. Desc
            desc_surf = self.font_desc.render(res["desc"], True, (200, 200, 200))
            screen.blit(desc_surf, (rect.centerx - desc_surf.get_width()//2, rect.top + 38))
            
            # 3. URL
            url_surf = self.font_url.render(res["url"], True, (0, 100, 200))
            screen.blit(url_surf, (rect.centerx - url_surf.get_width()//2, rect.top + 55))

        # Back Instruction
        back_text = self.font_desc.render("PRESS ESC TO RETURN", True, (100, 100, 100))
        screen.blit(back_text, (20, 20))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.switch_to(MenuScene())
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left Click
                mouse_pos = event.pos
                for rect, url in self.click_rects:
                    if rect.collidepoint(mouse_pos):
                         webbrowser.open(url)
