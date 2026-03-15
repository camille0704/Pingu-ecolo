import pygame
pygame.init()

#fenetre du jeu
pygame.display.set_caption("Pingu écolo !")
pygame.display.set_mode((1080,720))

running = True
#tant que le jeu est actif
while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")