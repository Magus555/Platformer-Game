from queue import Queue
import time
import pygame, sys
from settings import * 
from level import Level
from UI import Text
import button
import threading
import os


pygame.init()
screenWidth = pygame.display.Info().current_w
screenHeight = pygame.display.Info().current_h
screen = pygame.display.set_mode((screenWidth,screenHeight))
clock = pygame.time.Clock()

startImg = pygame.image.load('graphics/Menu/Buttons/Play.png').convert_alpha()
exitImg = pygame.image.load('graphics/Menu/Buttons/Levels.png').convert_alpha()
thirdImg = pygame.image.load('graphics/Menu/Buttons/Settings.png').convert_alpha()
backImg = pygame.image.load('graphics/Menu/Buttons/Back.png').convert_alpha()

playButton = button.Button((screenWidth/2), (screenHeight/4), startImg, 5)
levelSelectButton = button.Button((screenWidth/2), ((screenHeight*2)/4), exitImg, 5)
settingsButton = button.Button((screenWidth/2), ((screenHeight*3)/4), thirdImg, 5)
backButton = button.Button((screenWidth*0.9), ((screenHeight*3)/4), backImg, 5)

levelButtonImages = []
for i in range(1,4): levelButtonImages.append(pygame.image.load('graphics/Menu/Levels/0'+str(i)+'.png').convert_alpha())

lockedLevelButtonImages = []
for i in range(1,4): lockedLevelButtonImages.append(pygame.image.load('graphics/Menu/Levels/0'+str(i)+'g.png').convert_alpha())

firstButton = button.Button((screenWidth/4), (screenHeight/3), levelButtonImages[0], 5)
secondButton = button.Button((screenWidth/4*2), (screenHeight/3), levelButtonImages[1], 5)
thirdButton = button.Button((screenWidth/4*3), (screenHeight/3), levelButtonImages[2], 5)

lockedFirstButton = button.Button((screenWidth/4), (screenHeight/3), lockedLevelButtonImages[0], 5)
lockedSecondButton = button.Button((screenWidth/4*2), (screenHeight/3), lockedLevelButtonImages[1], 5)
lockedThirdButton = button.Button((screenWidth/4*3), (screenHeight/3), lockedLevelButtonImages[2], 5)

resolutionButton = button.textButton((screenWidth/2), (screenHeight/4),"resolution",5,5)

hostButton = button.textButton((screenWidth/4),(screenHeight/4),"Host Multiplayer",5,5)
clientButton = button.textButton((screenWidth/4),(screenHeight/3),"Join Multiplayer",5,5)

def saveCheck():
    try:
        saveData = open("saveData.txt","rt")
        saveData.close()
    except:
        saveData = open("saveData.txt","wt")
        saveData.write(str(0)+('\n')+str(5)+('\n')+str(1)+('\n')+str(0)+('\n')+str(0))
        saveData.close()
    saveData = open("saveData.txt","rt")
    saveData = saveData.read()
    saveData = saveData.splitlines()

    return(saveData)

def saveUpdate(coinCount,lives,level):
    saveData = open("saveData.txt","rt")
    placeHolderList = saveData.readlines()
    placeHolderList[0] = (str(coinCount)+('\n'))
    placeHolderList[1] = (str(lives)+('\n'))
    if level == 1:
        placeHolderList[3] = (str(1)+('\n'))
    if level == 2:
        placeHolderList[4] = (str(1)+('\n'))
    saveData = open("saveData.txt","wt")
    saveData.writelines(placeHolderList)
    saveData.close()

def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if playButton.draw(screen):
            level = Level(1,screen)
            game(level)
            saveUpdate(level.coinCount,level.lives,1)
        if levelSelectButton.draw(screen):
            levelSelect()
        if settingsButton.draw(screen):
            settings()
        if hostButton.draw(screen):
            connected = Queue()
            level = Level(1,screen)
            level.levelServer(connected)
            screen.fill('black')
            screen.blit(Text(("Waiting for player to join")), (50,50))
            pygame.display.update()
            while(connected.empty()!=False):
                pass
            game(level)
            saveUpdate(level.coinCount,level.lives,1)
        if clientButton.draw(screen):
            level = Level(1,screen)
            level.clientJoinServer()
            game(level)
            saveUpdate(level.coinCount,level.lives,1)
        pygame.display.update()

def levelSelect():
    screen.fill('black')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if (int(saveCheck()[2])) == 1:
            if firstButton.draw(screen):
                level = Level(1,screen)
                game(level)
                saveUpdate(level.coinCount,level.lives,1)
        else:
            lockedFirstButton.draw(screen)
        if (int(saveCheck()[3])) == 1:
            if secondButton.draw(screen):
                level = Level(2,screen)
                game(level)
                saveUpdate(level.coinCount,level.lives,2)
        else:
            lockedSecondButton.draw(screen)
        if (int(saveCheck()[4])) == 1:
            if thirdButton.draw(screen):
                level = Level(3,screen)
                game(level)
                saveUpdate(level.coinCount,level.lives,0) 
        else:
            lockedThirdButton.draw(screen)
        
        if backButton.draw(screen):
            screen.fill('black')
            break


        pygame.display.update()
        screen.fill('black')

def settings():
    screen.fill('black')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if resolutionButton.draw(screen):
            print("filler, scaling should be added last so i can add features without worrying about it, less work overall")



        if backButton.draw(screen):
            screen.fill('black')
            break

        pygame.display.update()
        screen.fill('black')
    
def game(level):
    startTicks=pygame.time.get_ticks()
    timeDeath = 0
    level.coinCount = int(saveCheck()[0])
    level.lives = int(saveCheck()[1])

    while level.finishState == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        seconds=(pygame.time.get_ticks()-startTicks)/1000
        timer=int(401-seconds)
        if timer == 0 and timeDeath == 0:
            level.lives = level.lives - 1
            timeDeath = 1
        level.currentClock = seconds
        screen.fill('black')

        level.run()


        screen.blit(Text(("Lives: "+str(level.lives))), (50,50))
        screen.blit(Text(str(timer)),(2400,50))
        screen.blit(Text("Coins: "+str(level.coinCount)),(50,100))
        screen.blit(Text("Score: "+str(level.score)),(2200,50))

        pygame.display.update()
        clock.tick(60)



    screen.fill('black')

menu()