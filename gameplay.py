import pygame
import random
import math

# --- Configuration ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Typing - Ninja Style")
clock = pygame.time.Clock()

# Couleurs et Polices
DARK_BLUE, YELLOW, RED, GREEN, WHITE = (44, 62, 80), (241, 196, 15), (231, 76, 60), (46, 204, 113), (255, 255, 255)
font_letter = pygame.font.SysFont("Arial", 32, bold=True)
font_ui = pygame.font.SysFont("Arial", 45, bold=True)
font_small = pygame.font.SysFont("Arial", 24, bold=True)

# --- Chargement des Images ---
IMAGES_LIST = {
    'abricot': 'abricot.png', 'ananas': 'ananas.png', 'banane': 'banane.png',
    'bombe': 'bombe.png', 'bonus_etoile': 'bonus_etoile.png',
    'fruit_dragon': 'fruit_du_dragon.png', 'kiwi': 'kiwi.png',
    'mangue': 'mangue.png', 'pasteque': 'pasteque.png', 'pomme': 'pomme.png',
    'piege_etoile': 'piege_etoile.png', 'coeur': 'coeur.png' # Notre nouvel objet rare
}

IMG_DATA = {}
for name, filename in IMAGES_LIST.items():
    try:
        img = pygame.image.load(filename).convert_alpha()
        IMG_DATA[name] = pygame.transform.scale(img, (60, 60))
    except:
        surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(surf, RED if name in ['bombe', 'coeur'] else GREEN, (30, 30), 25)
        IMG_DATA[name] = surf

# Image pour l'UI des vies
try:
    img_coeur_ui = pygame.image.load("coeur_pouls.png").convert_alpha()
    img_coeur_ui = pygame.transform.scale(img_coeur_ui, (35, 35))
except:
    img_coeur_ui = pygame.Surface((35, 35)); img_coeur_ui.fill(RED)

# --- Classe Objet Ninja (Propulsion) ---
class GameObject:
    def __init__(self, speed):
        # On choisit 'coeur' seulement 5% du temps
        prob = random.random()
        if prob < 0.05: self.type = 'coeur'
        else: self.type = random.choice([k for k in IMG_DATA.keys() if k != 'coeur'])
        
        self.image = IMG_DATA[self.type]
        self.letter = random.choice("abcdefghijklmnopqrstuvwxyz")
        
        # Position de départ : En bas de l'écran
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT + 20
        
        # Propulsion vers le haut (vitesse verticale négative)
        self.vy = random.uniform(-14, -18) - (speed * 0.5)
        # Petit décalage horizontal
        self.vx = random.uniform(-2, 2)
        self.gravity = 0.35 # La force qui fait retomber le fruit

    def move(self):
        self.vy += self.gravity # La gravité tire vers le bas
        self.y += self.vy
        self.x += self.vx

    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))
        color = RED if self.type == 'bombe' else YELLOW
        txt = font_letter.render(self.letter.upper(), True, color)
        surf.blit(txt, (self.x + 18, self.y + 60))

# --- Variables de Session ---
game_mode = "MENU"
score, vies, score_goal = 0, 3, 500
difficulty_speed = 3.0
spawn_delay = 1200
time_limit = 30
start_ticks = 0
active_objects = []
shake_amount = 0

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, spawn_delay)

def draw_menu():
    screen.fill(DARK_BLUE)
    title = font_ui.render("FRUIT NINJA TYPING", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
    txt_c = font_small.render("[C] MODE CLASSIQUE", True, GREEN)
    txt_h = font_small.render("[H] MODE CHALLENGE", True, YELLOW)
    screen.blit(txt_c, (WIDTH // 2 - txt_c.get_width() // 2, 320))
    screen.blit(txt_h, (WIDTH // 2 - txt_h.get_width() // 2, 380))

# --- Boucle Principale ---
running = True
while running:
    render_offset = [0, 0]
    if shake_amount > 0:
        render_offset = [random.randint(-shake_amount, shake_amount), random.randint(-shake_amount, shake_amount)]
        shake_amount -= 2

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: running = False
        
        if game_mode == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c: game_mode, score, vies, active_objects = "CLASSIQUE", 0, 3, []
                if event.key == pygame.K_h: game_mode, score, vies, active_objects = "CHALLENGE", 0, 3, [], pygame.time.get_ticks()

        elif game_mode in ["CLASSIQUE", "CHALLENGE"]:
            if event.type == SPAWN_EVENT:
                active_objects.append(GameObject(difficulty_speed))
            
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key).lower()
                for obj in active_objects[:]:
                    if obj.letter == key:
                        if obj.type == 'bombe':
                            vies -= 1; shake_amount = 15; active_objects = []
                        elif obj.type == 'coeur':
                            vies = min(3, vies + 1) # Max 3 vies
                        elif obj.type == 'bonus_etoile':
                            active_objects = [o for o in active_objects if o.type == 'bombe']; score += 50
                        elif obj.type == 'piege_etoile':
                            if any(o.type == 'bombe' for o in active_objects): vies -= 1; shake_amount = 15; active_objects = []
                            else: active_objects = []; score += 30
                        else: score += 10
                        if obj in active_objects: active_objects.remove(obj)
                        break

    if game_mode == "MENU":
        draw_menu()
    else:
        game_surf = pygame.Surface((WIDTH, HEIGHT))
        game_surf.fill(DARK_BLUE)
        
        if vies <= 0: game_mode = "MENU"

        # Logique des modes
        if game_mode == "CLASSIQUE":
            ui_txt = font_small.render(f"Score: {score}/{score_goal}", True, WHITE)
            if score >= score_goal:
                score_goal += 500; difficulty_speed += 0.5
                spawn_delay = max(400, spawn_delay - 100)
                pygame.time.set_timer(SPAWN_EVENT, spawn_delay)
                game_mode = "MENU"
        elif game_mode == "CHALLENGE":
            start_ticks = start_ticks if 'start_ticks' in locals() else pygame.time.get_ticks() # Fix challenge start
            # (Logique timer ici...)

        # Mise à jour Ninja
        for obj in active_objects[:]:
            obj.move()
            obj.draw(game_surf)
            # Supprime si l'objet est retombé sous l'écran
            if obj.y > HEIGHT + 50 and obj.vy > 0:
                active_objects.remove(obj)
                if game_mode == "CLASSIQUE" and obj.type not in ['bombe', 'coeur']: score -= 5

        # Affichage UI des Vies avec coeur_pouls.png
        for i in range(vies):
            game_surf.blit(img_coeur_ui, (20 + (i * 40), 50))
        game_surf.blit(ui_txt, (20, 20))
        
        screen.blit(game_surf, render_offset)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()