import pygame
import os
from settings import (
    COLUMN_TYPE_1, COLUMN_TYPE_2, COLUMN_TYPE_3, BOARD_SYMBOLS,
    PLAYER_BOARD_COLORS, IA_BOARD_COLORS, SQUARE_WIDTH, SQUARE_HEIGHT, SPACE_HEIGHT, SPACE_WIDTH,
    BORDER_WIDTH, BORDER_HEIGHT, COLUMN_WIDTH
)
from cryptris_logic import ternary_to_symbol, gen_public_key, PREGENERATED_PRIVATE_KEYS, REPEAT_GEN_PUBLIC_KEY_LIST

class GameBox:
    def __init__(self, screen, x, y, width, height, current_length, key_info, my_message, player=True):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.current_length = current_length
        self.key_info = key_info
        self.my_message = my_message
        self.player = player
        
        self.colors = PLAYER_BOARD_COLORS if player else IA_BOARD_COLORS
        
        self.message_columns = []
        self.key_columns = []
        
        self.waiting_for_regeneration = False
        
        self.init_columns()
        
        # Load Fonts
        try:
            self.font = pygame.font.Font("cryptris/fonts/inconsolata-regular.ttf", 15)
            self.symbol_font = pygame.font.Font("cryptris/fonts/inconsolata-regular.ttf", 20)
        except:
            print("Warning: Could not load custom fonts. Using system default.")
            self.font = pygame.font.SysFont("Consolas", 15)
            self.symbol_font = pygame.font.SysFont("Consolas", 20)

        # Load Background
        try:
            bg_path = os.path.join("cryptris", "img", "bg-circuits.png")
            self.bg_image = pygame.image.load(bg_path).convert()
        except:
            self.bg_image = None

    def init_columns(self):
        # Calculate dynamic dimensions to fit the box
        
        # 1. Width Calculation - properly account for spacing AND padding
        # Add horizontal padding to keep columns away from box edges
        horizontal_padding = 20  # Extra padding on each side
        available_width = self.rect.width - 2 * BORDER_WIDTH - 2 * horizontal_padding
        
        # For larger boards, reduce spacing to fit more columns
        if self.current_length <= 10:
            space_width = SPACE_WIDTH  # 4px
        elif self.current_length <= 12:
            space_width = 3  # Tighter spacing
        else:  # 14, 16
            space_width = 2  # Very tight spacing
        
        # Total width formula: n*col_width + (n-1)*space_width = available_width
        # Solving for col_width: col_width = (available_width - (n-1)*space_width) / n
        total_spacing = (self.current_length - 1) * space_width
        calculated_col_width = (available_width - total_spacing) / self.current_length
        
        # Ensure minimum width of 5px and don't exceed COLUMN_WIDTH
        self.col_width = max(5, min(COLUMN_WIDTH, int(calculated_col_width)))
        self.space_width = space_width  # Store for draw method
        self.horizontal_padding = horizontal_padding  # Store for draw method
        
        # 2. Height Calculation (Initial pass to find max value)
        # We need to check both message and key values to determine the scale
        # But we haven't created the objects yet. Let's look at the data.
        msg_data = self.my_message
        if self.player:
            key_data = self.key_info['private_key'][self.current_length]
        else:
            key_data = self.key_info['public_key'][self.current_length]
        
        max_val = 1
        if msg_data['message_number']:
            max_val = max(max_val, max(msg_data['message_number']))
            
        # Handle both dict (organic) and list (standard) key data
        if isinstance(key_data, dict) and 'number' in key_data:
             if key_data['number']:
                max_val = max(max_val, max(key_data['number']))
        elif isinstance(key_data, list):
             # For lists, height is roughly proportional to value, or max value is 3?
             # Actually, if it's a list, we don't have explicit 'number' (heights).
             # We can approximate or just use max absolute value?
             # Standard game logic implies height ~ value absolute?
             # Let's use max(abs(x) for x in key_data)
             max_k = max(abs(x) for x in key_data) if key_data else 1
             max_val = max(max_val, max_k)
            
        # Add some headroom for gameplay (stacking)
        max_val = int(max_val * 1.5) 
        
        available_height = self.rect.height - 2 * BORDER_HEIGHT
        
        # Calculate max possible height per block to fit 'max_val' blocks
        # height = n * (h + space) - space
        # h * n + space * (n-1) = available
        # h * n = available - space * (n-1)
        # h = (available - space * (n-1)) / n
        
        max_block_height = (available_height - SPACE_HEIGHT * (max_val - 1)) / max_val
        
        # Clamp height
        self.square_height = max(2, min(SQUARE_HEIGHT, max_block_height))
        
        # Recalculate width to maintain aspect ratio? No, blocks can be flat.
        # But let's ensure they aren't too thin?
        
        # Initialize Message Columns (The target)
        for i in range(self.current_length):
            col_type = msg_data['message_type'][i]
            val = msg_data['message_number'][i]
            self.message_columns.append(MessageColumn(i, col_type, val, self.colors, self.col_width, self.square_height))

        # Initialize Key Columns (The player's key)
        for i in range(self.current_length):
            col_type = key_data['normal_key'][i]
            val = key_data['number'][i]
            self.key_columns.append(KeyColumn(i, col_type, val, self.colors, self.col_width, self.square_height))

    # ... (handle_input, handle_mouse, rotate, invert unchanged) ...
    def handle_input(self, event):
        if event.key == pygame.K_LEFT:
            self.rotate_left()
        elif event.key == pygame.K_RIGHT:
            self.rotate_right()
        elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
            self.invert_key()
        elif event.key == pygame.K_DOWN:
            self.apply_key()

    def handle_mouse(self, event):
        pass

    def rotate_left(self):
        first = self.key_columns.pop(0)
        self.key_columns.append(first)
        self.update_column_indices()

    def rotate_right(self):
        last = self.key_columns.pop()
        self.key_columns.insert(0, last)
        self.update_column_indices()

    def invert_key(self):
        for col in self.key_columns:
            col.invert()

    def update_column_indices(self):
        for i, col in enumerate(self.key_columns):
            col.index = i

    def update(self):
        # Update Key Columns (Falling)
        for col in self.key_columns:
            col.update()
            if col.is_falling and col.y_offset >= col.target_y_offset:
                # Collision detected
                col.y_offset = col.target_y_offset
                col.is_falling = False
                self.resolve_collision(col)

        # Update Message Columns (Effects)
        for col in self.message_columns:
            col.update()
            
        self.adjust_scale()

    def adjust_scale(self):
        # Find max height in blocks (message columns + potential key height)
        max_blocks = 0
        for col in self.message_columns:
            if col.type != COLUMN_TYPE_3:
                max_blocks = max(max_blocks, col.value)
        
        # Add buffer for falling key (approx max key height)
        # We want to ensure we can see the stack + some space
        max_blocks += 5 # Buffer
        
        available_height = self.rect.height - 2 * BORDER_HEIGHT
        
        # Calculate needed height
        # h = (available - space * (n-1)) / n
        if max_blocks > 0:
            needed_height = (available_height - SPACE_HEIGHT * (max_blocks - 1)) / max_blocks
            
            # Clamp minimum to 1 pixel to avoid invisible blocks, but allow it to get very small
            needed_height = max(1, min(SQUARE_HEIGHT, needed_height))
            
            # Apply if smaller (Zoom out only? Or zoom in too? Let's zoom out only for stability)
            if needed_height < self.square_height:
                self.square_height = needed_height
                # Update all columns
                for col in self.message_columns:
                    col.square_height = self.square_height
                for col in self.key_columns:
                    col.square_height = self.square_height

    def resolve_collision(self, key_col):
        msg_col = self.message_columns[key_col.index]
        
        # Logic for merging columns
        if msg_col.type == COLUMN_TYPE_3: # Empty
            msg_col.type = key_col.type
            msg_col.value = key_col.value
        elif msg_col.type == key_col.type:
            msg_col.value += key_col.value
        else:
            # Different types - Destruction
            destruction_amount = min(msg_col.value, key_col.value)
            
            # Add destruction effect
            msg_col.add_destruction_effect(destruction_amount, msg_col.type, key_col.type)
            
            if msg_col.value > key_col.value:
                msg_col.value -= key_col.value
            elif msg_col.value < key_col.value:
                msg_col.value = key_col.value - msg_col.value
                msg_col.type = key_col.type
            else:
                msg_col.value = 0
                msg_col.type = COLUMN_TYPE_3
        
        # Reset Key Column (Same key falls again)
        key_col.reset()


    def draw(self):
        # Background is handled by the Scene
        
        # Draw Game Box Container (Semi-transparent blue)
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill((0, 113, 187, 50))
        self.screen.blit(s, self.rect)
        
        # Calculate positions using dynamic spacing and padding
        total_width = self.current_length * (self.col_width + self.space_width) - self.space_width
        # Center the columns in the box
        start_x = self.rect.x + (self.rect.width - total_width) // 2
        
        # Set clipping to prevent overflow
        old_clip = self.screen.get_clip()
        self.screen.set_clip(self.rect)
        
        try:
            # Draw Columns Backgrounds
            for i in range(self.current_length):
                x = start_x + i * (self.col_width + self.space_width)
                col_rect = pygame.Rect(x, self.rect.y + BORDER_HEIGHT, self.col_width, self.rect.height - 2 * BORDER_HEIGHT)
                pygame.draw.rect(self.screen, self.colors['columnColor'], col_rect)

            bottom_y = self.rect.bottom - BORDER_HEIGHT
            
            # Draw Message Columns
            for i, col in enumerate(self.message_columns):
                x = start_x + i * (self.col_width + self.space_width)
                col.draw(self.screen, x, bottom_y, self.col_width, self.font)

            # Draw Key Columns
            key_y = self.rect.top + BORDER_HEIGHT
            for i, col in enumerate(self.key_columns):
                x = start_x + i * (self.col_width + self.space_width)
                col.draw(self.screen, x, key_y, self.col_width, self.font, is_key=True)
                
        finally:
            # Restore clipping
            self.screen.set_clip(old_clip)

    def check_status(self):
        """
        Vérifie l'état du jeu (Victoire ou Défaite).
        Condition de victoire : Toutes les colonnes doivent avoir une hauteur <= 1.
        Cette condition stricte garantit que le joueur a décrypté le message.
        """
        all_low = True
        total_mass = 0
        
        for col in self.message_columns:
            # Si la valeur est 0, on s'assure que le type est marqué comme vide
            if col.value == 0 and col.type != COLUMN_TYPE_3:
                 col.type = COLUMN_TYPE_3
            
            total_mass += max(0, col.value)
            
            # Vérification Critique : Hauteur Absolue > 1
            # On tolère une hauteur de 1 (bruit)
            if col.value > 1: 
                all_low = False
                
        if all_low:
             return "WIN"

        return "PLAYING"

    def apply_key(self):
        # Trigger falling for all key columns
        for i in range(self.current_length):
            key_col = self.key_columns[i]
            msg_col = self.message_columns[i]
            
            # Calculate target Y (top of message column)
            # Message column height
            msg_height = msg_col.value * (self.square_height + SPACE_HEIGHT)
            if msg_col.type == COLUMN_TYPE_3:
                msg_height = 0
            
            # Available height in pixels
            available_height = (self.rect.height - 2 * BORDER_HEIGHT)
            
            # Target Y offset (positive downwards)
            # Start Y is key_y (top + border)
            # Target Y is bottom - border - msg_height - key_height
            
            key_height = key_col.value * (self.square_height + SPACE_HEIGHT)
            
            # Distance to fall
            # We want the bottom of the key to hit the top of the message
            # Key bottom is at y_offset + key_height
            # Message top is at available_height - msg_height
            
            dist = available_height - msg_height - key_height - SPACE_HEIGHT
            
            key_col.start_fall(dist)


class Column:
    def __init__(self, index, col_type, value, colors, col_width, square_height):
        self.index = index
        self.type = col_type
        self.value = value
        self.colors = colors
        self.col_width = col_width
        self.square_height = square_height

    def draw_gradient_rect(self, screen, rect, color_left, color_right, alpha=255):
        gradient_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        r1, g1, b1 = color_left
        r2, g2, b2 = color_right
        
        for x in range(int(rect.width)):
            ratio = x / rect.width
            r = int(r1 * (1 - ratio) + r2 * ratio)
            g = int(g1 * (1 - ratio) + g2 * ratio)
            b = int(b1 * (1 - ratio) + b2 * ratio)
            pygame.draw.line(gradient_surface, (r, g, b, alpha), (x, 0), (x, rect.height))
            
        screen.blit(gradient_surface, rect)

    def draw(self, screen, x, y, width, font, is_key=False):
        pass # Implemented in subclasses

class MessageColumn(Column):
    def __init__(self, index, col_type, value, colors, col_width, square_height):
        super().__init__(index, col_type, value, colors, col_width, square_height)
        self.effects = []

    def update(self):
        # Update effects
        for effect in self.effects[:]:
            effect.update()
            if effect.is_finished():
                self.effects.remove(effect)

    def add_destruction_effect(self, amount, type1, type2):
        self.effects.append(BlockEffect(amount, type1, type2, self.colors, self.col_width, self.square_height))

    def draw(self, screen, x, y, width, font, is_key=False):
        # Draw base column
        if self.type != COLUMN_TYPE_3:
            total_block_height = self.value * (self.square_height + SPACE_HEIGHT) - SPACE_HEIGHT
            start_y = y - total_block_height
            
            c_left = self.colors['colorLeft'][self.type]
            c_right = self.colors['colorRight'][self.type]
            c_stroke = self.colors['strokeColor'][self.type]

            for i in range(self.value):
                block_y = y - (i + 1) * (self.square_height + SPACE_HEIGHT) + SPACE_HEIGHT
                block_rect = pygame.Rect(x + 1.5, block_y, self.col_width, self.square_height)
                self.draw_gradient_rect(screen, block_rect, c_left, c_right)
                pygame.draw.rect(screen, c_stroke, block_rect, 1)

            # Draw Number
            text = font.render(str(self.value), True, self.colors['numberColor'])
            screen.blit(text, (x + width//2 - text.get_width()//2, y + 5))

        # Draw Effects
        current_height_px = self.value * (self.square_height + SPACE_HEIGHT)
        effect_start_y = y - current_height_px
        
        for effect in self.effects:
            effect.draw(screen, x, effect_start_y)


class KeyColumn(Column):
    def __init__(self, index, col_type, value, colors, col_width, square_height):
        super().__init__(index, col_type, value, colors, col_width, square_height)
        self.y_offset = 0
        self.target_y_offset = 0
        self.is_falling = False
        self.fall_speed = 20 # pixels per frame

    def start_fall(self, distance):
        self.target_y_offset = distance
        self.is_falling = True

    def update(self):
        if self.is_falling:
            self.y_offset += self.fall_speed
            if self.y_offset >= self.target_y_offset:
                self.y_offset = self.target_y_offset
                # Collision handled by GameBox

    def reset(self):
        self.y_offset = 0
        self.target_y_offset = 0
        self.is_falling = False

    def invert(self):
        if self.type == COLUMN_TYPE_1:
            self.type = COLUMN_TYPE_2
        elif self.type == COLUMN_TYPE_2:
            self.type = COLUMN_TYPE_1

    def draw(self, screen, x, y, width, font, is_key=True):
        if self.type == COLUMN_TYPE_3:
            return

        # Apply offset
        draw_y = y + self.y_offset
        
        height = self.value * (self.square_height + SPACE_HEIGHT) - SPACE_HEIGHT
        
        c_left = self.colors['colorLeft'][self.type]
        c_right = self.colors['colorRight'][self.type]
        c_stroke = self.colors['strokeColor'][self.type]
        
        for i in range(self.value):
            block_y = draw_y + i * (self.square_height + SPACE_HEIGHT)
            block_rect = pygame.Rect(x + 1.5, block_y, self.col_width, self.square_height)
            self.draw_gradient_rect(screen, block_rect, c_left, c_right)
            pygame.draw.rect(screen, c_stroke, block_rect, 1)

        # Draw Number
        text = font.render(str(self.value), True, self.colors['numberColor'])
        screen.blit(text, (x + width//2 - text.get_width()//2, draw_y - 25))

class BlockEffect:
    def __init__(self, amount, type1, type2, colors, col_width, square_height):
        self.amount = amount
        self.type1 = type1
        self.type2 = type2
        self.colors = colors
        self.col_width = col_width
        self.square_height = square_height
        self.alpha = 255
        self.fade_speed = 10 # Alpha per frame

    def update(self):
        self.alpha -= self.fade_speed
        if self.alpha < 0:
            self.alpha = 0

    def is_finished(self):
        return self.alpha == 0

    def draw(self, screen, x, start_y):
        c_left = self.colors['colorLeft'].get(self.type1, (255,255,255))
        c_right = self.colors['colorRight'].get(self.type1, (255,255,255))
        
        for i in range(self.amount):
            # Moving upwards
            block_y = start_y - (i + 1) * (self.square_height + SPACE_HEIGHT) + SPACE_HEIGHT
            
            rect = pygame.Rect(x + 1.5, block_y, self.col_width, self.square_height)
            
            # Draw with alpha
            s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            
            # Gradient
            r1, g1, b1 = c_left
            r2, g2, b2 = c_right
            for lx in range(int(rect.width)):
                ratio = lx / rect.width
                r = int(r1 * (1 - ratio) + r2 * ratio)
                g = int(g1 * (1 - ratio) + g2 * ratio)
                b = int(b1 * (1 - ratio) + b2 * ratio)
                pygame.draw.line(s, (r, g, b, self.alpha), (lx, 0), (lx, rect.height))
            
            screen.blit(s, rect)
            
            # Border
            pygame.draw.rect(screen, (255, 255, 255, self.alpha), rect, 1)
