import pygame
import random

# --- Configuration ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_surf = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja Ultimate - Fast Edition")
clock = pygame.time.Clock()

# Couleurs
DARK_BLUE = (44, 62, 80)
YELLOW, RED, GREEN, WHITE = (
    (241, 196, 15),
    (231, 76, 60),
    (46, 204, 113),
    (255, 255, 255),
)
GOLD, ICE_BLUE = (255, 215, 0), (100, 200, 255)
ORANGE_ELECTR = (255, 165, 0)


def get_font(size):
    return pygame.font.SysFont(["impact", "arialblack", "arial"], size)


font_letter = get_font(35)
font_small = get_font(22)
font_huge = get_font(50)

# --- Images ---
IMAGES_LIST = {
    "abricot": "abricot.png",
    "ananas": "ananas.png",
    "banane": "banane.png",
    "bombe": "bombe.png",
    "cerise": "cerise.png",
    "citron": "citron.png",
    "fraise": "fraise.png",
    "framboise": "framboise.png",
    "fruit_du_dragon": "fruit_du_dragon.png",
    "ice block": "glaçon.png",
    "kiwi": "kiwi.png",
    "mangue": "mangue.png",
    "melon": "melon.png",
    "myrtille": "myrtille.png",
    "noix_de_coco": "noix_de_coco.png",
    "orange": "orange.png",
    "pasteque": "pasteque.png",
    "peche": "peche.png",
    "poire": "poire.png",
    "pomme": "pomme.png",
    "raisin": "raisin.png",
    "spinner": "shuriken.png",
    "eclair": "eclair.png",
}

IMG_DATA = {}
for name, filename in IMAGES_LIST.items():
    try:
        img = pygame.image.load(filename).convert_alpha()
        IMG_DATA[name] = pygame.transform.scale(img, (60, 60))
    except:
        surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        c = (
            ICE_BLUE
            if name == "ice block"
            else (ORANGE_ELECTR if name == "eclair" else GREEN)
        )
        pygame.draw.circle(surf, c, (30, 30), 25)
        IMG_DATA[name] = surf


# --- Classes ---
class Lightning:
    def __init__(self):
        self.points = []
        self.life = 10
        curr_pos = [random.randint(0, WIDTH), 0]
        self.points.append(curr_pos)
        while curr_pos[1] < HEIGHT:
            curr_pos = [
                curr_pos[0] + random.randint(-50, 50),
                curr_pos[1] + random.randint(20, 80),
            ]
            self.points.append(curr_pos)

    def draw(self, surf):
        if self.life > 0:
            pygame.draw.lines(surf, WHITE, False, self.points, 3)
            pygame.draw.lines(surf, ICE_BLUE, False, self.points, 1)
            self.life -= 1


class Particle:
    def __init__(self, x, y, color=WHITE):
        self.x, self.y, self.color = x, y, color
        self.vx, self.vy, self.life = random.uniform(-5, 5), random.uniform(-5, 5), 255

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 15

    def draw(self, surf):
        if self.life > 0:
            p = pygame.Surface((5, 5), pygame.SRCALPHA)
            p.fill((*self.color, self.life))
            surf.blit(p, (self.x, self.y))


class FruitSlice:
    def __init__(self, image, x, y, direction):
        w, h = image.get_size()
        self.image = pygame.Surface((w // 2, h), pygame.SRCALPHA)
        self.image.blit(
            image, (0, 0), (0 if direction == "left" else w // 2, 0, w // 2, h)
        )
        self.vx, self.x, self.y, self.vy, self.angle = (
            (-7 if direction == "left" else 7),
            x,
            y,
            -10,
            0,
        )

    def update(self):
        self.vy += 0.5
        self.x += self.vx
        self.y += self.vy
        self.angle += 12

    def draw(self, surf):
        rot = pygame.transform.rotate(self.image, self.angle)
        surf.blit(rot, (self.x, self.y))


class GameObject:
    def __init__(self, speed_mult=1.0):
        # Halo doré désactivé en surcharge
        self.is_enrobed = (random.random() < 0.15) if not is_overcharged else False

        # Sélection du type (Surcharge = uniquement fruits simples)
        if is_overcharged:
            self.type = random.choice(
                [
                    k
                    for k in IMG_DATA.keys()
                    if k not in ["bombe", "spinner", "ice block", "eclair"]
                ]
            )
        else:
            rand = random.random()
            if rand < 0.05:
                self.type = "ice block"
            elif rand < 0.10:
                self.type = "eclair"
            elif rand < 0.18:
                self.type = "spinner"
            elif rand < 0.28:
                self.type = "bombe"
            else:
                self.type = random.choice(
                    [
                        k
                        for k in IMG_DATA.keys()
                        if k not in ["spinner", "bombe", "ice block", "eclair"]
                    ]
                )
        # 1. On récupère l'image normalement
        self.image_orig = IMG_DATA[self.type]

        # 2. On définit si c'est un bonus ou un fruit simple
        self.is_bonus_type = self.type in ["bombe", "ice block", "eclair", "spinner"]

        # 3. Attribution de la lettre et de la couleur selon le type
        if self.is_bonus_type:
            self.letter = random.choice("awsd")
            self.color_label = RED  # Rouge
            # Optionnel : On peut forcer l'apparition à gauche pour aider le joueur
            self.x = random.randint(50, WIDTH // 2 - 50)
        else:
            self.letter = random.choice("jkl")
            self.color_label = GREEN  # Vert
            # Apparition à droite
            self.x = random.randint(WIDTH // 2 + 50, WIDTH - 100)

        # --- IMPORTANT : On sort du if/else pour définir y pour TOUT LE MONDE ---
        self.y = HEIGHT + 20

        # --- PROPULSION INITIALE ---
        self.vy, self.vx = random.uniform(-16, -21) * speed_mult, random.uniform(
            -1.5, 1.5
        )
        self.angle, self.rot_speed, self.hp = (
            0,
            random.randint(-4, 4),
            (2 if self.is_enrobed else 1),
        )

    def move(self, slow=False):
        # --- GESTION DU RALENTI (Bonus Glaçon) ---
        f = 0.3 if slow else 1.0

        # Application de la physique avec le facteur f
        self.vy += 0.35 * f  # Gravité
        self.y += self.vy * f
        self.x += self.vx * f
        self.angle += self.rot_speed * f

    def draw(self, surf):
        if self.is_enrobed and self.hp > 0:
            pygame.draw.circle(surf, GOLD, (int(self.x + 30), int(self.y + 30)), 42, 5)
        rotated = pygame.transform.rotate(self.image_orig, self.angle)
        rect = rotated.get_rect(center=(self.x + 30, self.y + 30))
        surf.blit(rotated, rect.topleft)
        color = (
            ICE_BLUE
            if self.type == "ice block"
            else (ORANGE_ELECTR if self.type == "eclair" else YELLOW)
        )
        shadow = font_letter.render(self.letter.upper(), True, (20, 20, 20))
        surf.blit(shadow, (self.x + 17, self.y + 62))
        txt = font_letter.render(self.letter.upper(), True, self.color_label)
        surf.blit(txt, (self.x + 15, self.y + 60))


def trigger_bonus_cut(color_p=WHITE):
    global score
    for o in active_objects[:]:
        if o.type != "bombe":
            slices.extend(
                [
                    FruitSlice(o.image_orig, o.x, o.y, "left"),
                    FruitSlice(o.image_orig, o.x, o.y, "right"),
                ]
            )
            score += 20 if is_overcharged else 10
            for _ in range(3):
                particles.append(Particle(o.x + 30, o.y + 30, color_p))
            active_objects.remove(o)


# --- Variables Globales ---
game_mode = "MENU"
current_sub_mode, score, vies = "CLASSIC", 0, 3
active_objects, slices, particles, slashes, lightnings = [], [], [], [], []
speed_multiplier, shake_amount, flash_timer = 1.0, 0, 0
challenge_timer, is_iced, ice_timer = 3600, False, 0
is_overcharged, overcharge_timer, grand_slash_gauge = False, 0, 0
MAX_GRAND_SLASH = 100

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 900)


def reset_game(mode):
    global game_mode, current_sub_mode, score, vies, speed_multiplier, challenge_timer, active_objects, slices, particles, slashes, flash_timer, is_overcharged, overcharge_timer, grand_slash_gauge, lightnings, is_iced
    game_mode, current_sub_mode = "PLAY", mode
    score, vies, speed_multiplier, challenge_timer, flash_timer = 0, 3, 1.0, 3600, 0
    is_iced = is_overcharged = False
    overcharge_timer = grand_slash_gauge = 0
    active_objects, slices, particles, slashes, lightnings = [], [], [], [], []


# --- Boucle ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(DARK_BLUE)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_mode == "MENU":
                if WIDTH // 2 - 150 < mouse_pos[0] < WIDTH // 2 + 150:
                    if 280 < mouse_pos[1] < 340:
                        reset_game("CLASSIC")
                    elif 370 < mouse_pos[1] < 430:
                        reset_game("CHALLENGE")
            elif game_mode == "PAUSE":
                if pygame.Rect(WIDTH // 2 - 150, 300, 300, 60).collidepoint(mouse_pos):
                    game_mode = "PLAY"
                elif pygame.Rect(WIDTH // 2 - 150, 380, 300, 60).collidepoint(
                    mouse_pos
                ):
                    game_mode = "MENU"
            elif game_mode == "GAMEOVER":
                if pygame.Rect(WIDTH // 2 - 150, 320, 300, 60).collidepoint(mouse_pos):
                    reset_game(current_sub_mode)
                elif pygame.Rect(WIDTH // 2 - 150, 410, 300, 60).collidepoint(
                    mouse_pos
                ):
                    game_mode = "MENU"

        if event.type == pygame.KEYDOWN:
            if game_mode == "PLAY":
                if event.key == pygame.K_ESCAPE:
                    game_mode = "PAUSE"
                else:
                    key = pygame.key.name(event.key).lower()
                    # 1. Définition des zones de touches
                    TOUCHES_BONUS = ["q", "s", "d", "f"]
                    TOUCHES_FRUITS = ["j", "k", "l", "m"]
                    if (
                        event.key == pygame.K_SPACE
                        and is_overcharged
                        and grand_slash_gauge >= MAX_GRAND_SLASH
                    ):
                        slashes.append(
                            {
                                "start": (0, HEIGHT // 2),
                                "end": (WIDTH, HEIGHT // 2),
                                "life": 255,
                            }
                        )
                        trigger_bonus_cut(ORANGE_ELECTR)
                        grand_slash_gauge = 0
                        shake_amount = 25

                    for obj in active_objects[:]:
                        est_bonus = obj.type in [
                            "ice block",
                            "eclair",
                            "spinner",
                            "bombe",
                        ]
                        # 2. Vérification de la correspondance Touche <-> Type d'objet
                        valide = False
                        if est_bonus and key in TOUCHES_BONUS:
                            valide = obj.letter == key
                        elif not est_bonus and key in TOUCHES_FRUITS:
                            valide = obj.letter == key
                        if (is_overcharged and event.unicode.isalpha()) or (
                            obj.letter == key
                        ):
                            obj.hp -= 1
                            if obj.hp <= 0:
                                if obj.is_enrobed:
                                    flash_timer, shake_amount, score = (
                                        10,
                                        25,
                                        score + (100 if is_overcharged else 50),
                                    )
                                    trigger_bonus_cut(GOLD)
                                elif obj.type == "eclair":
                                    is_overcharged, overcharge_timer = True, 300
                                elif obj.type == "spinner":
                                    slashes.append(
                                        {
                                            "start": (0, obj.y + 30),
                                            "end": (WIDTH, obj.y + 30),
                                            "life": 255,
                                        }
                                    )
                                    trigger_bonus_cut(WHITE)
                                elif obj.type == "ice block":
                                    is_iced, ice_timer = True, 400
                                elif obj.type == "bombe":
                                    if current_sub_mode == "CLASSIC":
                                        vies -= 1
                                    else:
                                        score = max(0, score - 50)
                                    shake_amount = 30
                                else:
                                    score += 20 if is_overcharged else 10
                                    if is_overcharged:
                                        grand_slash_gauge = min(
                                            MAX_GRAND_SLASH, grand_slash_gauge + 10
                                        )
                                    slices.extend(
                                        [
                                            FruitSlice(
                                                obj.image_orig, obj.x, obj.y, "left"
                                            ),
                                            FruitSlice(
                                                obj.image_orig, obj.x, obj.y, "right"
                                            ),
                                        ]
                                    )
                                    for _ in range(4):
                                        particles.append(
                                            Particle(obj.x + 30, obj.y + 30)
                                        )
                                if obj in active_objects:
                                    active_objects.remove(obj)
                            break
            elif game_mode == "PAUSE" and event.key == pygame.K_ESCAPE:
                game_mode = "PLAY"

        # SPAWN SEULEMENT EN MODE PLAY
        if event.type == SPAWN_EVENT and game_mode == "PLAY":
            # 1. Calcul de la quantité de fruits selon le score (Max 4 en normal)
            nb_fruits = 1 + (score // 1000)
            if nb_fruits > 4:
                nb_fruits = 4

            # En surcharge, on double la mise !
            count = 6 if is_overcharged else nb_fruits

            for _ in range(count):
                active_objects.append(GameObject(speed_multiplier))

            # 2. Accélération du rythme de spawn selon le score
            # Plus le score est haut, plus le délai diminue (min 400ms)
            delai_normal = max(400, 900 - (score // 10))
            delai = 300 if is_overcharged else delai_normal

            pygame.time.set_timer(SPAWN_EVENT, delai)

    # --- Logique et Rendu ---
    if game_mode in ["PLAY", "PAUSE"]:
        if game_mode == "PLAY":
            # Mise à jour des timers uniquement si on joue
            if is_iced:
                ice_timer -= 1
                is_iced = ice_timer > 0
            if is_overcharged:
                overcharge_timer -= 1
                if overcharge_timer <= 0:
                    is_overcharged = False
                    slashes.append(
                        {
                            "start": (0, HEIGHT // 2),
                            "end": (WIDTH, HEIGHT // 2),
                            "life": 255,
                        }
                    )
                    trigger_bonus_cut(ORANGE_ELECTR)
                    shake_amount = 25
                else:
                    if random.random() < 0.2:
                        lightnings.append(Lightning())
            if current_sub_mode == "CHALLENGE":
                challenge_timer -= 1
                if challenge_timer <= 0:
                    game_mode = "GAMEOVER"

            # Mise à jour des objets
            for p in particles[:]:
                p.update()
                (particles.remove(p) if p.life <= 0 else None)
            for s in slices[:]:
                s.update()
                (slices.remove(s) if s.y > HEIGHT + 100 else None)
            for obj in active_objects[:]:
                obj.move(slow=is_iced)
                if obj.y > HEIGHT + 100:
                    if not is_iced and not is_overcharged:
                        if (
                            obj.type not in ["bombe", "ice block", "eclair"]
                            and current_sub_mode == "CLASSIC"
                        ):
                            vies -= 1
                    active_objects.remove(obj)
            for sl in slashes[:]:
                sl["life"] -= 50
                (slashes.remove(sl) if sl["life"] <= 0 else None)

        # RENDU (toujours actif pour voir le jeu en arrière-plan de la pause)
        game_surf.fill(DARK_BLUE)
        for p in particles:
            p.draw(game_surf)
        for s in slices:
            s.draw(game_surf)
        for l in lightnings:
            l.draw(game_surf)
        for obj in active_objects:
            obj.draw(game_surf)
        for sl in slashes:
            pygame.draw.line(game_surf, WHITE, sl["start"], sl["end"], 15)

        off = (
            [
                random.randint(-shake_amount, shake_amount),
                random.randint(-shake_amount, shake_amount),
            ]
            if shake_amount > 0
            else [0, 0]
        )
        if game_mode == "PLAY":
            shake_amount = max(0, shake_amount - 1)
        screen.blit(game_surf, off)

        # Overlays Visuels
        if is_overcharged:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((255, 165, 0, 40))
            screen.blit(ov, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), (WIDTH - 220, 20, 200, 20))
            bar_col = ORANGE_ELECTR if grand_slash_gauge >= MAX_GRAND_SLASH else WHITE
            pygame.draw.rect(
                screen,
                bar_col,
                (WIDTH - 220, 20, (grand_slash_gauge / MAX_GRAND_SLASH) * 200, 20),
            )
            screen.blit(
                font_small.render("GRAND SLASH (ESPACE)", True, bar_col),
                (WIDTH - 220, 45),
            )

        if is_iced:
            ice_ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ice_ov.fill((100, 200, 255, 60))
            screen.blit(ice_ov, (0, 0))

        screen.blit(
            font_small.render(
                f"SCORE: {score} | "
                + (
                    f"VIES: {vies}"
                    if current_sub_mode == "CLASSIC"
                    else f"TPS: {challenge_timer//60}s"
                ),
                True,
                WHITE,
            ),
            (20, 20),
        )

        if game_mode == "PAUSE":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            txt = font_huge.render("PAUSE", True, YELLOW)
            screen.blit(txt, txt.get_rect(center=(WIDTH // 2, 200)))
            for i, t in enumerate(["REPRENDRE", "MENU"]):
                rect = pygame.Rect(WIDTH // 2 - 150, 300 + i * 80, 300, 60)
                col = YELLOW if rect.collidepoint(mouse_pos) else WHITE
                pygame.draw.rect(screen, col, rect, 2, border_radius=10)
                btn = font_small.render(t, True, col)
                screen.blit(btn, btn.get_rect(center=rect.center))

        if current_sub_mode == "CLASSIC" and vies <= 0:
            game_mode = "GAMEOVER"

    elif game_mode == "GAMEOVER":
        txt = font_huge.render("PARTIE TERMINEE", True, RED)
        screen.blit(txt, txt.get_rect(center=(WIDTH // 2, 120)))
        score_txt = font_small.render(f"SCORE FINAL : {score}", True, WHITE)
        screen.blit(score_txt, score_txt.get_rect(center=(WIDTH // 2, 200)))
        for i, t in enumerate(["RECOMMENCER", "MENU"]):
            rect = pygame.Rect(WIDTH // 2 - 150, 320 + i * 90, 300, 60)
            col = YELLOW if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, col, rect, 2, border_radius=10)
            btn = font_small.render(t, True, col)
            screen.blit(btn, btn.get_rect(center=rect.center))
    else:
        txt = font_huge.render("FRUIT NINJA ULTIMATE", True, WHITE)
        screen.blit(txt, txt.get_rect(center=(WIDTH // 2, 150)))

        # --- NOUVEAU : TITRE ET RAPPEL DES COMMANDES ---
        # Titre central
        cmd_title = font_small.render("COMMANDES EN JEU :", True, WHITE)
        screen.blit(cmd_title, cmd_title.get_rect(center=(WIDTH // 2, 485)))

        # Encadré Gauche (Bonus/Danger)
        pygame.draw.rect(
            screen, (255, 80, 80), (WIDTH // 2 - 250, 520, 200, 50), 2, border_radius=10
        )
        lbl_l = font_small.render("BONUS : A W S D", True, (255, 80, 80))
        screen.blit(lbl_l, lbl_l.get_rect(center=(WIDTH // 2 - 150, 542)))

        # Encadré Droite (Fruits)
        pygame.draw.rect(
            screen, (80, 255, 80), (WIDTH // 2 + 50, 520, 200, 50), 2, border_radius=10
        )
        lbl_r = font_small.render("FRUITS : J K L", True, (80, 255, 80))
        screen.blit(lbl_r, lbl_r.get_rect(center=(WIDTH // 2 + 150, 542)))

        for i, t in enumerate(["CLASSIQUE", "CHALLENGE"]):
            rect = pygame.Rect(WIDTH // 2 - 150, 280 + i * 90, 300, 60)
            col = (GREEN if i == 0 else RED) if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, col, rect, 2, border_radius=10)
            btn = font_huge.render(t, True, col)
            screen.blit(btn, btn.get_rect(center=rect.center))
        # --- 1. INDICATEURS DE ZONES (HUD) ---
        if game_mode == "PLAY":
            # Rappel Main Gauche (Rouge)
            txt_l = font_small.render("GAUCHE : [ Q S D F ]", True, (255, 80, 80))
            screen.blit(txt_l, (20, HEIGHT - 50))

            # Rappel Main Droite (Vert)
            txt_r = font_small.render("[ J K L M ] : DROITE", True, (80, 255, 80))
            screen.blit(txt_r, (WIDTH - txt_r.get_width() - 20, HEIGHT - 50))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
