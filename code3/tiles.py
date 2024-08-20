import pygame 

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,width,height,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect(topleft = pos)




class Coin(Tile):
    def __init__(self,pos,size,groups):
        super().__init__(pos,size,size,pygame.image.load('graphics/coins/coin.png'),groups)
        self.rect = self.image.get_rect(topleft = pos)

class Flag(Tile):
    def __init__(self,pos,size,groups):
        super().__init__(pos,size,size,pygame.image.load('graphics/overworld/End (Idle).png'),groups)
        self.rect = self.image.get_rect(topleft = pos)

class backgroundTile(Tile):

    def update(self,y_shift):
        self.rect.y -= y_shift