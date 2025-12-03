import random
import pygame
import sys

pygame.init()


block_letter = random.choice("abcdefghijklmnopqrstuvwxyz")


# --- Fenêtre en plein écran ---
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = window.get_size()

pygame.display.set_caption("Cryptris")

# --- Paramètres grille ---
COLS, ROWS = 10, 20
CELL_SIZE = HEIGHT // ROWS  # grille pleine hauteur
GRID_HEIGHT = ROWS * CELL_SIZE
GRID_WIDTH = COLS * CELL_SIZE
GRID_X = (WIDTH - GRID_WIDTH) // 2
GRID_Y = 0
block_x = COLS // 2
block_y = 0

# --- Couleurs ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (50, 100, 255)

# --- Grille logique (stockage des blocs) ---
grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

# --- Bloc actif ---
block_x = COLS // 2
block_y = 0

clock = pygame.time.Clock()

def draw_grid():
    """Dessine la grille et les blocs empilés."""
    # Cases empilées
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] is not None:
                rect = pygame.Rect(
                    GRID_X + col * CELL_SIZE,
                    GRID_Y + row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(window, BLUE, rect)

                # Affichage de la lettre stockée dans la grille
                font = pygame.font.SysFont("consolas", CELL_SIZE - 6, bold=True)
                text = font.render(grid[row][col], True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                window.blit(text, text_rect)

    # Grille (lignes)
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(
                GRID_X + c * CELL_SIZE,
                GRID_Y + r * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(window, BLUE, rect, 1)


def block_can_move(nx, ny):
    """Vérifie si le bloc peut aller à (nx, ny)."""
    if nx < 0 or nx >= COLS:
        return False
    if ny >= ROWS:
        return False
    if ny >= 0 and grid[ny][nx] is not None:
        return False
    return True


def fix_block():
    global block_letter
    grid[block_y][block_x] = block_letter
    check_cancellation()  # si vous ajoutez les règles Cryptris
    new_block()


def new_block():
    global block_x, block_y, block_letter
    block_x = COLS // 2
    block_y = 0
    block_letter = random.choice("abcdefghijklmnopqrstuvwxyz")# lettre aléatoire

    # Game over si case déjà occupée
    if grid[block_y][block_x] is not None:
        pygame.quit()
        sys.exit()


def clear_full_lines():
    """Supprime les lignes pleines (Tetris classique)."""
    global grid
    new_grid = [row for row in grid if any(cell is None for cell in row)]
    removed = ROWS - len(new_grid)
    new_grid = [[None]*COLS for _ in range(removed)] + new_grid
    grid = new_grid

def get_connected_group(x, y):
    """Retourne la liste des cases connectées portant la même lettre."""
    target = grid[y][x]
    if target is None:
        return []

    to_visit = [(x, y)]
    visited = set()

    while to_visit:
        cx, cy = to_visit.pop()
        if (cx, cy) in visited:
            continue
        
        if grid[cy][cx] == target:
            visited.add((cx, cy))

            # Adjacent 4 directions
            for nx, ny in [(cx-1, cy), (cx+1, cy), (cx, cy-1), (cx, cy+1)]:
                if 0 <= nx < COLS and 0 <= ny < ROWS:
                    if grid[ny][nx] == target:
                        to_visit.append((nx, ny))

    return list(visited)


def annihilate_groups():
    """Supprime tous les groupes de 2 lettres identiques ou plus."""
    to_remove = set()

    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] is not None:
                group = get_connected_group(x, y)
                if len(group) >= 2:       # règle Cryptris
                    to_remove.update(group)

    # Suppression
    for (x, y) in to_remove:
        grid[y][x] = None

    return len(to_remove) > 0  # True = il y a eu annulation

def apply_gravity():
    """Fait tomber les blocs dans chaque colonne."""
    for x in range(COLS):
        column = [grid[y][x] for y in range(ROWS)]
        filtered = [c for c in column if c is not None]
        missing = ROWS - len(filtered)
        new_col = [None]*missing + filtered

        for y in range(ROWS):
            grid[y][x] = new_col[y]

def process_annihilation():
    """Boucle complète : annihilation → gravité → répéter tant que ça continue."""
    while True:
        has_removed = annihilate_groups()
        if not has_removed:
            break
        apply_gravity()

def check_cancellation():
    """Active les règles Cryptris complètes : annihilation + gravité."""
    process_annihilation()



running = True

while running:
    window.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Contrôles clavier ---
        if event.type == pygame.KEYDOWN:

            # Gauche
            if event.key == pygame.K_LEFT:
                if block_can_move(block_x - 1, block_y):
                    block_x -= 1

            # Droite
            if event.key == pygame.K_RIGHT:
                if block_can_move(block_x + 1, block_y):
                    block_x += 1

            # Descendre (NOUVEAU : pas de descente automatique)
            if event.key == pygame.K_DOWN:
                # le bloc descend seulement quand on appuie sur ↓
                while block_can_move(block_x, block_y + 1):
                    block_y += 1
                
                # bloqué → on le fige et on en crée un nouveau
                fix_block()
                clear_full_lines()

            # Échap = quitter
            if event.key == pygame.K_ESCAPE:
                running = False

    # --- Affichage grille + blocs ---
    draw_grid()

    # Affichage du bloc actif
    rect = pygame.Rect(
        GRID_X + block_x * CELL_SIZE,
        GRID_Y + block_y * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )
    pygame.draw.rect(window, BLUE, rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
