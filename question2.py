import pygame
import math

# ===============================
# 2D LiDAR Sensor Simulation
# ===============================

pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D LiDAR Sensor Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 128, 255)

# LiDAR settings
lidar_pos = (400, 500)   # Fixed LiDAR position
fov = 180                # Field of view
num_rays = fov           # 1 ray per degree
max_range = 400          # Max LiDAR range

# Obstacles as Rectangles
rectangles = [
    pygame.Rect(100, 300, 300, 200),
    pygame.Rect(300, 200, 500, 250),
    pygame.Rect(500, 250, 700, 300),
    pygame.Rect(200, 400, 600, 400),
]

# Convert rectangles into line segments [(p1, p2), ...]
def rect_to_segments(rect):
    x, y, w, h = rect
    return [
        ((x, y), (x + w, y)),         # top edge
        ((x + w, y), (x + w, y + h)), # right edge
        ((x + w, y + h), (x, y + h)), # bottom edge
        ((x, y + h), (x, y))          # left edge
    ]

obstacles = []
for rect in rectangles:
    obstacles.extend(rect_to_segments(rect))

# ===============================
# Utility Functions
# ===============================

def line_intersection(p1, p2, p3, p4):
    """Find intersection point of two segments (p1->p2 and p3->p4)."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if denom == 0:
        return None

    px = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / denom

    if (min(x1, x2) <= px <= max(x1, x2) and
        min(y1, y2) <= py <= max(y1, y2) and
        min(x3, x4) <= px <= max(x3, x4) and
        min(y3, y4) <= py <= max(y3, y4)):
        return (px, py)

    return None

def cast_ray(angle_deg):
    """Cast a ray at angle and return nearest hit point or max range."""
    angle = math.radians(angle_deg)
    dx = math.cos(angle)
    dy = math.sin(angle)

    ray_end = (lidar_pos[0] + dx*max_range, lidar_pos[1] - dy*max_range)
    closest_point = None
    min_dist = float("inf")

    for seg in obstacles:
        pt = line_intersection(lidar_pos, ray_end, seg[0], seg[1])
        if pt:
            dist = math.dist(lidar_pos, pt)
            if dist < min_dist:
                min_dist = dist
                closest_point = pt

    return closest_point if closest_point else ray_end

# ===============================
# Main Loop
# ===============================

def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        WIN.fill(BLACK)

        # Draw rectangles
        for rect in rectangles:
            pygame.draw.rect(WIN, WHITE, rect, 2)

        # Draw LiDAR position
        pygame.draw.circle(WIN, BLUE, lidar_pos, 6)

        detected_points = []

        # Cast rays in 180° FOV
        for i in range(num_rays + 1):
            angle = -fov/2 + i
            pt = cast_ray(angle)
            detected_points.append(pt)

            pygame.draw.line(WIN, RED, lidar_pos, pt, 1)
            pygame.draw.circle(WIN, RED, (int(pt[0]), int(pt[1])), 3)

        print("Detected Points:", [(int(x), int(y)) for x, y in detected_points])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
