import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, tile_sprites, data_manager, level):
        super().__init__(groups)
        self.image = pygame.Surface((32, 64))
        self.image.fill('#88c0d0')
        self.rect = self.image.get_rect(center=pos)
        
        # --- Persistent Data & State ---
        self.data = data_manager # Access to Ink, Essentials, and Gold
        self.level = level       # To check if we are in Town
        
        # --- Movement Setup ---
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
        # --- Mapping & World Setup ---
        self.vision_radius = 200
        self.obstacle_sprites = obstacle_sprites
        self.tile_sprites = tile_sprites

    def input(self):
        # We stop allowing movement if Ink is empty (The "Faint" threshold)
        if self.data.ink_current <= 0 and not self.level.is_town:
            self.direction.update(0, 0)
            return

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
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')

    def reveal_map(self):
        # The heart of the Cartographer loop
        # Only reveal if the player has Ink remaining
        if self.data.ink_current <= 0 and not self.level.is_town:
            return

        player_center = pygame.math.Vector2(self.rect.center)
        for tile in self.tile_sprites:
            if not tile.mapped:
                dist = player_center.distance_to(tile.rect.center)
                if dist < self.vision_radius:
                    tile.mapped = True
                    # Reward based on Pen Tier
                    reward = tile.revealed_value * self.data.essentials['pen']
                    self.data.gold += reward

    def update(self):
        self.input()
        self.move()
        self.reveal_map()
        
        # --- Ink Drain Logic ---
        # Only drain ink when moving and NOT in town
        if self.direction.magnitude() != 0 and not self.level.is_town:
            # Base drain (0.05). Future: Adjust by 'Focus Buff'
            self.data.ink_current -= 0.05 
            
            # Clamp ink to 0
            if self.data.ink_current < 0:
                self.data.ink_current = 0