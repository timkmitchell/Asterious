'''
Player
'''

import pygame

WHITE = (255, 255, 255)
GREEN = (30, 240, 120)
RED = (255, 0, 0)

 
class Player(pygame.sprite.Sprite):

    def __init__(self, img):

        super().__init__()
 
        
        self.image = img

        self.rect = self.image.get_rect()
        self.radius = 17
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 1)
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.invis = 50
        
    def update(self):
        self.speedx = 0
        self.speedy = 0
        
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.speedy = -5
        if keystate[pygame.K_s]:
            self.speedy = 5
        if keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_d]:
            self.speedx = 5
            
        if self.rect.right > 550:
            self.rect.right = 550
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
        if self.rect.top < 0:
            self.rect.top = 0
            
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
 

        
        