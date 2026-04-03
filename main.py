import pygame
pygame.init()
from game import Game
from player import Player
#fenetre du jeu
pygame.display.set_caption("Pingu écolo !")
screen = pygame.display.set_mode((1080,720))

background = pygame.image.load('Pingu écolo! - assets/fond.png')
banquise = pygame.image.load('Pingu écolo! - assets/banquise.png').convert_alpha()
game=Game('Pingu écolo! - assets/Pingu simple .png')
running = True
#tant que le jeu est actif
while running:
    #mettre arriere plan
    screen.blit(background, (0,0))
    screen.blit(banquise, (0, 0))
    #affichage joueur
    screen.blit(game.player.image,game.player.rect)
    #si le joueur appui sur la f_gauche ou la f_droite
    if game.pressed.get(pygame.K_LEFT) and game.player.rect.x >0:
        game.player.move_left()
    elif game.pressed.get(pygame.K_RIGHT) and game.player.rect.x +game.player.rect.width< screen.get_width():
        game.player.move_right()
    #mettre a jour l'ecran
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key]=True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key]=False
