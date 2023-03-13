import pygame
import math

from constantes import *
from mapa import *

class Player:
    def __init__(self):
        self.x = 75
        self.y = 146
        self.xvel = 4.25
        self.yvel = 4.25

        self.width = 30
        self.height = 30

        self.target = self
        self.dist = 99999
        self.fitness = 0

        self.colidiu = False
        self.win = False

        self.surface = pygame.image.load('img/player.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))
        self.rect = self.surface.get_rect(center = (self.x, self.y))
    
    def draw(self, win):
        self.rect = self.surface.get_rect(center = (self.x, self.y))
        win.blit(self.surface, self.rect)

    def move_up(self):
        self.y -= self.yvel
            
    def move_down(self):
        self.y += self.yvel

    def move_left(self):
        self.x -= self.xvel

    def move_right(self):
        self.x += self.xvel    

    def colisaoParedes(self, mapa):
        for parede in mapa.paredes:
            if self.rect.colliderect(parede.rect):

                if parede.index == 's':
                    self.y += self.yvel

                if parede.index == 'i':
                    self.y -= self.yvel

                if parede.index == 'e':
                    self.x += self.xvel

                if parede.index == 'd':
                    self.x -= self.xvel

    def colisaoBolas(self, bolas):
        for b in bolas:
            if self.rect.colliderect(b.rect):
                self.colidiu = True

    def colisaoWin(self, area):
        if self.rect.colliderect(area.rect):
            self.win = True

    def targetInfo(self, win, area, lines=False, dist=False):
        self.target = area

        self.dist = math.dist([self.x, self.y], [self.target.x, self.target.y])

        if lines:
            pygame.draw.line(win, RED, (self.x, self.y), (self.target.x, self.target.y))

        if dist:
            Xm = ((self.x + self.target.x) / 2) - 15
            Ym = ((self.y + self.target.y) / 2) - 15

            dist_text = DIST_FONT.render("d: " +  "{:.2f}".format(self.dist), 1, (0, 0, 0, 191))
            win.blit(dist_text, (Xm, Ym))

class Bola:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.vel = 4
        self.tipo = tipo
        self.count = 0

        self.surface = pygame.image.load('img/bola.png').convert_alpha()
        self.rect = self.surface.get_rect(center = (self.x, self.y))
    
    def draw(self, win):
        self.rect = self.surface.get_rect(center = (self.x, self.y))
        win.blit(self.surface, self.rect)
    
    def move(self):
        self.count += self.vel

        if self.tipo % 2 == 1:
            self.x += self.vel
            if self.x + self.vel >= 665 or self.x + self.vel <= 235 and self.count != 0:
                self.count = 0
                self.vel *= -1
        else:
            self.x -= self.vel
            if self.x - self.vel >= 665 or self.x - self.vel <= 235 and self.count != 0:
                self.count = 0
                self.vel *= -1
