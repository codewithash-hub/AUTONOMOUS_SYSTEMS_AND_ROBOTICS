import pygame
import heapq

# --- A* PATHFINDING IMPLEMENTATION ---
class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  # cost from start
        self.h = 0  # heuristic
        self.f = 0  # total cost

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    # Manhattan distance
    return abs(a.x - b.x) + abs(a.y - b.y)

def astar(start, goal, grid, grid_size):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, start)

    while open_list:
        current = heapq.heappop(open_list)
        if (current.x, current.y) == (goal.x, goal.y):
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        closed_set.add((current.x, current.y))

        # Explore neighbors
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            x2, y2 = current.x + dx, current.y + dy
            if 0 <= x2 < grid_size and 0 <= y2 < grid_size and grid[y2][x2] == 0:
                if (x2, y2) in closed_set:
                    continue

                neighbor = Node(x2, y2, current)
                neighbor.g = current.g + 1
                neighbor.h = heuristic(neighbor, goal)
                neighbor.f = neighbor.g + neighbor.h

                # Check if already in open_list with lower f
                if any(n.x == neighbor.x and n.y == neighbor.y and n.f <= neighbor.f for n in open_list):
                    continue

                heapq.heappush(open_list, neighbor)

    return None  # No path found

# --- PYGAME VISUALIZATION ---
pygame.init()
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
CELL = WIDTH // GRID_SIZE

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding - Autonomous Navigation")

# Create grid (0=empty, 1=obstacle)
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Add some obstacles
for i in range(10, 20):
    grid[15][i] = 1
for i in range(5, 25):
    grid[i][10] = 1

start = Node(2, 2)
goal = Node(25, 20)

path = astar(start, goal, grid, GRID_SIZE)

# --- MAIN LOOP ---
run = True
while run:
    win.fill((255, 255, 255))

    # Draw grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
            if grid[y][x] == 1:
                pygame.draw.rect(win, (0, 0, 0), rect)  # obstacle
            pygame.draw.rect(win, (200, 200, 200), rect, 1)

    # Draw start & goal
    pygame.draw.rect(win, (0, 255, 0), (start.x*CELL, start.y*CELL, CELL, CELL))
    pygame.draw.rect(win, (255, 0, 0), (goal.x*CELL, goal.y*CELL, CELL, CELL))

    # Draw path
    if path:
        for (x, y) in path:
            pygame.draw.rect(win, (0, 0, 255), (x*CELL, y*CELL, CELL, CELL))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
