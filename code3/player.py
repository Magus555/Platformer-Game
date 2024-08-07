import pygame 

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = pygame.image.load('graphics/character/idle/1.png')
		self.flippedImage = pygame.transform.flip(self.image,True,False)
		self.rect = self.image.get_rect(bottomleft = pos)
		self.flipped = 1
		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16

	def imageFlipped(self,playerHealth):

		if self.flipped == 1:
			self.image = pygame.image.load('graphics/character/idle/1.png')
		elif self.flipped == 0:
			self.image = pygame.transform.flip(pygame.image.load('graphics/character/idle/1.png'),True,False)
		if playerHealth==1:
			width=(self.image.get_size()[0])
			height=(self.image.get_size()[1])
			self.image=pygame.transform.scale(self.image,(width*0.75,height*.75))
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		if playerHealth == 2:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		
	def getInput(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_d]:
			self.direction.x = 1
			self.flipped = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
			self.flipped = 0
		else:
			self.direction.x = 0

		if keys[pygame.K_w] and self.onGround:
			self.jump()
			self.onGround = False

	def applyGravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed


	def update(self,playerHealth):
		self.getInput()
		self.imageFlipped(playerHealth)

		