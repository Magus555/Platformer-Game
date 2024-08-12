import pygame 

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size,text):
        super().__init__()
        self.image = pygame.image.load(text)
        self.image = pygame.transform.scale(self.image,(size,size))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self,x_shift):
        self.rect.x += x_shift

