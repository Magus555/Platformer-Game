import pygame 

class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()

        self.loopIndex = 0
        self.frameIndex = 0
        self.animationSpeed = 50
        self.idleFrames = pygame.image.load('graphics/character/Idle (32x32).png')
        self.fallFrames = pygame.image.load('graphics/character/Fall (32x32).png')
        self.jumpFrame = pygame.image.load('graphics/character/Jump (32x32).png')
        self.runFrames = pygame.image.load('graphics/character/Run (32x32).png')
        self.image = self.getImage(self.idleFrames,1)
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

    def getImage(self,sheet,imageNum):
        scale = 2
        image = pygame.Surface((32, 32)).convert_alpha()
        image.blit(sheet, (0,0), (32 * imageNum, 0, 32, 32))
        image = pygame.transform.scale(image, ((32) * scale, 32 * scale))
        image.set_colorkey((0,0,0))

        return image

    def imageFlipped(self,playerHealth):


        if self.flipped == 0:
            self.image = pygame.transform.flip(self.image,True,False)
            self.image.set_colorkey((0,0,0))
        if playerHealth==1:
            width=(self.image.get_size()[0])
            height=(self.image.get_size()[1])
            self.image=pygame.transform.scale(self.image,(width*0.75,height*.75))
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        if playerHealth == 2:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        
    def getInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.flipped = 1
            if self.frameIndex > 11 : self.frameIndex = 0
            self.image = self.getImage(self.runFrames,self.frameIndex)
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.flipped = 0
            if self.frameIndex > 11 : self.frameIndex = 0
            self.image = self.getImage(self.runFrames,self.frameIndex)
        else:
            self.direction.x = 0
            if self.frameIndex > 10 : self.frameIndex = 0
            self.image = self.getImage(self.idleFrames,self.frameIndex)

        if keys[pygame.K_w] and self.onGround:
            self.jump()
            self.onGround = False
            
        if self.direction.y < 0:
            self.image = self.getImage(self.jumpFrame,0)
        
        elif self.onGround == False:
            self.image = self.fallFrames
            self.image = self.getImage(self.fallFrames,0)


    def getPos(self):
        return (self.rect.x,self.rect.y)


    def applyGravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def frameIncrementer(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastUpdate > self.animationSpeed:
            self.frameIndex += 1
            self.lastUpdate = currentTime

    def update(self,playerHealth):
        self.frameIncrementer()
        self.getInput()
        self.imageFlipped(playerHealth)

        