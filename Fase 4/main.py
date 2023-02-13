import pygame
import sys
import neat
import os
import pickle
import math
import numpy as np

from constantes import *
from entidades import *
from mapa import *

# PYGAME
pygame.init()
pygame.display.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo mais Difícil do Mundo! (Fase 4)")

mapa_surface = pygame.image.load('img/mapa.png').convert_alpha()
mapa_rect = mapa_surface.get_rect(center = (WIDTH//2, HEIGHT//2))

# NEAT
GEN = 0
atw = 0

def draw_window(win, bolas, moedas, players, area):
    # Janela
    win.fill(FUNDO)
    win.blit(mapa_surface, mapa_rect)

    for b in bolas:
        b.draw(win)

    for m in moedas:
        m.draw(win)

    for p in players:
        if p in players:
            p.targetInfo(win, area, moedas, True)
            p.draw(win)

    ''' Textos '''

    # ESQUERDA

	# GEN
    gen_text = GEN_FONT.render("Gen: " + str(GEN-1), 1, BLACK)
    win.blit(gen_text, (30, 30))

	# Vivos:
    vivos_text = VIVOS_FONT.render("Vivos: " + str(len(players)), 1, BLACK)
    win.blit(vivos_text, (30, 60))
    
	# DIREITA

	# T
    tempo_text = TEMPO_FONT.render("T: " + str(tempo), 1, BLACK)
    win.blit(tempo_text, (WIDTH-150, 30))

	# W
    ganharam_text = TEMPO_FONT.render("W: " + str(ganharam), 1, BLACK)
    win.blit(ganharam_text, (WIDTH-150, 75))

	# ATW
    atw_text = ATW_FONT.render("ATW: " + str(atw), 1, RED)
    win.blit(atw_text, ((WIDTH-150, 120)))

    pygame.display.flip()

# -------------------------------------------------------------------------------------------------------

def main(genomes, config):
    global WIN_ON
    global GEN
    global tempo
    global tempo_max
    global ganharam
    global atw

    GEN += 1
    WIN_ON = True
    tempo_max = 25
    ganharam = 0

    ''' Objetos '''

    # Mapa
    mapa = Mapa()
    area = Win(230, 437, 1, 127)
    #spawn = Win(438, 32, 126, 198)

    # Bolas

    # Central
    bola0 = Bola(0, 0)

    # Verticais[10] (ini = 0)
    bola1 = Bola(0,  -1)
    bola2 = Bola(0, -2)
    bola3 = Bola(0, -3)
    bola4 = Bola(0, -4)
    bola5 = Bola(0, -5)

    bola6 = Bola(0, 1)
    bola7 = Bola(0, 2)
    bola8 = Bola(0, 3)
    bola9 = Bola(0, 4)
    bola10 = Bola(0, 5)

    # Horizontais[10] (ini = 90)
    bola11 = Bola(90, -1)
    bola12 = Bola(90, -2)
    bola13 = Bola(90, -3)
    bola14 = Bola(90, -4)
    bola15 = Bola(90, -5)

    bola16 = Bola(90, 1)
    bola17 = Bola(90, 2)
    bola18 = Bola(90, 3)
    bola19 = Bola(90, 4)
    bola20 = Bola(90, 5)

    # Moedas
    moeda1 = Moeda(500, 298)
    moeda2 = Moeda(703, 500)
    moeda3 = Moeda(500, 703)

    ''' Listas '''
    players = []
    moedas = []
    nets = []
    ge = []

    moedas = [moeda1, moeda2, moeda3]
    bolas = [bola0, bola1, bola2, bola3, bola4, bola5, bola6, bola7,
            bola8, bola9, bola10, bola11, bola12, bola13, bola14,
            bola15, bola16, bola17, bola18, bola19, bola20]

    # NEAT
    for genomes_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        nets.append(net)
        players.append(Player())

        genome.fitness = 0
        ge.append(genome)

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

        '''  Funcionamento básico do jogo '''

        for b in bolas:
            b.move()
        
        for x, player in enumerate(players):  

            # Verificadores de colisão

            player.colisaoBolas(bolas)
            player.colisaoMoedas(moedas)
            player.colisaoParedes(mapa)
            player.colisaoWin(area)

            ''' Neural Network '''

            # Define a bola mais próxima
            dist = []
            for b in bolas:
                dist.append(math.dist([b.x, b.y], [player.x, player.y]))
            bolaperto = bolas[dist.index(min(dist))]

            # Define a parede mais próxima
            dist2 = []
            for pr in mapa.paredes:
                dist2.append(math.dist([pr.x, pr.y], [player.x, player.y]))
            paredeperto = mapa.paredes[dist2.index(min(dist2))]

            # Inputs da NN
            outputs = nets[players.index(player)].activate(
                (

				player.x, player.y, # Posição do player

                bolaperto.x, bolaperto.y, # Bola mais próxima
                paredeperto.x, paredeperto.y, # Parede mais próxima

                player.target.x, player.target.y, # Target
                )
			)

            # Movimentos baseado no output (up, down, right, left)
            if max(outputs) == outputs[0]:
                if outputs[0] > 0.5:
                    player.move_up()

            if max(outputs) == outputs[1]:
                if outputs[1] > 0.5:
                    player.move_down()
            
            if max(outputs) == outputs[2]:
                if outputs[2] > 0.5:
                    player.move_right()
            
            if max(outputs) == outputs[3]:
                if outputs[3] > 0.5:
                    player.move_left()

            ''' Fitness '''

            # Começa geração nova quando o tempo acaba
            if tempo >= tempo_max:
                removeplayer(nets, ge, x, players, player, 0) 
            
            # Penaliza player que colidiu com alguma bola
            if player.colidiu:
                removeplayer(nets, ge, x, players, player, -2.5) # -2.5
            
            # Penaliza player que colidiu com a parede
            if player.colidiuP:
                removeplayer(nets, ge, x, players, player, -7.5) # Condicionamento: não bater na parede

            # Player vence
            if player.win:
                if atw >= 5:
                    removeplayer(nets, ge, x, players, player, 99999999)
                else:
                    removeplayer(nets, ge, x, players, player, 5000)
                    ganharam += 1
                    atw += 1

            # Remover players que após 3 segundos estejam dentro do spawn
            if tempo >= 3:
                if player.y <= 229:
                    removeplayer(nets, ge, x, players, player, -10)	
        
        if WIN_ON:
            draw_window(win, bolas, moedas, players, area)

# -------------------------------------------------------------------------------------------------------

# NOVA GERAÇÃO
def removeplayer(nets, ge, x, players, player, valor):

    if player in players:
        
        # Define o fitness
        ge[x].fitness += player.fitness + (1000 / player.dist) + valor
        
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

    winner = p.run(main, 9999999)

    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

    print('\nBest genome:\n{!s}'.format(winner))

# Config file path
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
