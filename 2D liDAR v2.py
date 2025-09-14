import pygame
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D LiDAR Robot Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 128, 255)

# Obstacles (walls)
walls = [
    pygame.Rect(100, 100, 600, 20),
    pygame.Rect(100, 200, 20, 300),
    pygame.Rect(680, 200, 20, 300),
    pygame.Rect(200, 500, 400, 20),
    pygame.Rect(300, 200, 20, 300)
]

# Robot properties
robot_x, robot_y = WIDTH // 2, HEIGHT // 2
robot_speed = 3
robot_radius = 10

# LiDAR properties
num_rays = 360
max_range = 250

def cast_ray(x, y, angle):
    """Cast a ray from (x,y) at given angle, return the intersection point."""
    dx = math.cos(angle)
    dy = math.sin(angle)

    for i in range(max_range):
        px = int(x + dx * i)
        py = int(y + dy * i)

        # Check collision with walls
        for wall in walls:
            if wall.collidepoint(px, py):
                return px, py
    return px, py  # No collision, max range point

def draw_robot(x, y):
    pygame.draw.circle(WIN, BLUE, (x, y), robot_radius)

def lidar_scan(x, y):
    """Perform LiDAR scan around the robot."""
    for i in range(num_rays):
        angle = math.radians(i)
        hit_point = cast_ray(x, y, angle)
        pygame.draw.line(WIN, RED, (x, y), hit_point, 1)
        pygame.draw.circle(WIN, RED, hit_point, 2)

def main():
    global robot_x, robot_y
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        # Draw walls
        for wall in walls:
            pygame.draw.rect(WIN, WHITE, wall)

        # Robot movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            robot_y -= robot_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            robot_y += robot_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            robot_x -= robot_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            robot_x += robot_speed

        # Draw robot and LiDAR scan
        lidar_scan(robot_x, robot_y)
        draw_robot(robot_x, robot_y)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
