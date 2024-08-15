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
        self.backgroundSurface = pygame.Surface((screenWidth,screenHeight))
        self.levelSurface = pygame.Surface((screenWidth,screenHeight))
        self.displaySurface = surface
        self.setupLevel()
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

        for y in range(0,8):
            for x in range(0,16):
                image = pygame.image.load("graphics/Background/Brown.png").convert_alpha()
                image = pygame.transform.scale(image,(screenWidth/16,screenHeight/8))
                self.backgroundSurface.blit(image, (screenWidth/16 * x,screenHeight/8 * y), area=None)

        tmx_data = load_pygame('mapLevel1.tmx')
        self.sprite_group = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        # cycle through all layers
        for layer in tmx_data.visible_layers:
            # if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
            if hasattr(layer,'data'):
                for x,y,surf in layer.tiles():
                    pos = (x * 64, y * 48)
                    Tile(pos = pos, width = 64, height = 48, surf = surf, groups = self.sprite_group)
        
        self.spawnPosition=(500,500)
        playerSprite = Player((500,500))
        self.player.add(playerSprite)



                    

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

        for sprite in self.sprite_group.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.currentX = player.rect.right

        for sprite in self.sprite_group.sprites():
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

        for sprite in self.sprite_group.sprites():
            if sprite.rect.colliderect(player.rect) == True:
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
        
        for sprite in self.sprite_group.sprites():
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
        enemyCollisionsTop = pygame.sprite.spritecollide(self.player.sprite,self.enemy,False)
        enemyCollisionsSide = pygame.sprite.spritecollide(self.player.sprite,self.enemy,False)
        if enemyCollisionsTop:
            for thisEnemy in enemyCollisionsTop:
                enemyCenter = thisEnemy.rect.centery
                enemyTop = thisEnemy.rect.top
                playerBottom = self.player.sprite.rect.bottom
                if enemyTop < playerBottom < enemyCenter and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    (x,y) = thisEnemy.rect.topleft
                    thisEnemy.kill()
                    explosionSprite = Explosion((x,y),64)
                    self.explosion.add(explosionSprite)
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
        for enemy in self.enemy.sprites():
            if pygame.sprite.spritecollide(enemy,self.tiles,False) or pygame.sprite.spritecollide(enemy,self.hiddenBlocks,False):
                enemy.reverse()

    def playerCoinCollisionCheck(self):
        coinCollisions = pygame.sprite.spritecollide(self.player.sprite,self.coin,False)
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
        

        

        self.horizontalMovementCollision()
        self.verticalMovementCollision()

        self.sprite_group.draw(self.levelSurface)

        self.player.update(self.playerHealth)
        self.player.draw(self.levelSurface)


        
        self.displaySurface.blit(self.levelSurface,(0,0),area=(self.player.sprite.rect.topleft[0]-(screenWidth/2),0,screenWidth,screenHeight))

        self.levelSurface.fill('black')


        
        
      

        




