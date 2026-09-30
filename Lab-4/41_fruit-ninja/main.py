import pygame
import sys
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slice - Pygame Version")

# Colors
DARK_BLUE = (20, 25, 45)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game engine instance
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                engine.handle_event(event)

        engine.update()

        SCREEN.fill(DARK_BLUE)
        engine.draw(SCREEN)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
