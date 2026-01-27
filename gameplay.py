import pygame
import random
import os

# --- Configuration ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_surf = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja Ultimate - Fixed Edition")
clock = pygame.time.Clock()

# Couleurs
DARK_BLUE = (44, 62, 80)
YELLOW, RED, GREEN, WHITE = (241, 196, 15), (231, 76, 60), (46, 204, 113), (255, 255, 255)
GOLD, PURPLE, ICE_BLUE = (255, 215, 0), (155, 89, 182), (100, 200, 255)
ORANGE = (255, 165, 0)
PINK = (255, 182, 193)
BROWN = (139, 69, 19)
LIGHT_GREEN = (144, 238, 144)

# Polices
font_letter = pygame.font.SysFont("Arial", 30, bold=True)
font_small = pygame.font.SysFont("Arial", 20, bold=True)
font_huge = pygame.font.SysFont("Arial", 40, bold=True) 

# --- Dictionnaire ---
if os.path.exists("mots.txt"):
    with open("mots.txt", "r", encoding="utf-8") as f:
        DICTIONNAIRE = [line.strip().upper() for line in f if line.strip()]
else:
    DICTIONNAIRE = ["FRUIT", "PYTHON", "LOTO", "BONUS", "NINJA", "GLACE"]

# --- Fonction pour créer des fruits dessinés ---
def create_fruit_surface(fruit_type, size=60):
    """Crée une surface pygame avec un fruit dessiné"""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    if fruit_type == "pomme":
        # Pomme rouge avec feuille
        pygame.draw.circle(surf, RED, (center, center), center - 5)
        pygame.draw.ellipse(surf, GREEN, (center - 5, 5, 10, 15))
        pygame.draw.circle(surf, (200, 50, 50), (center - 8, center - 8), 8)
        
    elif fruit_type == "banane":
        # Banane jaune courbée
        pygame.draw.ellipse(surf, YELLOW, (10, center - 10, size - 20, 20))
        pygame.draw.line(surf, BROWN, (10, center), (size - 10, center), 2)
        
    elif fruit_type == "orange":
        # Orange avec texture
        pygame.draw.circle(surf, ORANGE, (center, center), center - 5)
        for i in range(8):
            angle = i * 45
            x = center + int((center - 10) * 0.7 * pygame.math.Vector2(1, 0).rotate(angle).x)
            y = center + int((center - 10) * 0.7 * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.circle(surf, (255, 140, 0), (x, y), 3)
            
    elif fruit_type == "pasteque":
        # Pastèque verte et rouge
        pygame.draw.circle(surf, GREEN, (center, center), center - 5)
        pygame.draw.circle(surf, RED, (center, center), max(3, center - 12))
        if size > 30:
            for _ in range(5):
                px = random.randint(center - 10, center + 10)
                py = random.randint(center - 10, center + 10)
                pygame.draw.circle(surf, (50, 50, 50), (px, py), 2)
            
    elif fruit_type == "fraise":
        # Fraise rouge avec points
        points = [(center, 10), (size - 10, size - 10), (10, size - 10)]
        pygame.draw.polygon(surf, RED, points)
        if size > 30:
            pygame.draw.polygon(surf, GREEN, [(center - 8, 10), (center + 8, 10), (center, 5)])
            for i in range(6):
                px = random.randint(15, size - 15)
                py = random.randint(20, size - 15)
                pygame.draw.circle(surf, YELLOW, (px, py), 2)
            
    elif fruit_type == "raisin":
        # Grappe de raisin
        positions = [(center, center - 10), (center - 10, center), (center + 10, center),
                     (center - 5, center + 10), (center + 5, center + 10)]
        for pos in positions:
            pygame.draw.circle(surf, PURPLE, pos, max(3, int(size * 0.13)))
        pygame.draw.line(surf, BROWN, (center, 5), (center, center - 10), 3)
        
    elif fruit_type == "cerise":
        # Deux cerises
        pygame.draw.circle(surf, RED, (center - 8, center + 5), max(5, int(size * 0.16)))
        pygame.draw.circle(surf, RED, (center + 8, center + 5), max(5, int(size * 0.16)))
        pygame.draw.line(surf, BROWN, (center, 5), (center - 8, center + 5), 2)
        pygame.draw.line(surf, BROWN, (center, 5), (center + 8, center + 5), 2)
        
    elif fruit_type == "citron":
        # Citron jaune
        pygame.draw.ellipse(surf, YELLOW, (10, center - 12, size - 20, 24))
        pygame.draw.circle(surf, (255, 255, 150), (center - 8, center - 5), 6)
        
    elif fruit_type == "kiwi":
        # Kiwi marron et vert
        pygame.draw.circle(surf, BROWN, (center, center), center - 5)
        pygame.draw.circle(surf, LIGHT_GREEN, (center, center), max(3, center - 10))
        pygame.draw.circle(surf, WHITE, (center, center), max(2, int(size * 0.06)))
        if size > 30:
            for i in range(12):
                angle = i * 30
                x = center + int(8 * pygame.math.Vector2(1, 0).rotate(angle).x)
                y = center + int(8 * pygame.math.Vector2(1, 0).rotate(angle).y)
                pygame.draw.line(surf, (100, 150, 100), (center, center), (x, y), 1)
            
    elif fruit_type == "ananas":
        # Ananas jaune avec couronne
        pygame.draw.ellipse(surf, YELLOW, (center - 15, center - 5, 30, 35))
        for i in range(5):
            pygame.draw.line(surf, GREEN, (center + (i-2)*5, 10), (center + (i-2)*5, 20), 3)
        if size > 30:
            for y in range(3):
                for x in range(3):
                    px = center - 10 + x * 10
                    py = center + y * 10
                    pygame.draw.line(surf, ORANGE, (px - 3, py), (px + 3, py), 2)
                
    elif fruit_type == "peche":
        # Pêche rose/orange
        pygame.draw.circle(surf, (255, 150, 100), (center, center), center - 5)
        pygame.draw.ellipse(surf, (255, 100, 100), (center - 5, center - 15, 10, 30))
        pygame.draw.circle(surf, (255, 180, 120), (center - 10, center - 10), 8)
        
    elif fruit_type == "poire":
        # Poire verte
        pygame.draw.ellipse(surf, LIGHT_GREEN, (center - 12, center - 5, 24, 30))
        pygame.draw.ellipse(surf, LIGHT_GREEN, (center - 8, 10, 16, 20))
        pygame.draw.line(surf, BROWN, (center, 8), (center, 15), 3)
        
    elif fruit_type == "abricot":
        # Abricot orange
        pygame.draw.circle(surf, (255, 165, 0), (center, center), center - 5)
        pygame.draw.ellipse(surf, (255, 140, 0), (center - 5, center - 15, 10, 30))
        
    elif fruit_type == "framboise":
        # Framboise rouge
        for i in range(3):
            for j in range(3):
                pygame.draw.circle(surf, (220, 20, 60), (center - 8 + i * 8, center - 8 + j * 8), 4)
                
    elif fruit_type == "fruit_du_dragon":
        # Fruit du dragon
        pygame.draw.ellipse(surf, (255, 20, 147), (center - 15, center - 10, 30, 25))
        for i in range(5):
            pygame.draw.polygon(surf, GREEN, [
                (center + (i-2)*8, center - 15),
                (center + (i-2)*8 - 3, center - 5),
                (center + (i-2)*8 + 3, center - 5)
            ])
            
    elif fruit_type == "mangue":
        # Mangue
        pygame.draw.ellipse(surf, (255, 200, 0), (center - 15, center - 10, 30, 25))
        pygame.draw.circle(surf, (255, 220, 50), (center - 8, center - 5), 8)
        
    elif fruit_type == "melon":
        # Melon
        pygame.draw.circle(surf, (255, 228, 181), (center, center), center - 5)
        if size > 30:
            for i in range(6):
                angle = i * 60
                x = center + int((center - 8) * pygame.math.Vector2(1, 0).rotate(angle).x)
                y = center + int((center - 8) * pygame.math.Vector2(1, 0).rotate(angle).y)
                pygame.draw.line(surf, (210, 180, 140), (center, center), (x, y), 2)
                
    elif fruit_type == "myrtille":
        # Myrtille
        pygame.draw.circle(surf, (75, 0, 130), (center, center), center - 5)
        pygame.draw.circle(surf, (100, 50, 150), (center, center - 5), 5)
        
    elif fruit_type == "noix_de_coco":
        # Noix de coco
        pygame.draw.circle(surf, BROWN, (center, center), center - 5)
        pygame.draw.circle(surf, (160, 82, 45), (center, center), max(3, center - 10))
        for i in range(3):
            pygame.draw.circle(surf, (80, 40, 20), (center - 8 + i * 8, center), 3)
        
    elif fruit_type == "bombe":
        # Bombe noire avec mèche
        pygame.draw.circle(surf, (50, 50, 50), (center, center + 5), center - 8)
        pygame.draw.line(surf, BROWN, (center, 10), (center, center - 5), 4)
        pygame.draw.circle(surf, RED, (center, 8), 5)
        
    elif fruit_type == "ice block":
        # Glaçon bleu
        points = [(center, 5), (size - 10, center + 10), (center, size - 5), (10, center + 10)]
        pygame.draw.polygon(surf, ICE_BLUE, points)
        pygame.draw.polygon(surf, (150, 220, 255), points, 3)
        
    elif fruit_type == "spinner":
        # Shuriken
        for i in range(4):
            angle = i * 90
            points = [
                (center, center),
                (center + int(25 * pygame.math.Vector2(1, 0).rotate(angle).x),
                 center + int(25 * pygame.math.Vector2(1, 0).rotate(angle).y)),
                (center + int(25 * pygame.math.Vector2(1, 0).rotate(angle + 45).x),
                 center + int(25 * pygame.math.Vector2(1, 0).rotate(angle + 45).y))
            ]
            pygame.draw.polygon(surf, (192, 192, 192), points)
        pygame.draw.circle(surf, (100, 100, 100), (center, center), 8)
        
    elif fruit_type == "loto":
        # Ticket de loto
        pygame.draw.rect(surf, WHITE, (10, 15, size - 20, size - 30), border_radius=5)
        pygame.draw.rect(surf, PURPLE, (10, 15, size - 20, size - 30), 3, border_radius=5)
        if size > 30:
            font_mini = pygame.font.SysFont("Arial", 12, bold=True)
            loto_text = font_mini.render("LOTO", True, PURPLE)
            surf.blit(loto_text, (center - 15, center - 5))
        
    else:
        # Fruit générique coloré
        colors = [RED, ORANGE, YELLOW, GREEN, PURPLE, PINK]
        color = random.choice(colors)
        pygame.draw.circle(surf, color, (center, center), center - 5)
        pygame.draw.circle(surf, tuple(min(c + 50, 255) for c in color), (center - 8, center - 8), 8)
    
    return surf

# --- Créer les données d'images ---
FRUIT_TYPES = ["pomme", "banane", "orange", "pasteque", "fraise", "raisin", "cerise", 
               "citron", "kiwi", "ananas", "peche", "poire", "abricot", "framboise",
               "fruit_du_dragon", "mangue", "melon", "myrtille", "noix_de_coco",
               "bombe", "ice block", "spinner", "loto"]

IMG_DATA = {}
IMG_DATA_MINI = {}

for fruit_type in FRUIT_TYPES:
    IMG_DATA[fruit_type] = create_fruit_surface(fruit_type, 60)
    IMG_DATA_MINI[fruit_type] = create_fruit_surface(fruit_type, 15)

# Liste des fruits normaux (sans bombes ni power-ups)
FRUIT_NAMES = [k for k in IMG_DATA.keys() if k not in ["spinner", "bombe", "loto", "ice block"]]

# --- Classes Effets ---
class Particle:
    def __init__(self, x, y, fruit_type):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, -2)
        self.life = 255
        self.angle = random.randint(0, 360)
        self.rot_speed = random.randint(-15, 15)
        self.image = IMG_DATA_MINI[fruit_type]
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.life -= 8
        self.angle += self.rot_speed
        
    def draw(self, surf):
        if self.life > 0:
            temp_surf = self.image.copy()
            temp_surf.set_alpha(max(0, self.life))
            rotated = pygame.transform.rotate(temp_surf, self.angle)
            rect = rotated.get_rect(center=(self.x, self.y))
            surf.blit(rotated, rect.topleft)

class FruitSlice:
    def __init__(self, image, x, y, direction):
        w, h = image.get_size()
        self.image = pygame.Surface((w//2, h), pygame.SRCALPHA)
        self.image.blit(image, (0, 0), (0 if direction == "left" else w//2, 0, w//2, h))
        self.vx, self.x, self.y, self.vy, self.angle = (-6 if direction == "left" else 6), x, y, -8, 0
    def update(self): self.vy += 0.4; self.x += self.vx; self.y += self.vy; self.angle += 10
    def draw(self, surf):
        rot = pygame.transform.rotate(self.image, self.angle); surf.blit(rot, (self.x, self.y))

class GameObject:
    def __init__(self, speed_mult=1.0):
        self.is_enrobed = random.random() < 0.12 
        rand = random.random()
        if rand < 0.05: self.type = "loto"      
        elif rand < 0.10: self.type = "ice block"
        elif rand < 0.18: self.type = "spinner" 
        elif rand < 0.28: self.type = "bombe"   
        else: self.type = random.choice(FRUIT_NAMES)
        self.image_orig, self.letter = IMG_DATA[self.type], random.choice("abcdefghijklmnopqrstuvwxyz")
        self.x, self.y = random.randint(100, WIDTH - 100), HEIGHT + 20
        self.vy, self.vx = random.uniform(-14, -18) * speed_mult, random.uniform(-1.5, 1.5)
        self.angle, self.rot_speed, self.hp = 0, random.randint(-4, 4), (2 if self.is_enrobed else 1)
    def move(self): self.vy += 0.35; self.y += self.vy; self.x += self.vx; self.angle += self.rot_speed
    def draw(self, surf):
        if self.is_enrobed and self.hp > 0: pygame.draw.circle(surf, GOLD, (int(self.x + 30), int(self.y + 30)), 38, 3)
        rotated = pygame.transform.rotate(self.image_orig, self.angle)
        rect = rotated.get_rect(center=(self.x + 30, self.y + 30)); surf.blit(rotated, rect.topleft)
        color = PURPLE if self.type == "loto" else (ICE_BLUE if self.type == "ice block" else YELLOW)
        txt = font_letter.render(self.letter.upper(), True, color); surf.blit(txt, (self.x + 15, self.y + 60))

# --- Variables Globales ---
game_mode = "MENU"
current_sub_mode = "CLASSIC"
active_objects, slices, particles, slashes, found_words = [], [], [], [], []
score, vies, speed_multiplier, shake_amount = 0, 3, 1.0, 0
challenge_timer = 60 * 60
is_frozen, is_iced, freeze_timer, ice_timer, input_text = False, False, 0, 0, ""

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 900)

def reset_game(mode):
    global game_mode, current_sub_mode, score, vies, speed_multiplier, challenge_timer, active_objects, slices, particles, found_words, is_frozen, is_iced
    game_mode, current_sub_mode = "PLAY", mode
    score, vies, speed_multiplier, challenge_timer = 0, 3, 1.0, 60 * 60
    is_frozen = is_iced = False
    active_objects, slices, particles, found_words = [], [], [], []

# --- Boucle ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(DARK_BLUE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if game_mode == "MENU" and event.type == pygame.MOUSEBUTTONDOWN:
            if WIDTH//2 - 150 < mouse_pos[0] < WIDTH//2 + 150:
                if 250 < mouse_pos[1] < 310: reset_game("CLASSIC")
                elif 330 < mouse_pos[1] < 390: reset_game("CHALLENGE")

        if game_mode == "PLAY" and event.type == pygame.KEYDOWN:
            if is_frozen:
                if event.key == pygame.K_RETURN:
                    mot = input_text.upper().strip()
                    if mot in DICTIONNAIRE and mot not in found_words:
                        found_words.append(mot); score += 50
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE: input_text = input_text[:-1]
                elif len(input_text) < 12 and (event.unicode.isalpha() or event.unicode == "-"): input_text += event.unicode
            else:
                key = pygame.key.name(event.key).lower()
                for obj in active_objects[:]:
                    if obj.letter == key:
                        obj.hp -= 1
                        if obj.hp <= 0:
                            if obj.type == "loto": is_frozen, freeze_timer, input_text, found_words = True, 600, "", []
                            elif obj.type == "ice block": is_iced, ice_timer = True, 400
                            elif obj.type in ["spinner", "bombe"] or obj.is_enrobed:
                                if obj.type == "spinner": slashes.append({"start": (0, random.randint(100,500)), "end": (WIDTH, random.randint(100,500)), "life": 255})
                                if obj.type == "bombe": 
                                    if current_sub_mode == "CLASSIC": vies -= 1
                                    else: score = max(0, score - 50)
                                    shake_amount = 30
                                else:
                                    shake_amount = 15
                                    for o in active_objects[:]:
                                        if o.type != "bombe":
                                            slices.extend([FruitSlice(o.image_orig, o.x, o.y, "left"), FruitSlice(o.image_orig, o.x, o.y, "right")])
                                            score += 10; active_objects.remove(o)
                            else:
                                score += 10
                                slices.extend([FruitSlice(obj.image_orig, obj.x, obj.y, "left"), FruitSlice(obj.image_orig, obj.x, obj.y, "right")])
                                for _ in range(random.randint(6, 8)):
                                    particles.append(Particle(obj.x+30, obj.y+30, random.choice(FRUIT_NAMES)))
                            if obj in active_objects: active_objects.remove(obj)
                            speed_multiplier = 1.0 + (score // 600) * 0.1
                        break
        if event.type == SPAWN_EVENT and not is_frozen and game_mode == "PLAY": active_objects.append(GameObject(speed_multiplier))

    if game_mode == "PLAY":
        game_surf.fill(DARK_BLUE)
        
        # --- LOGIQUE DU TEMPS CORRIGÉE ---
        if is_frozen:
            freeze_timer -= 1
            is_frozen = (freeze_timer > 0)
        else:
            if is_iced:
                ice_timer -= 1
                if ice_timer <= 0: is_iced = False
            
            if current_sub_mode == "CHALLENGE":
                challenge_timer -= 1
                if challenge_timer <= 0: game_mode = "MENU"

        # Effets & Objets
        for p in particles[:]: p.update(); p.draw(game_surf); (particles.remove(p) if p.life <= 0 else None)
        for s in slices[:]: s.update(); s.draw(game_surf); (slices.remove(s) if s.y > HEIGHT + 100 else None)
        for sl in slashes[:]: pygame.draw.line(game_surf, WHITE, sl["start"], sl["end"], 10); sl["life"] -= 50; (slashes.remove(sl) if sl["life"] <= 0 else None)
        
        for obj in active_objects[:]:
            if not is_frozen:
                if is_iced: 
                    obj.y += obj.vy * 0.25; obj.x += obj.vx * 0.25
                else: 
                    obj.move()
            obj.draw(game_surf)
            if obj.y > HEIGHT + 100:
                if not is_iced and obj.type not in ["bombe", "loto", "ice block"] and current_sub_mode == "CLASSIC": vies -= 1
                active_objects.remove(obj)
        
        shake_off = [random.randint(-shake_amount, shake_amount), random.randint(-shake_amount, shake_amount)] if shake_amount > 0 else [0,0]
        shake_amount = max(0, shake_amount - 1); screen.blit(game_surf, shake_off)

        # Overlays
        if is_iced and not is_frozen:
            ice_ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); ice_ov.fill((100, 200, 255, 90)); screen.blit(ice_ov, (0,0))
            pygame.draw.rect(screen, WHITE, (0,0, WIDTH, HEIGHT), 8)

        if is_frozen:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); ov.fill((0, 0, 0, 210)); screen.blit(ov, (0,0))
            sec_loto = max(0, freeze_timer // 60 + 1)
            t_title = font_huge.render(f"LOTO: {sec_loto}s", True, GOLD)
            screen.blit(t_title, (WIDTH//2 - t_title.get_width()//2, 80))
            pygame.draw.rect(screen, PURPLE, (WIDTH//2 - 200, HEIGHT//2 - 30, 400, 60), 2, border_radius=15)
            t_in = font_huge.render(input_text.upper(), True, WHITE)
            screen.blit(t_in, (WIDTH//2 - t_in.get_width()//2, HEIGHT//2 - 22))
            if len(found_words) > 0:
                y_s = 150
                screen.blit(font_small.render("MOTS VALIDÉS :", True, YELLOW), (40, y_s))
                for i, m in enumerate(found_words[-10:]):
                    screen.blit(font_small.render(f"OK - {m}", True, GREEN), (45, y_s + 30 + i * 22))

        # HUD
        info = f"Score: {score} | " + (f"Vies: {vies}" if current_sub_mode == "CLASSIC" else f"Temps: {challenge_timer // 60}s")
        screen.blit(font_small.render(info, True, WHITE), (20, 20))
        if current_sub_mode == "CLASSIC" and vies <= 0: game_mode = "MENU"
        
    else: # MENU
        title = font_huge.render("FRUIT NINJA ULTIMATE", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        for i, text in enumerate(["CLASSIQUE", "CHALLENGE"]):
            rect = pygame.Rect(WIDTH//2 - 150, 250 + i*80, 300, 60)
            col = (GREEN if i==0 else RED) if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, col, rect, 2, border_radius=10)
            btn = font_huge.render(text, True, col)
            screen.blit(btn, (WIDTH//2 - btn.get_width()//2, 260 + i*80))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()