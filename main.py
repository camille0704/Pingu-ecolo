import pygame
pygame.init()

import menu
from game import Game

pygame.display.set_caption("Pingu écolo !")
screen = pygame.display.set_mode((1080, 720))

# --- ASSETS ---
background = pygame.image.load('Pingu écolo! - assets/fond.png').convert()
banquise = pygame.image.load('Pingu écolo! - assets/banquise.png').convert_alpha()

logo = pygame.image.load("Pingu écolo! - assets/pingu ecolo logo.png").convert_alpha()
logo = pygame.transform.smoothscale(logo, (550, 330))

bouton_start = pygame.image.load("Pingu écolo! - assets/bouton start.png").convert_alpha()
bouton_start = pygame.transform.smoothscale(bouton_start, (260, 180))
bouton_rect = bouton_start.get_rect(center=(540, 500))

icon_info = pygame.image.load("Pingu écolo! - assets/i.png").convert_alpha()
icon_info = pygame.transform.smoothscale(icon_info, (64, 64))
info_rect = icon_info.get_rect(topleft=(20, 20))

icon_menu = pygame.image.load("Pingu écolo! - assets/menu.png").convert_alpha()
icon_menu = pygame.transform.smoothscale(icon_menu, (64, 64))
menu_rect = icon_menu.get_rect(topleft=(20, 100))

# --- ICÔNE CALAMAR ---
icon_calamar = pygame.image.load("Pingu écolo! - assets/calamar.png").convert_alpha()
icon_calamar = pygame.transform.smoothscale(icon_calamar, (32, 32))

# --- SLIDES DES REGLES ---
menu.slides_regles[:] = [
    ["RÈGLES DU JEU"],
    ["BUT : évite les obstacles et va jusqu'à la fin !", "Attrape le calamar en sautant."],
    ["POINTS :", "+25 si tu évites un obstacle", "+50 si tu attrapes le calamar", "+100 si tu finis le parcours"],
    ["VIES :", "Tu as 3 vies", "-1 si tu touches un obstacle", "0 vie = tu recommences"],
    ["NIVEAU 2 :", "Débloqué quand tu as 500 points"],
    ["CONTROLES :", "Flèche gauche = aller à gauche", "Flèche droite = aller à droite"],
    ["SKINS :", "Pingu simple : gratuit", "Pingu rose : 3 calamars", "Pingu doré : 5 calamars + niveau 2"]
]

affiche_regles_ecran = False
affiche_menu_options_ecran = False

# --- GAME ---
game = Game('Pingu écolo! - assets/Pingu simple .png')

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1000 if game.niveau == 1 else 750)

clock = pygame.time.Clock()
running = True

# --- BOITE COLLISION ---
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

# --- MENU D'ACCUEIL ---
menu_actif = True
while menu_actif:
    menu.afficher_menu_accueil(screen, logo, bouton_start, bouton_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_rect.collidepoint(event.pos):
                menu_actif = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                menu_actif = False

# --- BOUCLE DE JEU ---
while running:

    # --- SI LES RÈGLES SONT OUVERTES ---
    if affiche_regles_ecran:
        menu.afficher_regles(screen)
        # On ne dessine QUE les règles ici pour éviter le clignotement

    # --- SINON, SI LE MENU OPTION EST OUVERT ---
    elif affiche_menu_options_ecran:
        menu.afficher_menu_options(screen)

    # --- SINON, ON DESSINE LE JEU NORMALEMENT ---
    else:
        screen.blit(background, (0, 0))
        screen.blit(game.calamar, (game.calamar_x, game.calamar_y))
        screen.blit(banquise, (0, game.banquise_y))
        game.all_dechet.draw(screen)
        screen.blit(game.player.image, game.player.rect)

        # COEURS
        for i in range(game.vies):
            screen.blit(game.coeur, (1000 - i*50, 20))

        # POINTS & CALAMARS
        font_stats = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
        txt_points = font_stats.render(f"Points : {game.points}", True, (0, 0, 0))
        screen.blit(txt_points, (850, 70))
        screen.blit(icon_calamar, (850, 110))
        txt_calamars = font_stats.render(f"{game.calamars}", True, (0, 0, 0))
        screen.blit(txt_calamars, (890, 115))

        # ICONES (i et menu)
        screen.blit(icon_info, info_rect)
        screen.blit(icon_menu, menu_rect)

        # MESSAGES DE PAUSE / GAME OVER
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

            if game.en_pause and not game.game_over and event.key == pygame.K_RETURN:
                game.en_pause = False
                game.message_collision = ""
                game.all_dechet.empty()

            if game.game_over and event.key == pygame.K_RETURN:
                game.__init__('Pingu écolo! - assets/Pingu simple .png')

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # --- OUVRIR REGLES ---
            if info_rect.collidepoint(event.pos):
                affiche_regles_ecran = True
                menu.slide_actuelle = 0

            # --- OUVRIR MENU OPTIONS ---
            if menu_rect.collidepoint(event.pos):
                affiche_menu_options_ecran = True

            # --- CLIC DANS REGLES ---
            if affiche_regles_ecran:
                x, y = event.pos
                action = menu.clic_regles(x, y)
                if action == "fermer":
                    affiche_regles_ecran = False

            # --- CLIC DANS MENU OPTIONS ---
            if affiche_menu_options_ecran:
                x, y = event.pos

                if not (190 <= x <= 890 and 80 <= y <= 630):
                    affiche_menu_options_ecran = False

        elif event.type == SPAWN_EVENT:
            game.spawn_dechets()