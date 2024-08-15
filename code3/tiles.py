import pygame 

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,width,height,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self,x_shift):
        self.rect.x += x_shift

class Coin(Tile):
    def __init__(self,pos,size):
        super().__init__(pos,size,size,'graphics/coins/coin.png')
        self.rect = self.image.get_rect(topleft = pos)

class Flag(Tile):
    def __init__(self,pos,size):
        super().__init__(pos,size,size,'graphics/overworld/End (Idle).png')
        self.rect = self.image.get_rect(topleft = pos)

class backgroundTile(Tile):

    def update(self,y_shift):
        self.rect.y -= y_shift