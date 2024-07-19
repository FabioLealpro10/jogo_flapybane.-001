import pygame as pg
from pygame.locals import *
from sys import exit
from random import randint

pg.init()


# configução do jogo
largura = 600
altura = 400
tela = pg.display.set_mode((largura,altura)) # janela
pg.display.set_caption('Flap')
velocidade = pg.time.Clock()
pontos = 0
font = pg.font.SysFont('arial',20,True,True)
rapides = 30
fundo = pg.image.load('fundo.jpg').convert_alpha()

fundo = pg.transform.scale(fundo,(largura,altura))
mover_fundo = largura

# configuração dos obstaculos
local_cano_x_1 = largura
local_cano_y_1 = 80
verde = (0,250,0)
branco = (250,250,250)
espaço = randint(1,200)

# configuração do personagem
personagem = [pg.transform.scale(pg.image.load('voando.png'),(471//8,371//8)),pg.transform.scale(pg.image.load('caindo.png'),(471//7,371//7))]
perso_x = 100
perso_Y = 200
figura = 0
voar = True

# texto recomeço
txt = 'PRECIONE " Z " PARA INICIAR'
txt_recoço = font.render(txt,True,(0,0,0))


def parado():
    # loop para recomeçar
    recomeçar = False
    fundo_parado = pg.image.load('jogo_parado.jpg').convert_alpha()
    fundo_jogo_parado = pg.transform.scale(fundo_parado, (largura, altura))
    while not(recomeçar):
        tela.blit(fundo_jogo_parado, (0, 0))
        for envento in pg.event.get():
            if envento.type == QUIT:
                pg.quit()
                exit()
            if envento.type == KEYDOWN:
                if pg.key.get_pressed()[K_z]:
                    recomeçar = True
        tela.blit(txt_recoço,(100,10))
        pg.display.update()

parado()


while True:
    mostra_pontos = font.render(f'PONTUAÇÃO: {int(pontos)}',True,(0,0,0))
    velocidade.tick(int(rapides))
    tela.fill(branco)
    for envento in pg.event.get():
        if envento.type==QUIT:
            pg.quit()
            exit()
        if envento.type== KEYDOWN:
            if pg.key.get_pressed()[K_SPACE]:
                voar = True
                figura = 0

    movimentar = mover_fundo % fundo.get_rect().width
    tela.blit(fundo, (movimentar - fundo.get_rect().width, 0))
    if movimentar < largura:
        tela.blit(fundo, (mover_fundo, 0))
        if mover_fundo==0:
            mover_fundo = largura
    mover_fundo -= 1

    # textos do jogo
    tela.blit(mostra_pontos,(5,5))


    #personagem do jogador
    perso = tela.blit(personagem[int(figura)],(perso_x,int(perso_Y)))

    # quando que vai ficar em cima
    parede_cano_2 = pg.draw.rect(tela, verde, (local_cano_x_1 + 20, 0, 20, espaço))
    cano_boca_2 = pg.draw.rect(tela, verde, (local_cano_x_1,espaço, 60, 10))


    # quando que vai ficar em baixo
    cano_boca_1 = pg.draw.rect(tela, verde, (local_cano_x_1, local_cano_y_1+espaço, 60, 10))
    parede_cano_1 = pg.draw.rect(tela, verde, (local_cano_x_1 + 20, local_cano_y_1+espaço+9, 20,300 ))
    local_cano_x_1-=3
    if local_cano_x_1 < -6:
        local_cano_x_1 = largura
        espaço = randint(1, 200)
        rapides += 1
    if local_cano_x_1==36:
        pontos += 1

    if voar:
        perso_Y -= 15
        voar = False


    else:
        perso_Y +=1
        figura +=0.2
        if figura>=1.9:
            figura = 1





    # textos do jogo
    tela.blit(mostra_pontos,(5,5))

    #condição de perda
    if perso.colliderect(parede_cano_2) or perso.colliderect(parede_cano_1):
        local_cano_x_1 = largura
        espaço = randint(1, 200)
        perso_x = 100
        perso_Y = 200
        figura = 0
        pontos = 0
        voar = True
        mover_fundo = largura
        txt = 'PRECIONE "Z" PARA RECOMEÇAR'
        txt_recoço = font.render(txt, True, (0, 0, 0))

        # loop para recomeçar
        parado()


    pg.display.update()
    # Em conjunto