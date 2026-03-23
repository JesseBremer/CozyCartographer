import random

class DungeonGenerator:
    def __init__(self, width=20, height=20, max_tiles=100):
        self.width = width
        self.height = height
        self.max_tiles = max_tiles

    def generate(self):
        # 1. Initialize the entire grid as Walls ('W')
        grid = [['W' for _ in range(self.width)] for _ in range(self.height)]
        
        # 2. Establish the "Safe Zone" Center
        # We use integer division to find the middle
        start_x = self.width // 2
        start_y = self.height // 2
        
        # Place the player at the center
        grid[start_y][start_x] = 'P' 
        
        # 3. Random Walk Variables
        x, y = start_x, start_y
        walked_tiles = 1
        path_history = [(x, y)]

        while walked_tiles < self.max_tiles:
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            new_x, new_y = x + dx, y + dy
            
            # Boundary Check (Leave a 1-tile thick wall border)
            if 1 <= new_x < self.width - 1 and 1 <= new_y < self.height - 1:
                x, y = new_x, new_y
                
                # SAFEGUARD: Only change the tile if it is currently a Wall.
                # This prevents the walker from overwriting 'P' with a floor or specialist.
                if grid[y][x] == 'W':
                    # Roll for specialists or standard floor
                    specialist_chance = 0.05 + (self.width / 500)
                    if random.random() < specialist_chance:
                        grid[y][x] = random.choice(['C', 'E', 'A'])
                    else:
                        grid[y][x] = ' ' # Standard floor
                    
                    walked_tiles += 1
                    path_history.append((x, y))

        # 4. Smart Exit Placement (Furthest valid point)
        for i in range(len(path_history) - 1, -1, -1):
            ex, ey = path_history[i]
            # Ensure we don't put the exit on top of the player!
            if grid[ey][ex] == ' ':
                grid[ey][ex] = 'X'
                break
                
        return ["".join(row) for row in grid]