import pygame


pygame.font.init()

def Text(word):
    my_font = pygame.font.SysFont('Comic Sans MS', 20)
    text_surface = my_font.render(word, False, (250, 250, 250))
    return text_surface