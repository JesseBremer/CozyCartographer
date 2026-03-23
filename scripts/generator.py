# scripts/generator.py

import random

class DungeonGenerator:
    def __init__(self, width=20, height=20, max_tiles=100):
        self.width = width
        self.height = height
        self.max_tiles = max_tiles

    def generate(self):
        # Fill everything with Walls
        grid = [['W' for _ in range(self.width)] for _ in range(self.height)]
        
        # Determine Entrance (Bottom Center, but 2 tiles up from the absolute edge)
        start_x = self.width // 2
        start_y = self.height - 2 
        
        # Place the Exit/Entrance
        grid[start_y][start_x] = 'X'
        
        # Start the "Drunkard" at the tile ABOVE the exit
        # This ensures there is an immediate floor tile to step into
        x, y = start_x, start_y - 1
        grid[y][x] = ' ' 
        
        walked_tiles = 1
        while walked_tiles < self.max_tiles:
            # Bias movement UP and AWAY from the edges
            directions = [(0, -1), (0, -1), (1, 0), (-1, 0), (0, 1)] 
            dx, dy = random.choice(directions)
            new_x, new_y = x + dx, y + dy
            
            # Stay within 1-tile border
            if 1 <= new_x < self.width - 1 and 1 <= new_y < self.height - 1:
                x, y = new_x, new_y
                if grid[y][x] == 'W':
                    # --- ADD SPECIALIST LOGIC HERE ---
                    # 10% chance for a Specialist, 90% for a Floor
                    if random.random() < 0.10:
                        grid[y][x] = random.choice(['C', 'E', 'A'])
                    else:
                        grid[y][x] = ' ' 
                    
                    walked_tiles += 1
                    
        return ["".join(row) for row in grid]