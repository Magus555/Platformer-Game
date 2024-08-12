import pygame 

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		
		self.idleFrames = []
		for i in range(1,6):
			self.idleFrames.append(pygame.image.load('graphics/character/idle/'+str(i)+'.png'))

		self.runFrames = []
		for i in range(1,7):
			self.runFrames.append(pygame.image.load('graphics/character/run/'+str(i)+'.png'))

		self.jumpFrames = []
		for i in range(1,4):
			self.jumpFrames.append(pygame.image.load('graphics/character/jump/'+str(i)+'.png'))

		self.fallFrame = pygame.image.load('graphics/character/fall/fall.png')
		self.loopIndex = 0
		self.frameIndex = 0
		self.animationSpeed = 150
		self.image = pygame.image.load('graphics/character/idle/1.png')
		self.flippedImage = pygame.transform.flip(self.image,True,False)
		self.rect = self.image.get_rect(bottomleft = pos)
		self.flipped = 1
		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16
		self.lastUpdate = 0
		self.onGround = False

	def imageFlipped(self,playerHealth):


		if self.flipped == 0:
			self.image = pygame.transform.flip(self.image,True,False)
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
			self.loopIndex = 6
			self.image = self.runFrames[self.frameIndex]
		elif keys[pygame.K_a]:
			self.direction.x = -1
			self.flipped = 0
			self.loopIndex = 6
			self.image = self.runFrames[self.frameIndex]
		else:
			self.direction.x = 0
			self.loopIndex=5
			if self.frameIndex > 4 : self.frameIndex = 0
			self.image = self.idleFrames[self.frameIndex]

		if keys[pygame.K_w] and self.onGround:
			self.jump()
			self.onGround = False
			
		if self.direction.y < 0:
			self.loopIndex = 3
			if self.frameIndex > 2 : self.frameIndex = 0
			self.image = self.jumpFrames[self.frameIndex]
		
		elif self.onGround == False:
			self.image = self.fallFrame



	def applyGravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def jump(self):
		self.direction.y = self.jump_speed

	def frameIncrementer(self):
		currentTime = pygame.time.get_ticks()
		if currentTime - self.lastUpdate > self.animationSpeed:
			self.frameIndex += 1
			if self.frameIndex >= self.loopIndex: self.frameIndex = 0
			self.lastUpdate = currentTime

	def update(self,playerHealth):
		self.frameIncrementer()
		self.getInput()
		self.imageFlipped(playerHealth)
	
		