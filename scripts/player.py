import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, tile_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((32, 64))
        self.image.fill('#88c0d0')
        self.rect = self.image.get_rect(center=pos)
        
        # --- Movement Setup ---
        self.direction = pygame.math.Vector2() # Fixed: Initializes the vector
        self.speed = 5                         # Fixed: Needed for move()
        
        # --- Mapping & World Setup ---
        self.vision_radius = 150 
        self.obstacle_sprites = obstacle_sprites
        self.tile_sprites = tile_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        
        # Vertical movement
        if keys[pygame.K_UP]: self.direction.y = -1
        elif keys[pygame.K_DOWN]: self.direction.y = 1
        else: self.direction.y = 0

        # Horizontal movement
        if keys[pygame.K_LEFT]: self.direction.x = -1
        elif keys[pygame.K_RIGHT]: self.direction.x = 1
        else: self.direction.x = 0

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # Moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: # Moving left
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # Moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: # Moving up
                        self.rect.top = sprite.rect.bottom

    def move(self):
        # Normalize the vector so diagonal movement isn't faster (1.41x)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        # Move and check collisions separately to allow sliding along walls
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')

    def reveal_map(self):
        # The heart of the Cartographer loop: revealing hidden tiles
        player_center = pygame.math.Vector2(self.rect.center)
        for tile in self.tile_sprites:
            # We only check tiles that aren't already mapped for performance
            if not tile.mapped:
                dist = player_center.distance_to(tile.rect.center)
                if dist < self.vision_radius:
                    tile.mapped = True

    def update(self):
        self.input()
        self.move()
        self.reveal_map()