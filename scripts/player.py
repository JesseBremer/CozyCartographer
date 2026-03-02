import pygame

class Player(pygame.sprite.Sprite):
    # Added 'obstacle_sprites' to the arguments list here
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((32, 64))
        self.image.fill('#a3be8c') 
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites 

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: self.direction.y = -1
        elif keys[pygame.K_DOWN]: self.direction.y = 1
        else: self.direction.y = 0

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
            
        # You must move and check collisions separately for X and Y!
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')

    def update(self):
        self.input()
        self.move()