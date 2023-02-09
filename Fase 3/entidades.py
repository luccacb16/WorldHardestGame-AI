import pygame
import math

from constantes import *
from mapa import *

# PLAYER
class Player:
    def __init__(self):
        self.x = 300
        self.y = 334
        self.xvel = 4
        self.yvel = 4

        self.width = 35
        self.height = 35

        self.target = self
        self.dist = 99999
        self.fitness = 0

        self.moeda = False
        self.colidiu = False
        self.win = False

        self.surface = pygame.image.load('img/player.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (self.width, self.height))
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def draw(self, win):
        self.rect = self.surface.get_rect(center = (self.x, self.y))
        win.blit(self.surface, self.rect)

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

    def move_up(self):
        self.y -= self.yvel

    def move_down(self):
        self.y += self.yvel

    def move_left(self):
        self.x -= self.xvel

    def move_right(self):
        self.x += self.xvel

    def colisaoBolas(self, bolas):
        for b in bolas:
            if self.rect.colliderect(b.rect):
                self.colidiu = True

    def colisaoMoeda(self, moeda):
        if not self.moeda:
            if self.rect.colliderect(moeda.rect):
                self.moeda = True
                self.fitness = 40
        
    def colisaoWin(self, area):
        if self.rect.colliderect(area.rect):
            if self.moeda:
                self.win = True

    def targetInfo(self, win, area, moeda, switch):
        # Linhas
        if not self.moeda: # Sem moeda
            self.target = moeda
            color = GREEN
        else:
            self.target = area
            color = RED
        
        pygame.draw.line(win, color, (self.x, self.y), (self.target.x, self.target.y))

        if switch:
            self.dist = math.dist([self.x, self.y], [self.target.x, self.target.y])
            Xm = ((self.x + self.target.x) / 2) - 15
            Ym = ((self.y + self.target.y) / 2) - 15

            dist_text = DIST_FONT.render("d: " +  "{:.2f}".format(self.dist), 1, (0, 0, 0, 191))
            win.blit(dist_text, (Xm, Ym))

    def controlar(self):
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_w]:
            self.y -= self.xvel
        if tecla[pygame.K_a]:
            self.x -= self.xvel
        if tecla[pygame.K_s]:
            self.y += self.xvel
        if tecla[pygame.K_d]:
            self.x += self.xvel

# BOLA
class Bola:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        
        if self.tipo == 1 or self.tipo == 11:
            self.xvel = 0
            self.yvel = -3.5
        if self.tipo >= 2 and self.tipo <= 4:
            self.xvel = 3.5
            self.yvel = 0
        if self.tipo >= 5 and self.tipo <= 7:
            self.xvel = 0
            self.yvel = 3.5
        if self.tipo >= 8 and self.tipo <= 10:
            self.xvel = -3.5
            self.yvel = 0

        self.surface = pygame.image.load('img/bola.png').convert_alpha()
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def draw(self, win):
        self.rect = self.surface.get_rect(center = (self.x, self.y))
        win.blit(self.surface, self.rect)

    def move(self, mapa):
        self.x += self.xvel
        self.y += self.yvel

        for parede in mapa.invis:
            if self.rect.colliderect(parede.rect):

                if parede.index == 's':
                    self.yvel = 0
                    self.xvel = 3.5

                    self.y += 1

                if parede.index == 'i':
                    self.yvel = 0
                    self.xvel = -3.5

                    self.y -= 1

                if parede.index == 'e':
                    self.yvel = -3.5
                    self.xvel = 0

                    self.x += 1

                if parede.index == 'd':
                    self.yvel = 3.5
                    self.xvel = 0

                    self.x -= 1

    def getx(self):
        return self.x

    def gety(self):
        return self.y

# MOEDA
class Moeda:
    def __init__(self):
        self.x = 198
        self.y = 166

        self.surface = pygame.image.load('img/moeda.png').convert_alpha()
        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def draw(self, win):
        win.blit(self.surface, self.rect)