import pygame
import sys
import neat
import os
import pickle
import math

from constantes import *
from entidades import *
from mapa import *

# PYGAME
pygame.init()
pygame.display.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo mais Difícil do Mundo! (Fase 1)")

mapa_surface = pygame.image.load('img/mapa.png').convert_alpha()
mapa_rect = mapa_surface.get_rect(center = (WIDTH//2, HEIGHT//2))

# NEAT
GEN = 0
atw = 0

# DRAW WINDOW
def draw_window(win, bolas, players, area):
    win.fill(FUNDO)
    win.blit(mapa_surface, mapa_rect)

    for b in bolas:
        b.draw(win)

    for p in players:
        if p in players:
            p.draw(win)
            p.targetInfo(win, area, False)

    ''' Textos '''

    # ESQUERDA

    # GEN
    score_label = STAT_FONT.render("Gen: " + str(GEN-1), 1, BLACK)
    win.blit(score_label, (30, 10))

    # Vivos
    vivos = VIVOS_FONT.render("Vivos: " + str(len(players)), 1, BLACK)
    win.blit(vivos, (30, 40))

    # DIREITA

    # ATW
    atw_text = ATW_FONT.render("ATW: " + str(atw), 1, RED)
    win.blit(atw_text, ((WIDTH-260, 40)))

    # Ganharam
    contador_ganharam = GANHARAM_FONT.render("W: " + str(ganharam), 1, BLACK)
    win.blit(contador_ganharam, (WIDTH-170, 40))

    # Tempo
    tempo_text = TEMPO_FONT.render("T: " + str(tempo), 1, BLACK)
    win.blit(tempo_text, (WIDTH-110, 40))

    pygame.display.flip()

def main(genomes, config):

    # NEAT
    global GEN
    global WIN_ON
    global tempo
    global tempo_max
    global ganharam
    global atw

    GEN += 1
    WIN_ON = True
    tempo_max = 8
    ganharam = 0

    # Objetos 
    mapa = Mapa()

    area = Win(738, 84, 1, 42)

    bola1 = Bola(235, 154, 1)
    bola2 = Bola(665, 202, 2)
    bola3 = Bola(235, 250, 3)
    bola4 = Bola(665, 298, 4)

    # Listas
    bolas = [bola1, bola2, bola3, bola4]

    players = []
    nets = []
    ge = []

    for genomes_id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)

        nets.append(net)
        players.append(Player())

        g.fitness = 0
        ge.append(g)

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    run = True

    # Main loop
    while run and len(players) > 0:
        if WIN_ON: clock.tick(FPS)

        # Tempo
        tempo = (pygame.time.get_ticks()-start_time) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
                break

        for b in bolas:
            b.move()

        # NN
        for x, player in enumerate(players):

           # Colisões
            player.colisaoBolas(bolas)
            player.colisaoParedes(mapa)
            player.colisaoWin(area)

            ''' Neural Network '''

            # Inputs da NN
            outputs = nets[players.index(player)].activate( 
                (
                player.x, player.y,

                bola1.x, bola1.y,
                bola2.x, bola2.y,
                bola3.x, bola3.y,
                bola4.x, bola4.y,
                )
            )

            # Movimentos baseado no output (up, down, right)
            if max(outputs) == outputs[0]:
                if outputs[0] > 0.5:
                    player.move_up()

            if max(outputs) == outputs[1]:
                if outputs[1] > 0.5:
                    player.move_down()

            if max(outputs) == outputs[2]:
                if outputs[2] > 0.5:
                    player.move_right()

            ''' Fitness '''

            # Tempo máximo
            if tempo >= tempo_max:
                removeplayer(nets, ge, x, players, player, 0)

            # Colisão com as bolas
            if player.colidiu:
                removeplayer(nets, ge, x, players, player, -2.5)

            # Ganhou:
            if player.win:
                if atw >= 10:
                    removeplayer(nets, ge, x, players, player, 99999999)
                else:
                    removeplayer(nets, ge, x, players, player, 5000)
                    ganharam += 1
                    atw += 1

            # Elimina players que estiverem no spawn depois de 3.5 segundos
            if tempo >= 3.5:
                if player.x <= 162 and player.y <= 371:
                    removeplayer(nets, ge, x, players, player, -5) # -5 de fitness
                
        if WIN_ON:
            draw_window(win, bolas, players, area) # Desenha tudo

# NOVA GERAÇÃO
def removeplayer(nets, ge, x, players, player, valor):
    
    if player in players:

        ge[x].fitness += player.fitness +  (2500 / player.dist) + valor

        # Remove player do jogo
    
        nets.pop(players.index(player))
        ge.pop(players.index(player))
        players.pop(players.index(player))

# NEAT
def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 9999)
    
    print('\nBest genome:\n{!s}'.format(winner))

# Config file path
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)