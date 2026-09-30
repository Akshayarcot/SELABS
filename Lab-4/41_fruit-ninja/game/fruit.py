import math
import random
import pygame

FRUIT_SPECS = {
    "apple": {
        "outer": (220, 45, 45),
        "inner": (255, 235, 205),
        "highlight": (255, 120, 120),
        "name": "Apple"
    },
    "orange": {
        "outer": (255, 140, 20),
        "inner": (255, 210, 140),
        "highlight": (255, 190, 80),
        "name": "Orange"
    },
    "lemon": {
        "outer": (240, 220, 40),
        "inner": (255, 250, 180),
        "highlight": (255, 245, 120),
        "name": "Lemon"
    },
    "watermelon": {
        "outer": (40, 160, 60),
        "inner": (235, 50, 70),
        "highlight": (100, 210, 110),
        "name": "Watermelon"
    }
}

class Fruit:
    def __init__(self, x, y, vx, vy, gravity, radius=28, kind="fruit"):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.gravity = float(gravity)
        self.radius = radius
        self.kind = kind  # "fruit" or "bomb"
        self.sliced = False

        if self.kind == "fruit":
            self.fruit_key = random.choice(list(FRUIT_SPECS.keys()))
            specs = FRUIT_SPECS[self.fruit_key]
            self.color = specs["outer"]
            self.inner_color = specs["inner"]
            self.highlight_color = specs["highlight"]
        else:
            self.fruit_key = "bomb"
            self.color = (35, 35, 40)
            self.inner_color = (60, 60, 65)
            self.highlight_color = (90, 90, 100)

        # Post-slice separation state
        self.half1_x = self.x
        self.half1_y = self.y
        self.half1_vx = 0.0
        self.half1_vy = 0.0

        self.half2_x = self.x
        self.half2_y = self.y
        self.half2_vx = 0.0
        self.half2_vy = 0.0

        self.rotation1 = 0.0
        self.rotation2 = 0.0
        self.rot_speed1 = 0.0
        self.rot_speed2 = 0.0

        self.particles = []

    def slice(self, swipe_dir=(1, 0)):
        """Splits fruit into two physical halves with juice particles."""
        if self.sliced:
            return
        self.sliced = True

        self.half1_x = self.x
        self.half1_y = self.y
        self.half2_x = self.x
        self.half2_y = self.y

        # Perpendicular impulse along normal to swipe
        norm_x = -swipe_dir[1]
        norm_y = swipe_dir[0]
        mag = math.hypot(norm_x, norm_y) or 1.0
        norm_x /= mag
        norm_y /= mag

        impulse = 4.0
        self.half1_vx = self.vx - norm_x * impulse
        self.half1_vy = self.vy - norm_y * impulse - 2.0
        self.half2_vx = self.vx + norm_x * impulse
        self.half2_vy = self.vy + norm_y * impulse - 2.0

        self.rot_speed1 = random.uniform(-6, -2)
        self.rot_speed2 = random.uniform(2, 6)

        # Generate juice spray particles
        num_particles = 14 if self.kind == "fruit" else 20
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            p_color = self.color if self.kind == "fruit" else (255, 120, 30)
            self.particles.append({
                "x": self.x,
                "y": self.y,
                "vx": math.cos(angle) * speed + self.vx * 0.3,
                "vy": math.sin(angle) * speed + self.vy * 0.3,
                "life": random.randint(15, 30),
                "color": p_color,
                "size": random.randint(3, 6)
            })

    def update(self):
        """Advances physics for unsliced fruit or sliced halves and particles."""
        if not self.sliced:
            self.vy += self.gravity
            self.x += self.vx
            self.y += self.vy
        else:
            # Physics for half 1
            self.half1_vy += self.gravity
            self.half1_x += self.half1_vx
            self.half1_y += self.half1_vy
            self.rotation1 += self.rot_speed1

            # Physics for half 2
            self.half2_vy += self.gravity
            self.half2_x += self.half2_vx
            self.half2_y += self.half2_vy
            self.rotation2 += self.rot_speed2

            # Particle physics
            for p in self.particles:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += self.gravity * 0.6
                p["life"] -= 1
            self.particles = [p for p in self.particles if p["life"] > 0]

    def contains_point(self, px, py):
        """Discrete collision check for a single point."""
        return (self.x - px) ** 2 + (self.y - py) ** 2 <= self.radius ** 2

    def intersects_segment(self, p1, p2):
        """
        Task 1: Enhanced Continuous Collision Detection.
        Calculates minimum distance between fruit center and blade line segment p1-p2.
        Reliably registers fast swipes that cross through the fruit within a single frame.
        """
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        len_sq = dx * dx + dy * dy

        if len_sq == 0:
            return self.contains_point(p1[0], p1[1])

        # Project fruit center onto segment p1-p2, clamped between 0 and 1
        t = ((self.x - p1[0]) * dx + (self.y - p1[1]) * dy) / len_sq
        t = max(0.0, min(1.0, t))

        closest_x = p1[0] + t * dx
        closest_y = p1[1] + t * dy

        dist_sq = (self.x - closest_x) ** 2 + (self.y - closest_y) ** 2
        return dist_sq <= self.radius ** 2

    def is_off_screen(self, screen_height):
        """Checks if fruit (or all fragments) fell below screen bottom."""
        if not self.sliced:
            return self.y > screen_height + 40 and self.vy > 0
        else:
            return (self.half1_y > screen_height + 60 and 
                    self.half2_y > screen_height + 60 and 
                    len(self.particles) == 0)

    def draw(self, surface):
        """Renders fruit/bomb or sliced halves with effects."""
        # Draw juice particles
        for p in self.particles:
            alpha_ratio = max(0.0, p["life"] / 30.0)
            radius = max(1, int(p["size"] * alpha_ratio))
            pygame.draw.circle(surface, p["color"], (int(p["x"]), int(p["y"])), radius)

        if not self.sliced:
            pos = (int(self.x), int(self.y))
            if self.kind == "bomb":
                # Draw bomb body
                pygame.draw.circle(surface, self.color, pos, self.radius)
                pygame.draw.circle(surface, (70, 70, 75), pos, self.radius, 2)
                # Bomb highlight
                pygame.draw.circle(surface, self.highlight_color, 
                                   (pos[0] - self.radius // 3, pos[1] - self.radius // 3), 
                                   self.radius // 4)
                # Cap & fuse
                cap_rect = pygame.Rect(pos[0] - 6, pos[1] - self.radius - 5, 12, 6)
                pygame.draw.rect(surface, (120, 120, 120), cap_rect, border_radius=2)
                fuse_top = (pos[0] + 6, pos[1] - self.radius - 12)
                pygame.draw.line(surface, (210, 180, 100), (pos[0], pos[1] - self.radius - 5), fuse_top, 2)
                # Spark
                spark_color = random.choice([(255, 230, 80), (255, 100, 30), (255, 255, 255)])
                pygame.draw.circle(surface, spark_color, fuse_top, random.randint(3, 5))
            else:
                # Fruit body
                pygame.draw.circle(surface, self.color, pos, self.radius)
                # 3D Highlight
                pygame.draw.circle(surface, self.highlight_color, 
                                   (pos[0] - self.radius // 3, pos[1] - self.radius // 3), 
                                   self.radius // 3)
                # Stem & leaf
                stem_end = (pos[0], pos[1] - self.radius - 4)
                pygame.draw.line(surface, (100, 60, 20), (pos[0], pos[1] - self.radius + 2), stem_end, 3)
                leaf_rect = pygame.Rect(stem_end[0], stem_end[1] - 4, 8, 5)
                pygame.draw.ellipse(surface, (50, 180, 50), leaf_rect)
        else:
            # Draw two split halves
            for hx, hy, angle in [(self.half1_x, self.half1_y, self.rotation1), 
                                  (self.half2_x, self.half2_y, self.rotation2)]:
                hpos = (int(hx), int(hy))
                half_r = max(4, self.radius - 2)
                pygame.draw.circle(surface, self.color, hpos, half_r)
                pygame.draw.circle(surface, self.inner_color, hpos, max(2, half_r - 6))
                if self.kind == "fruit" and self.fruit_key == "watermelon":
                    # Little seeds
                    pygame.draw.circle(surface, (30, 30, 30), (hpos[0] - 4, hpos[1]), 2)
                    pygame.draw.circle(surface, (30, 30, 30), (hpos[0] + 4, hpos[1] - 3), 2)
