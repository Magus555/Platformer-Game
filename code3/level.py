import pygame, sys
from pytmx import load_pygame
from tiles import Tile, backgroundTile, Coin, Flag
from settings import *
from player import Player
from entities import Enemy, Explosion

class Level:
    def __init__(self,levelData,surface):
        
        self.finishState = False
        self.levelComplete = 0
        self.lives = 0
        self.score = 0
        self.displaySurface = surface
        self.backgroundSurface = pygame.Surface((screenWidth+1000,screenHeight))
        self.setupLevel()
        self.levelSurface = pygame.Surface((self.levelSize[0]+5000,self.levelSize[1]+1000))

        self.worldShift = 0
        self.scrollYspeed = 15
        self.currentX = 0
        self.playerHealth = 2
        self.hitCD = 0
        self.currentClock = 0
        self.coinCount = 0
        self.timeOfHit = 1000000000000000000000000000000000000000000000000000000000
        self.spawnDistance = 0
        self.scroll = 0

        self.scroll_x = 0
        self.scroll_y = 0
        self.background_y = screenHeight

    def setupLevel(self):

        self.levelSize = [0,0]



        tmx_data = load_pygame('mapLevel1.tmx')
        self.tileGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.coinGroup = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.flag = pygame.sprite.GroupSingle()
        self.explosionGroup = pygame.sprite.GroupSingle()



        for y in range(0,9):
            for x in range(0,17):
                image = pygame.image.load("graphics/Background/Brown.png").convert_alpha()
                image = pygame.transform.scale(image,(screenWidth/16,screenHeight/8))
                self.backgroundSurface.blit(image, (screenWidth/16 * x,screenHeight/8 * y), area=None)

        # cycle through all layers
        for layer in tmx_data.visible_layers:
            # if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
            if hasattr(layer,'data'):
                for x,y,surf in layer.tiles():
                    pos = (x * 64 + 2000, y * 48)
                    Tile(pos = pos, width = 64, height = 48, surf = surf, groups = self.tileGroup)
                    if x>self.levelSize[0]: self.levelSize[0]=x
                    if y>self.levelSize[1]: self.levelSize[1]=y
        
        self.levelSize[0]=self.levelSize[0]*64
        self.levelSize[1]=self.levelSize[1]*64

        for obj in tmx_data.get_layer_by_name('Player'):
            pos = obj.x*4 + 2000,obj.y*3
            self.spawnPosition=(pos[0],pos[1])
            self.player.add(Player(pos))
        for obj in tmx_data.get_layer_by_name('Enemy'):
            pos = obj.x*4 + 2000,obj.y*3
            Enemy(pos,64,groups=self.enemyGroup)
        for obj in tmx_data.get_layer_by_name('Coin'):
            pos = obj.x*4 + 2000,obj.y*3
            Coin(pos,64,groups=self.coinGroup)
        for obj in tmx_data.get_layer_by_name('Flag'):
            pos = obj.x*4 + 2000,obj.y*3
            Flag(pos,64,groups=self.flag)

    def backgroundScrolling(self):
        self.scroll_y += 1
        self.background_y += 1

        self.levelSurface.blit(self.backgroundSurface, (self.player.sprite.rect.topleft[0]-(screenWidth/2), self.scroll_y))
        self.levelSurface.blit(self.backgroundSurface, (self.player.sprite.rect.topleft[0]-(screenWidth/2), self.background_y))

        if self.scroll_y >= screenHeight:
            self.scroll_y = -screenHeight+1

        if self.background_y >= screenHeight:
            self.background_y = -screenHeight+1


 
                    

    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x

        if playerX < screenWidth / 4 and directionX < 0:
            self.worldShift = 8
            player.speed = 0
            self.spawnDistance += 8
        elif playerX > screenWidth - (screenWidth / 4) and directionX > 0:
            self.worldShift = -8
            player.speed = 0
            self.spawnDistance -= 8
        else:
            self.worldShift = 0
            player.speed = 8
    





    
    def respawn(self):
        self.player.sprite.rect.x=self.spawnPosition[0]
        self.player.sprite.rect.y=self.spawnPosition[1]
        self.lives = self.lives-1
        self.worldShift=-self.spawnDistance
        self.spawnDistance=0
        self.playerHealth = 2

    def fallOutOfBounds(self):
        playerY = self.player.sprite.rect.centery
        if playerY > screenHeight:
            self.respawn()

    def horizontalMovementCollision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed


        for sprite in self.tileGroup.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.currentX = player.rect.right

        for sprite in self.tileGroup.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.currentX = player.rect.right
                    
    def verticalMovementCollision(self):
        player = self.player.sprite
        player.applyGravity()

        for sprite in self.tileGroup.sprites():
            if sprite.rect.colliderect(player.rect) == True:
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
        
        for sprite in self.tileGroup.sprites():
            if sprite.rect.colliderect(player.rect) == True:
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    sprite.kill()
                    self.score = self.score + 25

    def playerEnemyCollisionCheck(self):
        if self.currentClock>=self.timeOfHit+2:
            self.timeOfHit=10000000000000000000
            self.hitCD = 0
        enemyCollisionsTop = pygame.sprite.spritecollide(self.player.sprite,self.enemyGroup,False)
        enemyCollisionsSide = pygame.sprite.spritecollide(self.player.sprite,self.enemyGroup,False)
        if enemyCollisionsTop:
            for thisEnemy in enemyCollisionsTop:
                enemyCenter = thisEnemy.rect.centery
                enemyTop = thisEnemy.rect.top
                playerBottom = self.player.sprite.rect.bottom
                if enemyTop < playerBottom < enemyCenter and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    (x,y) = thisEnemy.rect.topleft
                    thisEnemy.kill()
                    Explosion((x,y),64,self.explosionGroup)
                    self.score = self.score + 50

        if enemyCollisionsSide:
            for enemy in enemyCollisionsSide:
                enemyCenter = enemy.rect.centery
                player=self.player.sprite.rect.centery

                if enemyCenter<=player and self.hitCD == 0:
                    self.playerHealth=self.playerHealth - 1
                    self.hitCD=1
                    self.timeOfHit=self.currentClock

                    if self.playerHealth == 0:
                        self.respawn()
    

    def enemyCollisionReverse(self):
        for enemy in self.enemyGroup.sprites():
            if pygame.sprite.spritecollide(enemy,self.tileGroup,False) or pygame.sprite.spritecollide(enemy,self.tileGroup,False):
                enemy.reverse()

    def playerCoinCollisionCheck(self):
        coinCollisions = pygame.sprite.spritecollide(self.player.sprite,self.coinGroup,False)
        if coinCollisions:
            for coin in coinCollisions:
                self.coinCount=(self.coinCount+1)
                self.playerHealth=2
                coin.kill()
        
    def playerFlagCollisionCheck(self):
        flagCollisions = pygame.sprite.spritecollide(self.player.sprite,self.flag,False)
        if flagCollisions:
            self.finishState = True

    def run(self):
  
        self.levelSurface.fill('black')

        

        self.fallOutOfBounds()

        self.enemyCollisionReverse()
        self.playerEnemyCollisionCheck()

        self.horizontalMovementCollision()
        self.verticalMovementCollision()

        self.playerCoinCollisionCheck()
        self.playerFlagCollisionCheck()

        self.tileGroup.update()
        

        self.enemyGroup.update()
        
        
        self.explosionGroup.update()
        
        
        self.coinGroup.update
        

        self.flag.update()
        

        self.player.update(self.playerHealth)
        

        self.backgroundScrolling()
       
        self.tileGroup.draw(self.levelSurface)
        self.enemyGroup.draw(self.levelSurface)
        self.explosionGroup.draw(self.levelSurface)
        self.coinGroup.draw(self.levelSurface)
        self.flag.draw(self.levelSurface)
        self.player.draw(self.levelSurface)
        
        self.displaySurface.blit(self.levelSurface,(0,0),area=(self.player.sprite.rect.topleft[0]-(screenWidth/2),0,screenWidth,screenHeight))

        

        


        
        
      

        




