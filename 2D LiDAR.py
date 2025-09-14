import pygame
import math

# Initializa pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D LiDAR Sensor Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 255, 0)

# Obstacles (walls)
walls = [
    pygame.Rect(100, 100, 500, 20),
    pygame.Rect(100, 200, 20, 300),
    pygame.Rect(600, 200, 20, 300),
    pygame.Rect(200, 500, 410, 20),
    pygame.Rect(300, 200, 20, 300),
]

# LiDAR sensor position
lidar_x, lidar_y = WIDTH // 3, HEIGHT // 3
num_rays = 360
max_range = 400

def cast_ray(angle):
    """Cast a ray from the LiDAR sensor and return the closest intersection point."""
    x = lidar_x
    y = lidar_y
    dx = math.cos(angle)
    dy = math.sin(angle)

    for i in range(max_range):
        px = int(x + dx * i)
        py = int(y + dy * i)

        # Check collision with walls
        for wall in walls:
            if wall.collidepoint(px, py):
                return px, py
    return px, py # no collision, return max range



clock = pygame.time.Clock()
run = True

while run:
    clock.tick(60)
    window.fill(BLACK)

    # draw walls
    for wall in walls:
        pygame.draw.rect(window, WHITE, wall)

    # Draw LiDAR sensor
    pygame.draw.circle(window, RED, (lidar_x, lidar_y), 5)

    # Cast rays
    for i in range(num_rays):
        angle = math.radians(i)
        hit_point = cast_ray(angle)
        pygame.draw.line(window, RED, (lidar_x, lidar_y), hit_point, 1)
        pygame.draw.circle(window, RED, hit_point, 2)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
