"""
Runnable demonstration of the original broken game behavior for the 'before' video.
Bugs demonstrated:
1. Fast swipes pass right through fruits without slicing them (tunneling).
2. No Game Over screen when lives run out or bomb is hit (only terminal print).
3. No replay or difficulty selection options.
4. No sound effects.
"""
import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 700, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slice - Broken Version (Before Fixes)")
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
DARK_BLUE = (20, 25, 45)
BOMB_BLACK = (30, 30, 30)
try:
    font = pygame.font.SysFont("Arial", 28)
except Exception:
    font = pygame.font.Font(None, 28)

class NaiveFruit:
    def __init__(self, x, y, vx, vy, gravity, radius=28, kind="fruit"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.gravity = gravity
        self.radius = radius
        self.kind = kind
        self.sliced = False
        self.color = BOMB_BLACK if kind == "bomb" else random.choice(FRUIT_COLORS)

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

    def contains_point(self, px, py):
        # BUG: Only checks discrete mouse point at the current frame!
        # Fast swipes skip right over the circle between frames!
        return (self.x - px) ** 2 + (self.y - py) ** 2 <= self.radius ** 2

fruits = []
score = 0
lives = 3
spawn_timer = 0
trail = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            trail.append(event.pos)
            if len(trail) > 10:
                trail.pop(0)
            # Naive point check on mouse motion
            for f in fruits:
                if not f.sliced and f.contains_point(event.pos[0], event.pos[1]):
                    if f.kind == "bomb":
                        print("BUGGY GAME OVER: Hit a bomb! (Console only, no UI screen)")
                        running = False
                    else:
                        f.sliced = True
                        score += 1

    # Spawn
    spawn_timer += 1
    if spawn_timer >= 55:
        x = random.randint(60, WIDTH - 60)
        vy = -random.uniform(13, 16)
        vx = random.uniform(-2, 2)
        kind = "bomb" if random.random() < 0.15 else "fruit"
        fruits.append(NaiveFruit(x, HEIGHT + 30, vx, vy, 0.35, kind=kind))
        spawn_timer = 0

    # Update
    for f in fruits:
        f.update()
        if not f.sliced and f.kind == "fruit" and f.y > HEIGHT + 40 and f.vy > 0:
            lives -= 1
            if lives <= 0:
                print("BUGGY GAME OVER: Out of lives! (Console only, no UI screen)")
                running = False

    fruits = [f for f in fruits if f.y <= HEIGHT + 50]

    # Draw
    SCREEN.fill(DARK_BLUE)
    for f in fruits:
        if not f.sliced:
            pygame.draw.circle(SCREEN, f.color, (int(f.x), int(f.y)), f.radius)

    # Simple blade line
    if len(trail) > 1:
        pygame.draw.lines(SCREEN, WHITE, False, trail, 3)

    # Score and lives text
    s_surf = font.render(f"Score: {score}  Lives: {lives}", True, WHITE)
    SCREEN.blit(s_surf, (20, 20))
    info_surf = font.render("(Buggy: Fast swipes miss fruit & ends without screen)", True, (255, 180, 180))
    SCREEN.blit(info_surf, (20, 60))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
