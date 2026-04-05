import pygame
pygame.init()
from game import Game

pygame.display.set_caption("Pingu écolo !")
screen = pygame.display.set_mode((1080, 720))

background = pygame.image.load('Pingu écolo! - assets/fond.png').convert()
banquise = pygame.image.load('Pingu écolo! - assets/banquise.png').convert_alpha()

game = Game('Pingu écolo! - assets/Pingu simple .png')

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1000 if game.niveau == 1 else 750)

clock = pygame.time.Clock()
running = True

# --- BOITE DE DIALOGUE COLLISION ---
def afficher_message(screen, texte):
    overlay = pygame.Surface((1080, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    box = pygame.Surface((750, 260), pygame.SRCALPHA)
    pygame.draw.rect(box, (255, 240, 200), (0, 0, 750, 260), border_radius=25)
    pygame.draw.rect(box, (255, 180, 80), (0, 0, 750, 260), width=6, border_radius=25)

    font = pygame.font.SysFont("Comic Sans MS", 38, bold=True)
    font_small = pygame.font.SysFont("Comic Sans MS", 28)

    txt = font.render(texte, True, (60, 40, 20))
    info = font_small.render("Appuie sur ENTER pour reprendre le jeu", True, (80, 60, 40))

    box.blit(txt, (375 - txt.get_width()//2, 70 - txt.get_height()//2))
    box.blit(info, (375 - info.get_width()//2, 160 - info.get_height()//2))

    screen.blit(overlay, (0, 0))
    screen.blit(box, (165, 230))

# --- BOITE GAME OVER ---
def afficher_game_over(screen):
    overlay = pygame.Surface((1080, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))

    box = pygame.Surface((700, 260), pygame.SRCALPHA)
    pygame.draw.rect(box, (255, 180, 180), (0, 0, 700, 260), border_radius=25)
    pygame.draw.rect(box, (200, 60, 60), (0, 0, 700, 260), width=6, border_radius=25)

    font = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
    font_small = pygame.font.SysFont("Comic Sans MS", 28)

    txt = font.render("Oh non... tu as perdu !", True, (120, 20, 20))
    info = font_small.render("Appuie sur ENTER pour recommencer", True, (80, 20, 20))

    box.blit(txt, (350 - txt.get_width()//2, 70 - txt.get_height()//2))
    box.blit(info, (350 - info.get_width()//2, 160 - info.get_height()//2))

    screen.blit(overlay, (0, 0))
    screen.blit(box, (190, 230))


# --- BOUCLE DE JEU ---
while running:

    screen.blit(background, (0, 0))
    screen.blit(game.calamar, (game.calamar_x, game.calamar_y))
    screen.blit(banquise, (0, game.banquise_y))
    game.all_dechet.draw(screen)
    screen.blit(game.player.image, game.player.rect)

    # --- COEURS ---
    for i in range(game.vies):
        screen.blit(game.coeur, (1000 - i*50, 20))

    # --- MESSAGES ---
    if game.en_pause and not game.game_over:
        afficher_message(screen, game.message_collision)

    if game.game_over:
        afficher_game_over(screen)

    pygame.display.flip()
    clock.tick(60)

    # --- LOGIQUE ---
    if not game.en_pause and not game.game_over:
        game.all_dechet.update()
        game.update_timer()
        game.descendre_banquise()
        game.faire_monter_calamar()
        game.gerer_collisions()

    # --- DEPLACEMENT ---
    if game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
        game.player.move_left()
    elif game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < screen.get_width():
        game.player.move_right()

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            # --- ENTER pour reprendre ---
            if game.en_pause and not game.game_over and event.key == pygame.K_RETURN:
                game.en_pause = False
                game.message_collision = ""
                game.all_dechet.empty()

            # --- ENTER pour recommencer ---
            if game.game_over and event.key == pygame.K_RETURN:
                game.__init__('Pingu écolo! - assets/Pingu simple .png')

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == SPAWN_EVENT:
            game.spawn_dechets()