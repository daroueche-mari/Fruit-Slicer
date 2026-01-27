import pygame
import random

# --- Configuration ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Typing - Pure Gameplay")
clock = pygame.time.Clock()

# Couleurs et Police
DARK_BLUE, YELLOW, RED, GREEN = (44, 62, 80), (241, 196, 15), (231, 76, 60), (46, 204, 113)
font_letter = pygame.font.SysFont("Arial", 32, bold=True)

# --- Chargement des Images ---
IMAGES_LIST = ['banane', 'fraise', 'kiwi', 'pasteque', 'pomme', 'bombe', 'bonus_etoile', 'piege_etoile']
IMG_DATA = {}
for name in IMAGES_LIST:
    try:
        img = pygame.image.load(f"{name}.png").convert_alpha()
        IMG_DATA[name] = pygame.transform.scale(img, (60, 60))
    except:
        surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(surf, RED if name == 'bombe' else GREEN, (30, 30), 25)
        IMG_DATA[name] = surf

# --- Classe Objet ---
class GameObject:
    def __init__(self, speed):
        self.type = random.choice(list(IMG_DATA.keys()))
        self.image = IMG_DATA[self.type]
        self.letter = random.choice("abcdefghijklmnopqrstuvwxyz")
        self.x, self.y = random.randint(50, WIDTH - 70), -70
        self.speed = random.uniform(speed, speed + 2)

    def move(self): 
        self.y += self.speed

    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))
        color = RED if self.type == 'bombe' else YELLOW
        txt = font_letter.render(self.letter.upper(), True, color)
        surf.blit(txt, (self.x + 18, self.y + 60))

# Variables de session
active_objects = []
difficulty_speed = 3.0
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1000)

# --- Boucle Principale ---
running = True
while running:
    screen.fill(DARK_BLUE)
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == SPAWN_EVENT:
            active_objects.append(GameObject(difficulty_speed))
            
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key).lower()
            
            for obj in active_objects[:]:
                if obj.letter == key:
                    # Logique simplifiée sans score
                    if obj.type == 'bombe':
                        running = False # Défaite immédiate
                    elif obj.type == 'bonus_etoile':
                        active_objects = [o for o in active_objects if o.type == 'bombe']
                    elif obj.type == 'piege_etoile':
                        if any(o.type == 'bombe' for o in active_objects):
                            running = False # Défaite si bombe présente
                        else:
                            active_objects = [] # Nettoyage si tout va bien
                    
                    if obj in active_objects: 
                        active_objects.remove(obj)
                    break

    # Mise à jour et dessin
    for obj in active_objects[:]:
        obj.move()
        obj.draw(screen)
        if obj.y > HEIGHT:
            active_objects.remove(obj)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()