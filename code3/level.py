import pygame, sys
from tiles import Tile 
from settings import *
from player import Player
from enemy import Enemy, Coin, Flag

class Level:
	def __init__(self,levelData,surface):
		
		self.finishState = False
		self.levelComplete = 0
		self.lives = 0
		self.score = 0
		self.displaySurface = surface 
		self.setupLevel(levelData)
		self.worldShift = 0
		self.currentX = 0
		self.playerHealth = 2
		self.hitCD = 0
		self.currentClock = 0
		self.coinCount = 0
		self.timeOfHit = 1000000000000000000000000000000000000000000000000000000000

	def setupLevel(self,layout):
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.enemy = pygame.sprite.Group()
		self.coin = pygame.sprite.Group()
		self.flag = pygame.sprite.GroupSingle()
		self.hidden = pygame.sprite.Group()
		self.bricks = pygame.sprite.Group()

		for rowIndex,row in enumerate(layout):
			for colIndex,cell in enumerate(row):
				x = colIndex * (tileSize)
				y = rowIndex * (tileSize)
				if cell == 'X':
					tile = Tile((x,y),64,"grass block.png")
					self.tiles.add(tile)
				if cell == 'Y':
					tile = Tile((x,y),64,"desert block.png")
					self.tiles.add(tile)
				if cell == 'Z':
					tile = Tile((x,y),64,"alien block.png")
					self.tiles.add(tile)
				if cell == 'B':
					tile = Tile((x,y),64,"brick block.png")
					self.bricks.add(tile)
				if cell == 'H':
					tile = Tile((x,y),64,"grass block.png")
					self.hidden.add(tile)
				if cell == 'P':
					playerSprite = Player((x,y))
					self.player.add(playerSprite)
				if cell == 'E':
					enemySprite = Enemy((x,y),64)
					self.enemy.add(enemySprite)
				if cell == 'C':
					coinSprite = Coin((x,y),64)
					self.coin.add(coinSprite)				
				if cell == 'F':
					flagSprite = Flag((x,y),64)
					self.flag.add(flagSprite)

	def scrollX(self):
		player = self.player.sprite
		playerX = player.rect.centerx
		directionX = player.direction.x

		if playerX < 1920 / 4 and directionX < 0:
			self.worldShift = 8
			player.speed = 0
		elif playerX > 1920 - (1920 / 4) and directionX > 0:
			self.worldShift = -8
			player.speed = 0
		else:
			self.worldShift = 0
			player.speed = 8

	def horizontalMovementCollision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					self.currentX = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					self.currentX = player.rect.right

		for sprite in self.bricks.sprites():
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

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect) == True:
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.onGround = True
				if player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
		
		for sprite in self.bricks.sprites():
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
			for enemy in enemyCollisionsTop:
				enemyCenter = enemy.rect.centery
				enemyTop = enemy.rect.top
				playerBottom = self.player.sprite.rect.bottom
				if enemyTop < playerBottom < enemyCenter and self.player.sprite.direction.y >= 0:
					self.player.sprite.direction.y = -15
					enemy.kill()
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
						self.player.sprite.rect.x=(screenWidth / 2)
						self.player.sprite.rect.y=(screenHeight / 2)
						self.lives = self.lives-1
						self.playerHealth = 2

	def enemyCollisionReverse(self):
		for enemy in self.enemy.sprites():
			if pygame.sprite.spritecollide(enemy,self.tiles,False) or pygame.sprite.spritecollide(enemy,self.hidden,False):
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

		self.tiles.update(self.worldShift)
		self.tiles.draw(self.displaySurface)
		self.scrollX()
		self.hidden.update(self.worldShift)
		self.hidden.draw(self.displaySurface)
		self.bricks.update(self.worldShift)
		self.bricks.draw(self.displaySurface)

		self.enemyCollisionReverse()
		self.playerEnemyCollisionCheck()
		self.enemy.update(self.worldShift)
		self.enemy.draw(self.displaySurface)

		self.coin.update(self.worldShift)
		self.coin.draw(self.displaySurface)

		self.flag.update(self.worldShift)
		self.flag.draw(self.displaySurface)

		self.player.update(self.playerHealth)
		self.horizontalMovementCollision()

		self.verticalMovementCollision()
		self.player.draw(self.displaySurface)
		self.playerCoinCollisionCheck()
		self.playerFlagCollisionCheck()

		


