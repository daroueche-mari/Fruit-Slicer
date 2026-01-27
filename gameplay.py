import pygame
import random
import os

# --- Configuration ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_surf = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja Ultimate - Pause Edition")
clock = pygame.time.Clock()

# Couleurs
DARK_BLUE = (44, 62, 80)
YELLOW, RED, GREEN, WHITE = (241, 196, 15), (231, 76, 60), (46, 204, 113), (255, 255, 255)
GOLD, PURPLE, ICE_BLUE = (255, 215, 0), (155, 89, 182), (100, 200, 255)

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

# --- Images ---
IMAGES_LIST = {
    "abricot": "abricot.png", "ananas": "ananas.png", "banane": "banane.png",
    "bombe": "bombe.png", "cerise": "cerise.png", "citron": "citron.png", 
    "fraise": "fraise.png", "framboise": "framboise.png", "fruit_du_dragon": "fruit_du_dragon.png",
    "ice block": "glaçon.png", "kiwi": "kiwi.png", "mangue": "mangue.png",
    "melon": "melon.png", "myrtille": "myrtille.png", "noix_de_coco": "noix_de_coco.png",
    "orange": "orange.png", "pasteque": "pasteque.png", "peche": "peche.png",
    "poire": "poire.png", "pomme": "pomme.png", "raisin": "raisin.png",
    "spinner": "shuriken.png", "loto": "loto.png"
}

IMG_DATA = {}
for name, filename in IMAGES_LIST.items():
    try:
        img = pygame.image.load(filename).convert_alpha()
        IMG_DATA[name] = pygame.transform.scale(img, (60, 60))
    except:
        surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        c = PURPLE if name == "loto" else (ICE_BLUE if name == "ice block" else GREEN)
        pygame.draw.circle(surf, c, (30, 30), 25)
        IMG_DATA[name] = surf

# --- Classes ---
class Particle:
    def __init__(self, x, y):
        self.x, self.y, self.vx, self.vy, self.life = x, y, random.uniform(-4, 4), random.uniform(-4, 4), 255
    def update(self): self.x += self.vx; self.y += self.vy; self.life -= 15
    def draw(self, surf):
        if self.life > 0:
            p = pygame.Surface((4, 4), pygame.SRCALPHA); p.fill((255, 255, 255, self.life)); surf.blit(p, (self.x, self.y))

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
        else: self.type = random.choice([k for k in IMG_DATA.keys() if k not in ["spinner", "bombe", "loto", "ice block"]])
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
game_mode = "MENU" # MENU, PLAY, GAMEOVER, PAUSE
current_sub_mode = "CLASSIC"
active_objects, slices, particles, slashes, found_words = [], [], [], [], []
score, high_score, vies, speed_multiplier, shake_amount = 0, 0, 3, 1.0, 0
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
        
        # CLIC SOURIS (MENUS)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_mode == "MENU":
                if WIDTH//2 - 150 < mouse_pos[0] < WIDTH//2 + 150:
                    if 250 < mouse_pos[1] < 310: reset_game("CLASSIC")
                    elif 330 < mouse_pos[1] < 390: reset_game("CHALLENGE")
            
            elif game_mode == "GAMEOVER":
                if WIDTH//2 - 150 < mouse_pos[0] < WIDTH//2 + 150:
                    if 300 < mouse_pos[1] < 360: reset_game(current_sub_mode)
                    elif 380 < mouse_pos[1] < 440: game_mode = "MENU"
            
            elif game_mode == "PAUSE":
                if WIDTH//2 - 150 < mouse_pos[0] < WIDTH//2 + 150:
                    if 300 < mouse_pos[1] < 360: game_mode = "PLAY" # Reprendre
                    elif 380 < mouse_pos[1] < 440: game_mode = "MENU" # Quitter vers Menu

        # CLAVIER
        if event.type == pygame.KEYDOWN:
            if game_mode == "PLAY":
                if event.key == pygame.K_ESCAPE:
                    game_mode = "PAUSE" # Activer la pause
                elif is_frozen:
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
                                    score += 10; slices.extend([FruitSlice(obj.image_orig, obj.x, obj.y, "left"), FruitSlice(obj.image_orig, obj.x, obj.y, "right")])
                                    for _ in range(4): particles.append(Particle(obj.x+30, obj.y+30))
                                if obj in active_objects: active_objects.remove(obj)
                                speed_multiplier = 1.0 + (score // 600) * 0.1
                                if score > high_score: high_score = score
                            break
            elif game_mode == "PAUSE" and event.key == pygame.K_ESCAPE:
                game_mode = "PLAY" # Sortir de pause avec Echap aussi
        
        if event.type == SPAWN_EVENT and not is_frozen and game_mode == "PLAY": 
            active_objects.append(GameObject(speed_multiplier))

    # --- ÉTATS DU JEU ---
    if game_mode == "PLAY":
        game_surf.fill(DARK_BLUE)
        if is_frozen:
            freeze_timer -= 1
            is_frozen = (freeze_timer > 0)
        else:
            if is_iced:
                ice_timer -= 1
                if ice_timer <= 0: is_iced = False
            if current_sub_mode == "CHALLENGE":
                challenge_timer -= 1
                if challenge_timer <= 0: game_mode = "GAMEOVER"

        for p in particles[:]: p.update(); p.draw(game_surf); (particles.remove(p) if p.life <= 0 else None)
        for s in slices[:]: s.update(); s.draw(game_surf); (slices.remove(s) if s.y > HEIGHT + 100 else None)
        for sl in slashes[:]: pygame.draw.line(game_surf, WHITE, sl["start"], sl["end"], 10); sl["life"] -= 50; (slashes.remove(sl) if sl["life"] <= 0 else None)
        for obj in active_objects[:]:
            if not is_frozen:
                if is_iced: obj.y += obj.vy * 0.25; obj.x += obj.vx * 0.25
                else: obj.move()
            obj.draw(game_surf)
            if obj.y > HEIGHT + 100:
                if not is_iced and obj.type not in ["bombe", "loto", "ice block"] and current_sub_mode == "CLASSIC": vies -= 1
                active_objects.remove(obj)
        
        shake_off = [random.randint(-shake_amount, shake_amount), random.randint(-shake_amount, shake_amount)] if shake_amount > 0 else [0,0]
        shake_amount = max(0, shake_amount - 1); screen.blit(game_surf, shake_off)

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

        info = f"Score: {score} | " + (f"Vies: {vies}" if current_sub_mode == "CLASSIC" else f"Temps: {challenge_timer // 60}s")
        screen.blit(font_small.render(info, True, WHITE), (20, 20))
        if current_sub_mode == "CLASSIC" and vies <= 0: game_mode = "GAMEOVER"

    elif game_mode == "PAUSE":
        # On affiche le jeu en fond mais assombri
        screen.blit(game_surf, (0,0))
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA); ov.fill((0, 0, 0, 150)); screen.blit(ov, (0,0))
        
        title = font_huge.render("PAUSE", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
        sub = font_small.render("Voulez-vous quitter la partie ?", True, WHITE)
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 220))

        for i, text in enumerate(["REPRENDRE", "QUITTER"]):
            rect = pygame.Rect(WIDTH//2 - 150, 300 + i*80, 300, 60)
            col = YELLOW if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, col, rect, 2, border_radius=10)
            btn = font_huge.render(text, True, col)
            screen.blit(btn, btn.get_rect(center=rect.center))

    elif game_mode == "GAMEOVER":
        title = font_huge.render("PARTIE TERMINÉE", True, RED)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        score_txt = font_huge.render(f"SCORE FINAL: {score}", True, WHITE)
        screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, 180))
        best_txt = font_small.render(f"MEILLEUR SCORE: {high_score}", True, GOLD)
        screen.blit(best_txt, (WIDTH//2 - best_txt.get_width()//2, 230))
        for i, text in enumerate(["RECOMMENCER", "MENU"]):
            rect = pygame.Rect(WIDTH//2 - 150, 300 + i*80, 300, 60)
            col = YELLOW if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, col, rect, 2, border_radius=10)
            btn_font = font_letter if text == "RECOMMENCER" else font_huge
            btn = btn_font.render(text, True, col)
            screen.blit(btn, btn.get_rect(center=rect.center))

    else: # MENU
        title = font_huge.render("FRUIT NINJA ULTIMATE", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        for i, text in enumerate(["CLASSIQUE", "CHALLENGE"]):
            rect = pygame.Rect(WIDTH//2 - 150, 250 + i*80, 300, 60)
            col = (GREEN if i==0 else RED) if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, col, rect, 2, border_radius=10)
            btn = font_huge.render(text, True, col)
            screen.blit(btn, btn.get_rect(center=rect.center))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()