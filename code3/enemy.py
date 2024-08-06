import pygame
from tiles import Tile
from random import randint

class Enemy(Tile):
	def __init__(self,pos,size):
		super().__init__(pos,size,'2.png')
		self.rect = self.image.get_rect(topleft = pos)
		self.speed = randint(1,2)

	def move(self):
		self.rect.x += self.speed

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	def reverse(self):
		self.speed *= -1

	def update(self,shift):
		self.rect.x += shift
		self.move()

class Coin(Tile):
	def __init__(self,pos,size):
		super().__init__(pos,size,'coin.png')
		self.rect = self.image.get_rect(topleft = pos)

class Flag(Tile):
	def __init__(self,pos,size):
		super().__init__(pos,size,'End (Idle).png')
		self.rect = self.image.get_rect(topleft = pos)

