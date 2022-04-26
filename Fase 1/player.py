import pygame

from constantes import *
from mapa import *
from bola import *

class Player:
    def __init__(self):
        self.x = self.og_x = 75
        self.y = self.og_y = 146
        self.xvel = 4
        self.yvel = 4

        self.colidiu = False
        self.dist = 99999

        self.width = 30
        self.height = 30
        self.border_width = 5

        self.player_surface = pygame.image.load('img/player.png').convert_alpha()
        self.player_rect = self.player_surface.get_rect(center = (self.x, self.y))
    
    def draw(self, win):
        self.player_rect = self.player_surface.get_rect(center = (self.x, self.y))
        win.blit(self.player_surface, self.player_rect)

    def move_up(self):
        self.y -= self.yvel
            
    def move_down(self):
        self.y += self.yvel

    def move_left(self):
        self.x -= self.xvel

    def move_right(self):
        self.x += self.xvel

    def move_stop(self):
        self.x += 0
        self.y += 0    

    def colisao_paredes(self, mapa):
        for parede in mapa.lista_rects:
            i = mapa.lista_rects.index(parede)
            if self.player_rect.colliderect(parede):
                
                if mapa.lista_paredes[i].index == 's':
                    self.y += self.yvel

                if mapa.lista_paredes[i].index == 'i':
                    self.y -= self.yvel

                if mapa.lista_paredes[i].index == 'e':
                    self.x += self.xvel

                if mapa.lista_paredes[i].index == 'd':
                    self.x -= self.xvel

    def reset(self):
        self.x = self.og_x
        self.y = self.og_y
    
    def getx(self):
        return self.x
    
    def gety(self):
        return self.y