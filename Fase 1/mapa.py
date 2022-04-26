import pygame

from constantes import *
from player import *
from bola import *

class Win:
    def __init__(self):
        self.x = 738
        self.y = 84
        self.width = 1
        self.height = 42
        
        self.win_surface = pygame.Surface((self.width, self.height))
        self.win_rect = self.win_surface.get_rect(topleft = (self.x, self.y))
    
    def getx(self):
        return self.x

    def gety(self):
        return self.y    

class Parede:
    def __init__(self, x, y, width, height, index):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = index

        self.parede_surface = pygame.Surface((self.width, self.height))
        self.parede_rect = self.parede_surface.get_rect(topleft = (self.x, self.y))

    def draw(self, win):
        win.blit(self.parede_surface, self.parede_rect)

class Mapa:
    def __init__(self):
        pass
        self.lista_paredes = []
        self.lista_rects = []
    
    def paredes(self):
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

        self.lista_paredes = [self.parede1, self.parede2, self.parede3, 
                            self.parede4, self.parede5, self.parede6,
                            self.parede7, self.parede8, self.parede9,
                            self.parede10, self.parede11, self.parede12,
                            self.parede13, self.parede14, self.parede15, self.parede16]
        
        self.lista_rects = [self.parede1.parede_rect, self.parede2.parede_rect, self.parede3.parede_rect, 
                            self.parede4.parede_rect, self.parede5.parede_rect, self.parede6.parede_rect,
                            self.parede7.parede_rect, self.parede8.parede_rect, self.parede9.parede_rect,
                            self.parede10.parede_rect, self.parede11.parede_rect, self.parede12.parede_rect,
                            self.parede13.parede_rect, self.parede14.parede_rect, self.parede15.parede_rect, self.parede16.parede_rect]