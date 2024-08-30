import pygame, sys
from pytmx import load_pygame
from tiles import Tile, backgroundTile, Coin, Flag
from settings import *
from player import Player
from entities import Enemy, Explosion
import threading
from queue import Queue
from server import Server
from client import *
import time


class Level:
    def __init__(self,levelNum,surface):

        self.screenWidth = pygame.display.Info().current_w
        self.screenHeight = pygame.display.Info().current_h
        self.multiplayer = False
        self.levelNum = levelNum
        self.finishState = False
        self.levelComplete = 0
        self.lives = 0
        self.score = 0
        self.displaySurface = surface
        self.backgroundSurface = pygame.Surface((self.screenWidth+1000,self.screenHeight))
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
        self.background_y = self.screenHeight
        
    def setupLevel(self):

        self.levelSize = [0,0]



        tmx_data = load_pygame('mapLevel'+str(self.levelNum)+'.tmx')
        self.tileGroup = pygame.sprite.Group()
        self.enemyGroup = pygame.sprite.Group()
        self.coinGroup = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.otherPlayer = pygame.sprite.GroupSingle()
        self.flag = pygame.sprite.GroupSingle()
        self.explosionGroup = pygame.sprite.GroupSingle()



        for y in range(0,9):
            for x in range(0,17):
                image = pygame.image.load("graphics/Background/Brown.png").convert_alpha()
                image = pygame.transform.scale(image,(self.screenWidth/16,self.screenHeight/8))
                self.backgroundSurface.blit(image, (self.screenWidth/16 * x,self.screenHeight/8 * y), area=None)

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

    def levelServer(self,connected):
        self.multiplayer = True
        self.playerNum = 1
        self.q = Queue()
        print("now hosting")
        self.hostServer = Server()
        self.otherPlayer.add(Player(self.player.sprite.getPos()))
        serverThread = threading.Thread(target=self.hostServer.startServer, name='serverThread',args = (self.player.sprite, self.otherPlayer.sprite, connected, ))
        serverThread.start()



    def clientJoinServer(self,connected):
        self.multiplayer = True
        self.playerNum = 2
        self.q = Queue()
        print("now joining")
        self.clientNetwork = Network(connected)
        self.otherPlayer.add(Player(self.player.sprite.getPos()))
        clientThread = threading.Thread(target=self.clientNetwork.connect, name='clientThread',args=(self.player.sprite,  self.otherPlayer.sprite))
        clientThread.start()
        self.clientNetwork.send('this is a big fat message')



    def otherPlayerSetPosition(self,x,y):
        self.otherPlayer.sprite.rect.center = (x,y)


    def backgroundScrolling(self):
        self.scroll_y += 1
        self.background_y += 1

        self.levelSurface.blit(self.backgroundSurface, (self.player.sprite.rect.topleft[0]-(self.screenWidth/2), self.scroll_y))
        self.levelSurface.blit(self.backgroundSurface, (self.player.sprite.rect.topleft[0]-(self.screenWidth/2), self.background_y))

        if self.scroll_y >= self.screenHeight:
            self.scroll_y = -self.screenHeight+1

        if self.background_y >= self.screenHeight:
            self.background_y = -self.screenHeight+1


 
                    

    def scrollX(self):
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x

        if playerX < self.screenWidth / 4 and directionX < 0:
            self.worldShift = 8
            player.speed = 0
            self.spawnDistance += 8
        elif playerX > self.screenWidth - (self.screenWidth / 4) and directionX > 0:
            self.worldShift = -8
            player.speed = 0
            self.spawnDistance -= 8
        else:
            self.worldShift = 0
            player.speed = 8
    





    
    def respawn(self,player):
        player.rect.x=self.spawnPosition[0]
        player.rect.y=self.spawnPosition[1]
        self.lives = self.lives-1
        self.worldShift=-self.spawnDistance
        self.spawnDistance=0
        self.playerHealth = 2

    def fallOutOfBounds(self,player):
        playerY = player.rect.centery
        if playerY > self.screenHeight:
            self.respawn(player)

    def horizontalMovementCollision(self,player):
        player.rect.x += player.direction.x * player.speed


        for sprite in self.tileGroup.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.currentX = player.rect.right
                    
    def verticalMovementCollision(self,player):
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
        
    
    def enemyVerticalCollision(self):

        for enemy in self.enemyGroup.sprites():
            enemy.applyGravity()
            for sprite in self.tileGroup.sprites():
                if sprite.rect.colliderect(enemy.rect) == True:
                    if enemy.direction.y > 0: 
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
                        enemy.onGround = True
                    if enemy.direction.y < 0:
                        enemy.rect.top = sprite.rect.bottom
                        enemy.direction.y = 0

    def enemyCollisionReverse(self):
        
        for sprite in self.tileGroup.sprites():
            for enemy in self.enemyGroup.sprites():
                if sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.x < 0: 
                        enemy.rect.left = sprite.rect.right
                        self.currentX = enemy.rect.left
                        enemy.reverse()
                    elif enemy.direction.x > 0:
                        enemy.rect.right = sprite.rect.left
                        self.currentX = enemy.rect.right
                        enemy.reverse()
    def playerEnemyCollisionCheck(self,player):
        if self.currentClock>=self.timeOfHit+2:
            self.timeOfHit=10000000000000000000
            self.hitCD = 0
        enemyCollisionsTop = pygame.sprite.spritecollide(player,self.enemyGroup,False)
        enemyCollisionsSide = pygame.sprite.spritecollide(player,self.enemyGroup,False)
        if enemyCollisionsTop:
            for thisEnemy in enemyCollisionsTop:
                enemyCenter = thisEnemy.rect.centery
                enemyTop = thisEnemy.rect.top
                playerBottom = player.rect.bottom
                if enemyTop < playerBottom < enemyCenter and player.direction.y >= 0:
                    player.direction.y = -15
                    (x,y) = thisEnemy.rect.topleft
                    thisEnemy.kill()
                    Explosion((x,y),64,self.explosionGroup)
                    self.score = self.score + 50

        if enemyCollisionsSide:
            for enemy in enemyCollisionsSide:
                enemyCenter = enemy.rect.centery
                playerY=self.player.sprite.rect.centery

                if enemyCenter<=playerY and self.hitCD == 0:
                    self.playerHealth=self.playerHealth - 1
                    self.hitCD=1
                    self.timeOfHit=self.currentClock

                    if self.playerHealth == 0:
                        self.respawn(player)



                    
    def playerCoinCollisionCheck(self,player):
        coinCollisions = pygame.sprite.spritecollide(player,self.coinGroup,False)
        if coinCollisions:
            for coin in coinCollisions:
                self.coinCount=(self.coinCount+1)
                self.playerHealth=2
                coin.kill()
        
    def playerFlagCollisionCheck(self,player):
        flagCollisions = pygame.sprite.spritecollide(player,self.flag,False)
        if flagCollisions:
            self.finishState = True


    def sendAndReceiveCoordinates(self):
        while(True):
            if (self.multiplayer == True and self.playerNum == 2):
                print(self.clientNetwork.connect())
                time.sleep(1)

##        if self.multiplayer == True:
 #           if(self.q.empty() == False):
  #              string = self.q.get()
   #             print(string)
    #            if((string.split('(')[0]=='Player2' and self.playerNum == 1) or (string.split('(')[0]=='Player1' and self.playerNum == 2)):
     #               x,y=(string.split('(')[1].split(')'))[0][0],(string.split('(')[1].split(')'))[0][2]
      #              self.otherPlayerSetPosition(x,y)
       #             print("THIS TRIGGERED")

            self.q.put('Player'+str(self.playerNum)+'('+str(self.player.sprite.rect.x)+','+str(self.player.sprite.rect.y)+')')

    def sendPlayerLocation(self):
        while True:
            if self.playerNum==1:
                self.hostServer.serverSend(self.player.sprite.getPos())
                time.sleep(1)
            else:
                self.clientNetwork.send(self.player.sprite.getPos())
                time.sleep(1)

    def run(self):
  
        self.levelSurface.fill('black')
            
        if(self.multiplayer==True):
            self.playerEnemyCollisionCheck(self.otherPlayer.sprite)
            self.playerCoinCollisionCheck(self.otherPlayer.sprite)
            self.playerFlagCollisionCheck(self.otherPlayer.sprite)

        self.fallOutOfBounds(self.player.sprite)

        self.enemyCollisionReverse()
        self.enemyVerticalCollision()
        self.playerEnemyCollisionCheck(self.player.sprite)

        self.horizontalMovementCollision(self.player.sprite)
        self.verticalMovementCollision(self.player.sprite)

        self.playerCoinCollisionCheck(self.player.sprite)
        self.playerFlagCollisionCheck(self.player.sprite)

        self.tileGroup.update()

        self.enemyGroup.update()
        
        
        self.explosionGroup.update()
        
        self.coinGroup.update

        self.flag.update()
        
        self.player.update(self.playerHealth)
        if(self.multiplayer==True):
            self.otherPlayer.sprite.otherPlayerUpdate(self.playerHealth)

        self.backgroundScrolling()
       
        self.tileGroup.draw(self.levelSurface)
        self.enemyGroup.draw(self.levelSurface)
        self.explosionGroup.draw(self.levelSurface)
        self.coinGroup.draw(self.levelSurface)
        self.flag.draw(self.levelSurface)
        self.player.draw(self.levelSurface)
        self.otherPlayer.draw(self.levelSurface)
        
        self.displaySurface.blit(self.levelSurface,(0,0),area=(self.player.sprite.rect.topleft[0]-(self.screenWidth/2),0,self.screenWidth,self.screenHeight))

        

        


        
        
      

        




