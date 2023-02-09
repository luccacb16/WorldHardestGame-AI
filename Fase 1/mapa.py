import pygame

from constantes import *
from entidades import *

class Win:
    def __init__(self, x, y, width, height): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(topleft = (self.x, self.y))   

class Parede:
    def __init__(self, x, y, width, height, index):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = index

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(topleft = (self.x, self.y))

    def draw(self, win):
        win.blit(self.rect, self.rect)

class Mapa:
    def __init__(self):
        #self.parede = Parede(x, y, width, height, index)

        self.parede1 = Parede(15, 78, 6, 294, 'e')
        self.parede2 = Parede(255, 318, 437, 6, 'i')
        self.parede3 = Parede(207, 126, 437, 6, 's')
        self.parede4 = Parede(15, 366, 245, 6, 'i')
        self.parede5 = Parede(15, 78, 150, 6, 's')
        self.parede6 = Parede(879, 78, 6, 294, 'd')
        self.parede7 = Parede(159, 78, 6, 245, 'd')
        self.parede8 = Parede(159, 318, 53, 6, 's')
        self.parede8 = Parede(255, 318, 6, 53, 'd')
        self.parede9 = Parede(639, 78, 6, 53, 'e')
        self.parede10 = Parede(639, 78, 245, 6, 's')
        self.parede11 = Parede(207, 126, 6, 197, 'e')
        self.parede12 = Parede(687, 126, 6, 197, 'd')
        self.parede13 = Parede(687, 126, 53, 6 , 'i')
        self.parede14 = Parede(159, 318, 53, 6, 's')
        self.parede15 = Parede(735, 126, 6, 245, 'e')
        self.parede16 = Parede(735, 366, 149, 6, 'i')

        self.paredes = [self.parede1, self.parede2, self.parede3, 
                            self.parede4, self.parede5, self.parede6,
                            self.parede7, self.parede8, self.parede9,
                            self.parede10, self.parede11, self.parede12,
                            self.parede13, self.parede14, self.parede15, self.parede16]