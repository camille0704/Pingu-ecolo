import pygame
pygame.init()
from game import Game

# fenêtre du jeu
pygame.display.set_caption("Pingu écolo !")
screen = pygame.display.set_mode((1080, 720))

background = pygame.image.load('Pingu écolo! - assets/fond.png').convert()
banquise = pygame.image.load('Pingu écolo! - assets/banquise.png').convert_alpha()

game = Game('Pingu écolo! - assets/Pingu simple .png')

SPAWN_EVENT = pygame.USEREVENT + 1

# fréquence selon le niveau
if game.niveau == 1:
    pygame.time.set_timer(SPAWN_EVENT, 1000)
else:
    pygame.time.set_timer(SPAWN_EVENT, 750)

clock = pygame.time.Clock()
running = True

# boucle du jeu
while running:

    # --- DESSIN ---
    screen.blit(background, (0, 0))  # 1. FOND
    screen.blit(game.calamar, (game.calamar_x, game.calamar_y)) # 2. CALAMAR
    screen.blit(banquise, (0, game.banquise_y))  # 3. BANQUISE
    game.all_dechet.draw(screen)  # 4. DÉCHETS
    screen.blit(game.player.image, game.player.rect)  # 5. JOUEUR

    # --- LOGIQUE ---
    game.all_dechet.update()
    game.update_timer()
    game.descendre_banquise()
    game.faire_monter_calamar()

    # déplacement joueur
    if game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
        game.player.move_left()
    elif game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < screen.get_width():
        game.player.move_right()

    pygame.display.flip()
    clock.tick(60)

    # --- ÉVÉNEMENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == SPAWN_EVENT:
            game.spawn_dechets()