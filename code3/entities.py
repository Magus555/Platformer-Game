import pygame
from tiles import Tile
from random import randint

class Enemy(Tile):
    def __init__(self,pos,size):
        super().__init__(pos,size,"graphics/enemy/run/2.png")
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = randint(1,2)
        self.size = size
        self.lastUpdate = 0
        self.loopIndex = 5
        self.frameIndex = 0
        self.animationSpeed = 150
        self.dead = 0

        self.frameSet = []
        for i in range(1,7):
            self.frameSet.append(pygame.image.load('graphics/enemy/run/'+str(i)+'.png'))



    def move(self):
        self.rect.x += self.speed

    def reverse(self):
        self.speed *= -1

    def frameIncrementer(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastUpdate > self.animationSpeed:
            self.frameIndex += 1
            if self.frameIndex >= self.loopIndex: self.frameIndex = 0
            self.lastUpdate = currentTime
        
        self.image = self.frameSet[self.frameIndex]

        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)
        
        self.image = pygame.transform.scale(self.image,(self.size,self.size))

    def update(self,shift):
            self.frameIncrementer()
            self.rect.x += shift
            self.move()
class Coin(Tile):
    def __init__(self,pos,size):
        super().__init__(pos,size,'graphics/coins/coin.png')
        self.rect = self.image.get_rect(topleft = pos)

class Flag(Tile):
    def __init__(self,pos,size):
        super().__init__(pos,size,'graphics/overworld/End (Idle).png')
        self.rect = self.image.get_rect(topleft = pos)

class Explosion(Tile):
    def __init__(self,pos,size):
        super().__init__(pos,size,'graphics/enemy/explosion/1.png')
        self.rect = self.image.get_rect(topleft = pos)

        self.lastUpdate = 0
        self.frameIndex = 0
        self.animationSpeed = 150
        self.size = size

        self.deathAnim = []
        for i in range(1,8):
            self.deathAnim.append(pygame.image.load('graphics/enemy/explosion/'+str(i)+'.png'))

    def update(self,shift):

        self.rect.x += shift

        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastUpdate > self.animationSpeed:
            self.frameIndex += 1
            if(self.frameIndex >= 6):
                self.kill()
            self.lastUpdate = currentTime
        self.image = self.deathAnim[self.frameIndex]
        self.image = pygame.transform.scale(self.image,(self.size,self.size))

