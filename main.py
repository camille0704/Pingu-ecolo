import pygame
pygame.init()

#fenetre du jeu
pygame.display.set_caption("Pingu écolo !")
screen = pygame.display.set_mode((1080,720))

background =pygame.image.load('Pingu écolo! - assets/fond.jpg')
running = True
#tant que le jeu est actif
while running:
    #mettre arriere plan
    screen.blit(background, (0,0))
    #mettre a jour l'ecran
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")