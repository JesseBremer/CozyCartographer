import random

class DungeonGenerator:
    def __init__(self, width=20, height=20, max_tiles=100):
        self.width = width
        self.height = height
        self.max_tiles = max_tiles

    def generate(self):
        # 1. Initialize grid with walls
        grid = [['W' for _ in range(self.width)] for _ in range(self.height)]
        
        # 2. Starting Point (The heart of the ruin)
        x, y = self.width // 2, self.height // 2
        grid[y][x] = 'P' 
        
        # Dynamic Scaling: Chance for a specialist lock increases slightly with map size
        # This ensures larger maps aren't just empty hallways
        specialist_chance = 0.05 + (self.width / 500) 
        
        walked_tiles = 1
        path_history = [(x, y)] # Track tiles for smarter exit placement

        while walked_tiles < self.max_tiles:
            # Pick a random direction
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            new_x, new_y = x + dx, y + dy
            
            # Boundary Check: Keep a 1-tile thick wall border around the edge
            if 1 <= new_x < self.width - 1 and 1 <= new_y < self.height - 1:
                x, y = new_x, new_y
                
                if grid[y][x] == 'W':
                    # Determine if this new floor tile is a specialist lock
                    if random.random() < specialist_chance:
                        grid[y][x] = random.choice(['C', 'E', 'A']) # Cipher, Extractor, Architect
                    else:
                        grid[y][x] = ' ' # Standard navigable floor
                    
                    walked_tiles += 1
                    path_history.append((x, y))

        # 3. Smart Exit Placement ('X')
        # We look back through path history to find the furthest point from the start
        # that isn't already a specialist lock or the player start.
        for i in range(len(path_history) - 1, -1, -1):
            ex, ey = path_history[i]
            if grid[ey][ex] == ' ':
                grid[ey][ex] = 'X'
                break
        
        # Convert to list of strings for the Level class
        return ["".join(row) for row in grid]