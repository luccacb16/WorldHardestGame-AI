import pygame

global tempo_max
tempo_max = 12

WIDTH = 950
HEIGHT = 375

FPS = 60

FUNDO = (180, 181, 254)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (66, 179, 245)
YELLOW = (141, 122, 23)

pygame.font.init()
STAT_FONT = pygame.font.Font(None, 32)
VIVOS_FONT = pygame.font.Font(None, 32)
GANHARAM_FONT = pygame.font.Font(None, 32)
TEMPO_FONT = pygame.font.Font(None, 32)
ATW_FONT = pygame.font.Font(None, 32)
DIST_FONT = pygame.font.Font(None, 18)