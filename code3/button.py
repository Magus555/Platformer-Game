import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        function = False
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                function = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return function

class textButton():
    def __init__(self, x, y, text, textScaleX, textScaleY):
        i=0
        image = pygame.image.load('graphics/buttons/reusable.png')
        height = image.get_height()
        
        image = pygame.transform.scale(image, (len(text)*8*textScaleX + len(text)*8*textScaleX/2.5, int(height*textScaleY)))
        textImage = pygame.image.load('graphics/Menu/Text/Text (White) (8x10).png')
        self.buttonSurface = pygame.Surface((image.get_width(),image.get_height()))
        self.buttonSurface.blit(image,(0,0))
        for letter in text:
            asciiVal = ord(letter)
            if 64<asciiVal<91:
                asciiVal -= 64
            elif 96<asciiVal<123:
                asciiVal -= 96
            elif asciiVal == 32:
                asciiVal = 27
            elif 47<asciiVal<58:
                asciiVal -= 16
            letterRow = (asciiVal-1)//10
            letterColumn = (asciiVal-1)%10
            if(asciiVal==20): print("trigger", letterRow, letterColumn)
            self.buttonSurface.blit(pygame.transform.scale(textImage, (int(textImage.get_width() * textScaleX), int(textImage.get_height() * textScaleY))),(i*8*textScaleX + self.buttonSurface.get_width()/7,self.buttonSurface.get_height()/5),area=(letterColumn*8*textScaleX,letterRow*10*textScaleY,8*textScaleX,10*textScaleY))
            i+=1



        self.rect = self.buttonSurface.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, surface):
        function = False
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                function = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.buttonSurface, (self.rect.x, self.rect.y))

        return function
