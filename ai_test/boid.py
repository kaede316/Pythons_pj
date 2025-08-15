import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boids Algorithm - Flocking Behavior Simulation")

# Color definitions
BACKGROUND = (255, 255, 255)  # Changed to white background
BOID_COLOR = (0, 100, 200)  # Adjusted for better visibility on white
HIGHLIGHT_COLOR = (200, 0, 0)
TEXT_COLOR = (50, 50, 50)  # Darker text for white background
GRID_COLOR = (220, 220, 220)  # Lighter grid for white background
CONNECTION_COLOR = (100, 150, 200)  # Adjusted connection color

# Font settings: Use simple English font (default system font)
font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 25)

# Boid class (unchanged)
class Boid:
    # 分离，对齐，聚集
    def __init__(self, x, y, boid_type="basic"):
        self.type = boid_type
        self.separation_strength = 1.2 if boid_type == "advanced" else 1.0
        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle))
        self.velocity *= random.uniform(1.5, 3.0)
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 3.0
        self.max_force = 0.2
        self.perception = 50
        self.size = 6

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.position += self.velocity
        self.acceleration *= 0

        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x > WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT:
            self.position.y = 0

    def apply_force(self, force):
        self.acceleration += force

    def align(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < self.perception:
                steering += boid.velocity
                total += 1
        if total > 0:
            steering /= total
            steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def cohesion(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < self.perception:
                steering += boid.position
                total += 1
        if total > 0:
            steering /= total
            steering -= self.position
            if steering.length() > 0:
                steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def separation(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < self.perception and distance > 0:
                diff = self.position - boid.position
                diff /= distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering.scale_to_length(self.max_speed)
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
        return steering

    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)

        alignment *= 1.0
        cohesion *= 0.8
        separation *= 1.2

        self.apply_force(alignment)
        self.apply_force(cohesion)
        self.apply_force(separation)

    def draw(self, surface):
        angle = math.atan2(self.velocity.y, self.velocity.x)
        points = [
            (self.position.x + self.size * math.cos(angle),
             self.position.y + self.size * math.sin(angle)),
            (self.position.x + self.size / 2 * math.cos(angle + 2.5),
             self.position.y + self.size / 2 * math.sin(angle + 2.5)),
            (self.position.x + self.size / 2 * math.cos(angle - 2.5),
             self.position.y + self.size / 2 * math.sin(angle - 2.5))
        ]
        pygame.draw.polygon(surface, BOID_COLOR, points)

# Create boids flock
boids = []
for _ in range(150):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    boids.append(Boid(x, y))

# Draw background grid
def draw_grid():
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)

# Draw info panel (translated to English)
def draw_info_panel(boids_count):
    # Semi-transparent panel background (adjusted for white theme)
    # panel_surf = pygame.Surface((300, 250), pygame.SRCALPHA)
    # panel_surf.fill((240, 240, 240, 180))  # Light gray semi-transparent
    # screen.blit(panel_surf, (20, 20))
    #
    # panel_surf_right = pygame.Surface((300, 200), pygame.SRCALPHA)
    # panel_surf_right.fill((240, 240, 240, 180))
    # screen.blit(panel_surf_right, (WIDTH - 320, 20))

    # Left panel: Rules
    title = font.render("Boids Algorithm Demo", True, HIGHLIGHT_COLOR)
    screen.blit(title, (30, 30))

    rules = [
        "Flocking Rules:",
        "1. Separation: Avoid crowding neighbors",
        "2. Alignment: Steer towards average heading",
        "3. Cohesion: Steer towards average position"
    ]
    for i, rule in enumerate(rules):
        text = small_font.render(rule, True, TEXT_COLOR)
        screen.blit(text, (30, 70 + i * 25))

    count_text = small_font.render(f"Current Boids: {boids_count}", True, TEXT_COLOR)
    screen.blit(count_text, (30, 70 + len(rules) * 25 + 20))

    # Right panel: Controls
    controls_title = font.render("Controls", True, HIGHLIGHT_COLOR)
    screen.blit(controls_title, (WIDTH - 310, 30))

    controls = [
        "Space - Reset flock (150)",
        "Left click - Add 5 Boids",
        "Right click - Remove nearest 10",
        "ESC - Quit"
    ]
    for i, control in enumerate(controls):
        text = small_font.render(control, True, TEXT_COLOR)
        screen.blit(text, (WIDTH - 310, 70 + i * 25))

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                boids = []
                for _ in range(150):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    boids.append(Boid(x, y))
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if event.button == 1:  # Left click add
                for _ in range(5):
                    boids.append(Boid(x, y))
            elif event.button == 3:  # Right click remove
                if boids:
                    boids.sort(key=lambda b: b.position.distance_to(pygame.Vector2(x, y)))
                    del boids[:10]

    # Update boids
    for boid in boids:
        boid.flock(boids)
        boid.update()

    # Draw
    screen.fill(BACKGROUND)
    draw_grid()

    # Draw connections between boids
    for i, boid1 in enumerate(boids):
        for boid2 in boids[i + 1:]:
            distance = boid1.position.distance_to(boid2.position)
            if distance < boid1.perception:
                alpha = int(max(0, 100 - distance * 2))
                color = (*CONNECTION_COLOR[:3], alpha)
                pygame.draw.line(screen, color, boid1.position, boid2.position, 1)

    # Draw boids
    for boid in boids:
        boid.draw(screen)

    # Draw info panel
    draw_info_panel(len(boids))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()