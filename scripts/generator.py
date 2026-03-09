import random

class DungeonGenerator:
    def __init__(self, width=30, height=30, max_tiles=150):
        self.width = width
        self.height = height
        self.max_tiles = max_tiles

    def generate(self):
        # 1. Start with a solid block of walls
        grid = [['W' for _ in range(self.width)] for _ in range(self.height)]
        
        # 2. Set the starting point
        x, y = self.width // 2, self.height // 2
        grid[y][x] = 'P' # Player Start
        
        walked_tiles = 1
        while walked_tiles < self.max_tiles:
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            new_x, new_y = x + dx, y + dy
            
            # Stay within map boundaries (leave 1-tile border of 'W')
            if 1 <= new_x < self.width - 1 and 1 <= new_y < self.height - 1:
                x, y = new_x, new_y
                
                # If we hit a wall, decide what it becomes
                if grid[y][x] == 'W':
                    # 8% chance to spawn a specialist FOMO lock
                    if random.random() < 0.08:
                        grid[y][x] = random.choice(['C', 'E', 'A']) # Cipher, Extractor, Architect
                    else:
                        grid[y][x] = ' ' # Just a normal path
                    
                    walked_tiles += 1
        
        # 3. Place the Exit ('X') at the very last position walked
        # Ensure we don't overwrite the player or a specialist
        if grid[y][x] not in ['P', 'C', 'E', 'A']:
            grid[y][x] = 'X'
        
        return ["".join(row) for row in grid]