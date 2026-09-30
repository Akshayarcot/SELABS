import os
import pygame
import random
import time
from .fruit import Fruit
from .audio import ensure_sound_effects

WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (235, 60, 60)
GREEN = (70, 200, 90)
DARK_BLUE = (20, 25, 45)
OVERLAY_BG = (15, 18, 30, 215)
BLADE_COLOR = (240, 248, 255)
BLADE_GLOW = (120, 180, 255)

DIFFICULTIES = {
    "Easy": {
        "spawn_interval": 70,
        "bomb_chance": 0.08,
        "speed_scale": 0.85,
        "label": "Easy"
    },
    "Medium": {
        "spawn_interval": 52,
        "bomb_chance": 0.16,
        "speed_scale": 1.0,
        "label": "Medium"
    },
    "Hard": {
        "spawn_interval": 36,
        "bomb_chance": 0.28,
        "speed_scale": 1.25,
        "label": "Hard"
    }
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.fruits = []
        # Trail stores tuples of ((x, y), timestamp)
        self.trail = []
        self.last_pos = None

        self.lives = 3
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.game_over_reason = ""

        # Difficulty setting (Task 3)
        self.current_difficulty = "Medium"
        self._apply_difficulty(self.current_difficulty)
        self._spawn_timer = 0

        # Fonts with safe fallback (avoids macOS permission errors on ~/Library/Fonts)
        self.font_score = self._load_font("Helvetica", 28, bold=True)
        self.font_title = self._load_font("Helvetica", 54, bold=True)
        self.font_subtitle = self._load_font("Helvetica", 24)
        self.font_button = self._load_font("Helvetica", 20, bold=True)

        # Sound effects (Task 4)
        self.sound_enabled = False
        self.sound_slice = None
        self.sound_bomb = None
        self.sound_game_over = None
        self._init_sounds()

        # Replay buttons rects for mouse interaction (Task 3)
        self.replay_buttons = {}

    def _load_font(self, name, size, bold=False):
        """Safely loads SysFont with fallback to built-in Font to avoid permission issues."""
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            f = pygame.font.Font(None, size)
            f.set_bold(bold)
            return f

    def _init_sounds(self):
        """Initializes mixer and synthesizes/loads sound effects."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            
            sounds_dir = os.path.join(os.path.dirname(__file__), "..", "sounds")
            slice_path, bomb_path, game_over_path = ensure_sound_effects(sounds_dir)

            self.sound_slice = pygame.mixer.Sound(slice_path)
            self.sound_bomb = pygame.mixer.Sound(bomb_path)
            self.sound_game_over = pygame.mixer.Sound(game_over_path)

            self.sound_slice.set_volume(0.65)
            self.sound_bomb.set_volume(0.85)
            self.sound_game_over.set_volume(0.75)
            self.sound_enabled = True
        except Exception as e:
            # Graceful fallback if audio hardware is absent/headless
            print(f"[Audio Warning] Sound system initialized in silent mode: {e}")
            self.sound_enabled = False

    def play_sound(self, sound):
        if self.sound_enabled and sound is not None:
            try:
                sound.play()
            except Exception:
                pass

    def _apply_difficulty(self, diff_name):
        cfg = DIFFICULTIES.get(diff_name, DIFFICULTIES["Medium"])
        self.current_difficulty = diff_name
        self.spawn_interval = cfg["spawn_interval"]
        self.bomb_chance = cfg["bomb_chance"]
        self.speed_scale = cfg["speed_scale"]

    def reset_game(self, difficulty=None):
        """Task 3: Resets game state and applies selected difficulty."""
        if difficulty is not None and difficulty in DIFFICULTIES:
            self._apply_difficulty(difficulty)

        self.fruits.clear()
        self.trail.clear()
        self.last_pos = None
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.game_over_reason = ""
        self._spawn_timer = 0

    def spawn_fruit(self):
        """Spawns 1 to 2 items with randomized trajectory arc."""
        count = 1 if random.random() < 0.7 else 2
        for _ in range(count):
            x = random.randint(70, self.width - 70)
            vy = -random.uniform(13.5, 16.5) * self.speed_scale
            # Angle towards the center
            center_drift = (self.width / 2.0 - x) / (self.width / 2.0)
            vx = random.uniform(0.5, 2.5) * center_drift
            gravity = 0.38
            kind = "bomb" if random.random() < self.bomb_chance else "fruit"

            fruit = Fruit(x, self.height + 35, vx, vy, gravity, kind=kind)
            self.fruits.append(fruit)

    def handle_event(self, event):
        """Processes player inputs: mouse movement swipe detection and UI button clicks."""
        now = time.time()

        if event.type == pygame.MOUSEMOTION:
            curr_pos = event.pos
            self.trail.append((curr_pos, now))

            if self.last_pos is not None and not self.game_over:
                self._check_swipe_collision(self.last_pos, curr_pos)
            self.last_pos = curr_pos

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            curr_pos = event.pos
            self.last_pos = curr_pos
            self.trail.append((curr_pos, now))

            if self.game_over:
                # Check button clicks on Game Over screen
                for diff_key, rect in self.replay_buttons.items():
                    if rect.collidepoint(curr_pos):
                        if diff_key == "Quit":
                            pygame.event.post(pygame.event.Event(pygame.QUIT))
                        else:
                            self.reset_game(diff_key)
                        return

        elif event.type == pygame.KEYDOWN:
            if self.game_over:
                # Key bindings for replay options (Task 3)
                if event.key in (pygame.K_1, pygame.K_e):
                    self.reset_game("Easy")
                elif event.key in (pygame.K_2, pygame.K_m):
                    self.reset_game("Medium")
                elif event.key in (pygame.K_3, pygame.K_h):
                    self.reset_game("Hard")
                elif event.key == pygame.K_r:
                    self.reset_game(self.current_difficulty)
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

    def _check_swipe_collision(self, p1, p2):
        """
        Task 1: Continuous swipe collision check against all active fruits.
        Uses line-segment intersection with fruit hitboxes.
        """
        swipe_dir = (p2[0] - p1[0], p2[1] - p1[1])

        for fruit in self.fruits:
            if not fruit.sliced and fruit.intersects_segment(p1, p2):
                if fruit.kind == "bomb":
                    # Task 2: Trigger game over on bomb hit
                    fruit.slice(swipe_dir)
                    self.play_sound(self.sound_bomb)
                    self._trigger_game_over("Sliced a Bomb!")
                    break
                else:
                    # Slice fruit successfully
                    fruit.slice(swipe_dir)
                    self.score += 1
                    if self.score > self.high_score:
                        self.high_score = self.score
                    self.play_sound(self.sound_slice)

    def _trigger_game_over(self, reason):
        """Task 2 & 4: Sets game over state and plays game over sound."""
        if not self.game_over:
            self.game_over = True
            self.game_over_reason = reason
            self.play_sound(self.sound_game_over)

    def update(self):
        """Advances physics, fruit spawns, trail pruning, and checks dropped fruits."""
        now = time.time()
        # Retain blade trail for 0.18 seconds
        self.trail = [(pos, t) for (pos, t) in self.trail if now - t < 0.18]

        if not self.game_over:
            self._spawn_timer += 1
            if self._spawn_timer >= self.spawn_interval:
                self.spawn_fruit()
                self._spawn_timer = 0

            # Update all fruits and check bottom boundary
            for fruit in self.fruits:
                fruit.update()
                # Missed fruit penalty: unsliced fruit falling below screen
                if not fruit.sliced and fruit.kind == "fruit" and fruit.is_off_screen(self.height):
                    self.lives -= 1
                    if self.lives <= 0:
                        self._trigger_game_over("Out of Lives! (Fruits Missed)")

            # Purge fruits that have fully left screen
            self.fruits = [f for f in self.fruits if not f.is_off_screen(self.height)]
        else:
            # Let sliced fragments fall naturally during game over
            for fruit in self.fruits:
                if fruit.sliced:
                    fruit.update()
            self.fruits = [f for f in self.fruits if not f.is_off_screen(self.height)]

    def draw(self, surface):
        """Renders game world, katana trail, HUD, and Game Over screen."""
        # 1. Draw all fruits / bombs
        for fruit in self.fruits:
            fruit.draw(surface)

        # 2. Draw blade swipe trail
        self._draw_blade_trail(surface)

        # 3. Draw HUD (Score, High Score, Difficulty, Lives)
        self._draw_hud(surface)

        # 4. Draw Game Over screen (Task 2 & 3)
        if self.game_over:
            self._draw_game_over(surface)

    def _draw_blade_trail(self, surface):
        """Renders anti-aliased glowing blade swipe trail with fading width."""
        if len(self.trail) < 2:
            return

        now = time.time()
        points = [p[0] for p in self.trail]
        num_pts = len(points)

        for i in range(num_pts - 1):
            p1 = points[i]
            p2 = points[i + 1]
            progress = (i + 1) / float(num_pts)
            glow_width = max(1, int(progress * 6))
            core_width = max(1, int(progress * 3))

            # Outer blade glow
            pygame.draw.line(surface, BLADE_GLOW, p1, p2, glow_width + 2)
            # Inner bright white edge
            pygame.draw.line(surface, BLADE_COLOR, p1, p2, core_width)

    def _draw_hud(self, surface):
        """Renders scores, difficulty badge, and hearts for lives."""
        # Score
        score_surf = self.font_score.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_surf, (20, 16))

        # High Score
        hi_surf = self.font_subtitle.render(f"Best: {self.high_score}", True, GOLD)
        surface.blit(hi_surf, (20, 50))

        # Difficulty Badge
        diff_text = f"[{self.current_difficulty}]"
        diff_surf = self.font_subtitle.render(diff_text, True, (170, 200, 240))
        diff_rect = diff_surf.get_rect(center=(self.width // 2, 28))
        surface.blit(diff_surf, diff_rect)

        # Lives (rendered as hearts)
        for i in range(3):
            heart_x = self.width - 35 - (i * 30)
            heart_y = 28
            color = RED if i < self.lives else (70, 75, 90)
            # Draw heart icon using circles and triangle
            pygame.draw.circle(surface, color, (heart_x - 5, heart_y - 3), 6)
            pygame.draw.circle(surface, color, (heart_x + 5, heart_y - 3), 6)
            pygame.draw.polygon(surface, color, [
                (heart_x - 10, heart_y),
                (heart_x + 10, heart_y),
                (heart_x, heart_y + 11)
            ])

    def _draw_game_over(self, surface):
        """
        Task 2 & 3: Displays stylized Game Over card with final score,
        defeat reason, and difficulty replay buttons.
        """
        # Semi-transparent dark overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill(OVERLAY_BG)
        surface.blit(overlay, (0, 0))

        # Modal panel box
        panel_w, panel_h = 520, 420
        panel_x = (self.width - panel_w) // 2
        panel_y = (self.height - panel_h) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(surface, (28, 32, 54), panel_rect, border_radius=16)
        pygame.draw.rect(surface, (80, 100, 140), panel_rect, width=2, border_radius=16)

        # "GAME OVER" Title
        title_surf = self.font_title.render("GAME OVER", True, RED)
        title_rect = title_surf.get_rect(center=(self.width // 2, panel_y + 50))
        surface.blit(title_surf, title_rect)

        # Defeat Reason
        reason_surf = self.font_subtitle.render(self.game_over_reason, True, (240, 190, 80))
        reason_rect = reason_surf.get_rect(center=(self.width // 2, panel_y + 98))
        surface.blit(reason_surf, reason_rect)

        # Final Score & High Score
        score_info = f"Final Score: {self.score}   |   Best: {self.high_score}"
        score_surf = self.font_score.render(score_info, True, WHITE)
        score_rect = score_surf.get_rect(center=(self.width // 2, panel_y + 140))
        surface.blit(score_surf, score_rect)

        # Replay prompt banner
        prompt_surf = self.font_subtitle.render("Select Difficulty to Play Again:", True, (180, 200, 230))
        prompt_rect = prompt_surf.get_rect(center=(self.width // 2, panel_y + 190))
        surface.blit(prompt_surf, prompt_rect)

        # Buttons config (Task 3: Replay with Easy, Medium, Hard, or Quit)
        buttons = [
            ("Easy", "1. Easy", (46, 125, 50), panel_y + 225),
            ("Medium", "2. Medium", (21, 101, 192), panel_y + 275),
            ("Hard", "3. Hard", (198, 40, 40), panel_y + 325),
            ("Quit", "Q. Exit Game", (60, 64, 80), panel_y + 372)
        ]

        self.replay_buttons.clear()
        mouse_pos = pygame.mouse.get_pos()

        for key, text, base_color, btn_y in buttons:
            btn_w, btn_h = 320, 38
            btn_x = (self.width - btn_w) // 2
            btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            self.replay_buttons[key] = btn_rect

            # Hover highlight
            is_hover = btn_rect.collidepoint(mouse_pos)
            draw_color = tuple(min(255, c + 35) for c in base_color) if is_hover else base_color

            pygame.draw.rect(surface, draw_color, btn_rect, border_radius=8)
            border_col = (255, 255, 255) if is_hover else (120, 140, 170)
            pygame.draw.rect(surface, border_col, btn_rect, width=1, border_radius=8)

            label_surf = self.font_button.render(text, True, WHITE)
            label_rect = label_surf.get_rect(center=btn_rect.center)
            surface.blit(label_surf, label_rect)
