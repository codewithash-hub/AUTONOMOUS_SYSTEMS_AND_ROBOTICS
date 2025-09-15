import heapq
import matplotlib.pyplot as plt
import numpy as np

# Hueristic function
def hueristic(a, b):
    return abs(a[0] - b[0]) - abs(a[1] - b[1])

# A* algorithm
def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: hueristic(start, goal)}
    visited = set()

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, visited
        
        visited.add(current)

        # Explore neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + hueristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None, visited


# Create 10x10 gird (0=free, 1=obstacle)
grid = np.zeros((10, 10), dtype=int)

# Draw obstacle
grid[3, 1:5] = 1
grid[6, 4:8] = 1
grid[1:5, 8] = 1

# Get user input for start and goal position
start = tuple(map(int, input("Enter start position (row col): ").split()))
goal = tuple(map(int, input("Enter goal position (row col): ").split()))

# Call astart
path, visited = astar(grid, start, goal)

# Visualization
fig, ax = plt.subplots()
ax.imshow(grid, cmap="Greys", origin="upper")

# Mark visited
for (r, c) in visited:
    ax.scatter(c, r, marker=".", color="yellow")

# Mark path
if path:
    for (r, c) in path:
        ax.scatter(c, r, marker="o", color="blue")
    else:
        print("no path found")

# Mark start and goal
ax.scatter(start[1], start[0], marker="s", s=100, label="Start")
ax.scatter(goal[1], goal[0], marker="s", s=100, label="Goal")

ax.set_xticks(np.arange(-0.5, 10, 1), minor=True)
ax.set_yticks(np.arange(-0.5, 10, 1), minor=True)
ax.grid(which="minor", color="black", linewidth=1)
ax.legend()
plt.show()

# LiDAR
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