import pygame
import sys
import neat
import os
import pickle
import math

# Classes
from constantes import *
from mapa import *
from bola import *
from player import *

''' Save Winner '''
def save_winner(winner, playerNet):
    with open("winner.pickle", 'wb') as f:
        pickle.dump(playerNet, f)
        f.close

# PYGAME
pygame.init()
pygame.display.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo mais Difícil do Mundo!")

mapa_surface = pygame.image.load('img/mapa.png').convert_alpha()
mapa_rect = mapa_surface.get_rect(center = (WIDTH//2, HEIGHT//2)) 

# DRAW WINDOW
def draw_window(win, mapa, lista_bolas, player_list):
    win.fill(FUNDO)
    win.blit(mapa_surface, mapa_rect)

    for player in player_list:
        player.draw(win)
    
    for bola in lista_bolas:
        bola.draw(win)
    
    mapa.paredes()
    for p in mapa.lista_paredes:
        p.draw(win)

    # Gerações
    score_label = STAT_FONT.render("Gen: " + str(GEN-1), 1, BLACK)
    win.blit(score_label, (30, 10))

    # Vivos
    vivos = VIVOS_FONT.render("Vivos: " + str(len(player_list)), 1, BLACK)
    win.blit(vivos, (30, 40))

    # Ganharam
    contador_ganharam = GANHARAM_FONT.render("W: " + str(ganharam), 1, BLACK)
    win.blit(contador_ganharam, (WIDTH-70, 40))

    # Tempo
    tempo_text = TEMPO_FONT.render("T: " + str(tempo), 1, BLACK)
    win.blit(tempo_text, (WIDTH-170, 40))

    pygame.display.flip()

def main(genomes, config):

    # NEAT
    global GEN
    global WIN_ON
    GEN += 1

    player_list = []
    nets = []
    ge = []

    global bestDist
    bestDist = 99999

    global ganharam
    ganharam = 0

    for genomes_id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)

        nets.append(net)
        player_list.append(Player())

        g.fitness = 0
        ge.append(g)

    # Objetos 
    mapa = Mapa()

    bola1 = Bola(235, 154, 1)
    bola2 = Bola(665, 202, 2)
    bola3 = Bola(235, 250, 3)
    bola4 = Bola(665, 298, 4)
    lista_bolas = (bola1, bola2, bola3, bola4)
    area = Win()

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    run = True

    # Main loop
    while run and len(player_list) > 0:
        if WIN_ON: clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
                break

        # Tempo
        global tempo
        tempo = (pygame.time.get_ticks()-start_time)/1000

        # NN
        for x_c, player in enumerate(player_list):
            player.colisao_paredes(mapa) # Colisão com as paredes

            # Inputs da NN: player(x, y), bolas[1-4](x, y)
            outputs = nets[player_list.index(player)].activate( 
                (player.getx(), player.gety(),
                bola1.getx(), bola1.gety(),
                bola2.getx(), bola2.gety(),
                bola3.getx(), bola3.gety(),
                bola4.getx(), bola4.gety(),)
            )

            # Movimentos baseado no output (up, down, right)
            if max(outputs[0], outputs[1], outputs[2]) == outputs[0]:
                if outputs[0] > 0.5:
                    player.move_up()
                else:
                    player.move_stop()

            if max(outputs[0], outputs[1], outputs[2]) == outputs[1]:
                if outputs[1] > 0.5:
                    player.move_down()
                else:
                    player.move_stop()

            if max(outputs[0], outputs[1], outputs[2]) == outputs[2]:
                if outputs[2] > 0.5:
                    player.move_right()
                else:
                    player.move_stop()

            ''' NOVA GERAÇÃO '''

            # Colisão com as bolas
            for bola in lista_bolas:
                if player.player_rect.colliderect(bola.bola_rect):
                    player.colidiu = True

            if player.colidiu:
                ge[x_c].fitness -= 2.75 # Perde fitness por encostar na bola

                new_gen(nets, ge, x_c, player_list, player, area)

            # A cada X gerações, aumenta o tempo de jogo em Y
            tempo_max = 8

            if GEN % 15 == 0:
                tempo_max += 4

            # Se exceder o tempo máximo, começa uma nova geração
            if tempo > tempo_max:

                new_gen(nets, ge, x_c, player_list, player, area)

            # Colisão com área que ganha
            if player.player_rect.colliderect(area.win_rect):
                ge[x_c].fitness += 9999 # Ganha fitness para acabar a evolução

                ganharam += 1

                # Salva o vencedor
                save_winner(player, nets[player_list.index(player)])

                new_gen(nets, ge, x_c, player_list, player, area)
                
        # Movimentação Bola
        for bola in lista_bolas:
            bola.move()  

        # Display
        if WIN_ON:
            draw_window(win, mapa, lista_bolas, player_list) # Desenha tudo

# NOVA GERAÇÃO
def new_gen(nets, ge, x_c, player_list, player, area):
    global bestDist

    # Calcula a distância da área de vitória e soma o inverso ao fitness
    player.dist = math.sqrt( (area.getx() - player.getx())**2 + (area.gety() - player.gety())**2 )

    # Se a distância do player for maior do que a bestDist, se torna a nova bestDist
    if player.dist < bestDist:
        bestDist = player.dist

    # Mostra a melhor distância
    print("bestDist: " + str(bestDist))

    # Remove o player da lista
    nets.pop(player_list.index(player))
    ge.pop(player_list.index(player))
    player_list.pop(player_list.index(player))

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