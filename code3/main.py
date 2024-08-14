import pygame, sys
from settings import * 
from level import Level
from UI import Text
import button

pygame.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
clock = pygame.time.Clock()

startImg = pygame.image.load('graphics/Menu/Buttons/Play.png').convert_alpha()
exitImg = pygame.image.load('graphics/Menu/Buttons/Levels.png').convert_alpha()
thirdImg = pygame.image.load('graphics/Menu/Buttons/Settings.png').convert_alpha()
backImg = pygame.image.load('graphics/Menu/Buttons/Back.png').convert_alpha()

levelButtonImg1 = pygame.image.load('graphics/Menu/Levels/01.png').convert_alpha()
levelButtonImg2 = pygame.image.load('graphics/Menu/Levels/02.png').convert_alpha()
levelButtonImg3 = pygame.image.load('graphics/Menu/Levels/03.png').convert_alpha()

lockedLevelButtonImg1 = pygame.image.load('graphics/Menu/Levels/01g.png').convert_alpha()
lockedLevelButtonImg2 = pygame.image.load('graphics/Menu/Levels/02g.png').convert_alpha()
lockedLevelButtonImg3 = pygame.image.load('graphics/Menu/Levels/03g.png').convert_alpha()

playButton = button.Button((screenWidth/2), (screenHeight/4), startImg, 5)
levelSelectButton = button.Button((screenWidth/2), ((screenHeight*2)/4), exitImg, 5)
settingsButton = button.Button((screenWidth/2), ((screenHeight*3)/4), thirdImg, 5)
backButton = button.Button((screenWidth*0.9), ((screenHeight*3)/4), backImg, 5)

firstButton = button.Button((screenWidth/4), (screenHeight/3), levelButtonImg1, 5)
secondButton = button.Button((screenWidth/4*2), (screenHeight/3), levelButtonImg2, 5)
thirdButton = button.Button((screenWidth/4*3), (screenHeight/3), levelButtonImg3, 5)

lockedFirstButton = button.Button((screenWidth/4), (screenHeight/3), lockedLevelButtonImg1, 5)
lockedSecondButton = button.Button((screenWidth/4*2), (screenHeight/3), lockedLevelButtonImg2, 5)
lockedThirdButton = button.Button((screenWidth/4*3), (screenHeight/3), lockedLevelButtonImg3, 5)

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
            level = Level((levelMap1),screen)
            game(level)
            saveUpdate(level.coinCount,level.lives,1)
        if levelSelectButton.draw(screen):
            level = Level((levelMap1),screen)
            levelSelect(level)
        if settingsButton.draw(screen):
            print("third")

        pygame.display.update()

def levelSelect(level):
    screen.fill('black')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if (int(saveCheck()[2])) == 1:
            if firstButton.draw(screen):
                level = Level((levelMap1),screen)
                game(level)
                saveUpdate(level.coinCount,level.lives,1)
        else:
            lockedFirstButton.draw(screen)
        if (int(saveCheck()[3])) == 1:
            if secondButton.draw(screen):
                level = Level((levelMap2),screen)
                game(level)
                saveUpdate(level.coinCount,level.lives,2)
        else:
            lockedSecondButton.draw(screen)
        if (int(saveCheck()[4])) == 1:
            if thirdButton.draw(screen):
                level = Level((levelMap3),screen)
                game(level)
                saveUpdate(level.coinCount,level.lives,0)
        else:
            lockedThirdButton.draw(screen)
        
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
        screen.blit(Text(("Lives: "+str(level.lives))), (50,50))
        screen.blit(Text(str(timer)),(1700,50))
        screen.blit(Text("Coins: "+str(level.coinCount)),(50,100))
        screen.blit(Text("Score: "+str(level.score)),(1500,50))
        level.run()

        pygame.display.update()
        clock.tick(500)



    screen.fill('black')

menu()