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
pygame.display.set_caption("Jogo mais Difícil do Mundo! (Fase 3)")

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
            p.targetInfo(win, area, moedas, False)
            p.draw(win)

    # Textos

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

	# M
    vivosmoeda1 = []
    vivosmoeda2 = []
    vivosmoeda3 = []
    for p in players:
        if p.moeda1:
            vivosmoeda1.append(p)
        if p.moeda2:
            vivosmoeda2.append(p)
        if p.moeda3:
            vivosmoeda3.append(p) 

    moeda1_text = MOEDASPEGAS_FONT.render("M1: " + str(len(vivosmoeda1)), 1, YELLOW)
    win.blit(moeda1_text, (30, 120))

    moeda2_text = MOEDASPEGAS_FONT.render("M2: " + str(len(vivosmoeda2)), 1, YELLOW)
    win.blit(moeda2_text, (30, 155))

    moeda3_text = MOEDASPEGAS_FONT.render("M3: " + str(len(vivosmoeda3)), 1, YELLOW)
    win.blit(moeda3_text, (30, 190))

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
    tempo_max = 10
    ganharam = 0

	# Tempo Max
    if GEN % 100 == 0 and GEN > 0:
        tempo_max += 2
    if GEN >= 500:
        tempo_max = 20

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

            for b in bolas:
                player.colisaoBola(b)

            player.colisaoMoedas(moedas)
            player.colisaoParedes(mapa)
            player.colisaoWin(area)

            if tempo >= tempo_max:
                player.timeout = True

            ''' Neural Network '''

            # Determina a distância do player à cada barra e escolhe a menor para fornecer para a NN
            b0 = np.array([bola0.getx(), bola0.gety()])

            b1 = np.array([bola5.getx(), bola5.gety()])
            b2 = np.array([bola10.getx(), bola10.gety()])
            b3 = np.array([bola15.getx(), bola15.gety()])
            b4 = np.array([bola20.getx(), bola20.gety()])
            p = np.array([player.getx(), player.gety()])

            #distb = np.cross(b0-b1, p-b1) / np.linalg.norm(b0-b1)
            distb1 = np.cross(b0-b1, p-b1) / np.linalg.norm(b0-b1) # d(Player | b0b1)
            distb2 = np.cross(b0-b2, p-b2) / np.linalg.norm(b0-b2) # d(Player | b0b2)
            distb3 = np.cross(b0-b3, p-b3) / np.linalg.norm(b0-b3) # d(Player | b0b3)
            distb4 = np.cross(b0-b4, p-b4) / np.linalg.norm(b0-b4) # d(Player | b0b4)

            dists = [distb1, distb2, distb3, distb4]
            
            barra = min(dists)

            # Inputs da NN
            outputs = nets[players.index(player)].activate(
                (

				player.getx(), player.gety(), # Posição do player

                barra, # Distância do player às barras

                abs(player.target.getx() - player.getx()), 
                abs(player.target.gety() - player.gety())
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

            if player in players:
                if player.timeout:
                    removeplayer(nets, ge, x, players, player, 0)

            if player in players:
                if player.colidiu:
                    removeplayer(nets, ge, x, players, player, -2.5) # -2.5
            
            if player in players:
                if player.win:
                    if atw >= 5:
                        removeplayer(nets, ge, x, players, player, 99999999)
                    else:
                        ganharam += 1
                        atw += 1

                        print("Ganhou!")

                        removeplayer(nets, ge, x, players, player, 5000)

            if player in players:
                if tempo >= 1.5:
                    if player.gety() <= 229:
                            removeplayer(nets, ge, x, players, player, -10)	
        if WIN_ON:
            draw_window(win, bolas, moedas, players, area)

# -------------------------------------------------------------------------------------------------------

# NOVA GERAÇÃO
def removeplayer(nets, ge, x, players, player, valor):

    if player in players:
        
        # Define o fitness
        ge[x].fitness += player.fitness + (3000 / player.dist) + valor
        
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