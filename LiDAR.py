import pygame
import math

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D LiDAR Sensor Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 255, 0)

walls = {
    pygame.Rect(100, 100, 500, 20),
    pygame.Rect(100, 200, 20, 300),
    pygame.Rect(600, 200, 20, 300),
    pygame.Rect(200, 500, 410, 20),
    pygame.Rect(300, 200, 20, 300),
}

# LiDAR postion
lidar_x, lidar_y = WIDTH // 2, HEIGHT // 2
num_rays = 180
max_range = 300

def cast_ray(angle):
    x = lidar_x
    y = lidar_y
    dx = math.cos(angle)
    dy = math.sin(angle)

    for i in range(max_range):
        px = int(x + dx * i)
        py = int(y + dy * i)

        for wall in walls:
            if wall.collidepoint(px, py):
                return px, py
    return px, py