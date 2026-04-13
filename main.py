import pygame
import sys
import menu
from game import Game

pygame.init()

screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Pingu écolo !")
clock = pygame.time.Clock()

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

icon_calamar = pygame.image.load("Pingu écolo! - assets/calamar.png").convert_alpha()
icon_calamar = pygame.transform.smoothscale(icon_calamar, (40, 40))

cible_img = pygame.image.load("Pingu écolo! - assets/cible.png").convert_alpha()
cible_img = pygame.transform.smoothscale(cible_img, (100, 100))

skin_normal_img = pygame.image.load("Pingu écolo! - assets/Pingu simple .png").convert_alpha()
skin_rose_img = pygame.image.load("Pingu écolo! - assets/Pingu rose.png").convert_alpha()
skin_dore_img = pygame.image.load("Pingu écolo! - assets/Pingu dore.png").convert_alpha()

game = Game('Pingu écolo! - assets/Pingu simple .png')

menu.slides_regles[:] = [
    ["RÈGLES DU JEU"],
    ["BUT : évite les obstacles et va jusqu'à la fin !", "Attrape le calamar en sautant."],
    ["POINTS :", "+50 si tu attrapes le calamar", "+100 si tu finis le parcours"],
    ["VIES :", "Tu as 3 vies", "-1 si tu touches un obstacle"],
    ["CONTROLES :", "Flèches = bouger / cible", "SPACE = sauter"]
]

def afficher_message_centre(screen, texte, sous_texte=""):
    overlay = pygame.Surface((1080, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    box_rect = pygame.Rect(165, 230, 750, 260)
    pygame.draw.rect(screen, (255, 240, 200), box_rect, border_radius=25)
    font_main = pygame.font.SysFont("Comic Sans MS", 35, bold=True)
    txt_surf = font_main.render(texte, True, (60, 40, 20))
    screen.blit(txt_surf, (540 - txt_surf.get_width() // 2, 300))
    if sous_texte:
        font_sub = pygame.font.SysFont("Comic Sans MS", 25)
        sub_surf = font_sub.render(sous_texte, True, (100, 80, 60))
        screen.blit(sub_surf, (540 - sub_surf.get_width() // 2, 400))

SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1200)

running = True
menu_accueil = True
affiche_regles = False
affiche_boutique = False
boutons_boutique = {}
bouton_close_boutique = None

while running:

    m_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---------------------------
        # MENU ACCUEIL
        # ---------------------------
        if menu_accueil:
            if event.type == pygame.MOUSEBUTTONDOWN and bouton_rect.collidepoint(event.pos):
                menu_accueil = False
            continue

        # ---------------------------
        # SPAWN OBSTACLES
        # ---------------------------
        if event.type == SPAWN_EVENT and not (game.en_pause or game.game_over or game.parcours_termine or affiche_regles or affiche_boutique):
            game.spawn_dechets()

        # ---------------------------
        # TOUCHES
        # ---------------------------
        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if not game.en_pause and not game.game_over and not game.parcours_termine and not game.saut_possible:
                if event.key == pygame.K_LEFT: game.player.move_left()
                if event.key == pygame.K_RIGHT: game.player.move_right()

            if event.key == pygame.K_RETURN:

                # Sauvegarde des données persistantes
                ancien_calamars = game.calamars
                ancien_points = game.points
                ancien_niveau2 = game.niveau2_debloque
                ancien_niveau = game.niveau
                ancien_rose = game.pingu_rose_debloque
                ancien_dore = game.pingu_dore_debloque
                ancien_skin = game.skin_actuel

                # Fin de parcours ou game over → nouvelle partie
                if game.game_over or game.parcours_termine:
                    game = Game('Pingu écolo! - assets/Pingu simple .png')

                    # Restauration
                    game.calamars = ancien_calamars
                    game.points = ancien_points
                    game.niveau2_debloque = ancien_niveau2
                    game.niveau = ancien_niveau
                    game.pingu_rose_debloque = ancien_rose
                    game.pingu_dore_debloque = ancien_dore
                    game.skin_actuel = ancien_skin
                    game.changer_skin(ancien_skin)

                # Sortie de pause collision
                elif game.en_pause:
                    game.en_pause = False
                    game.all_dechet.empty()

            if event.key == pygame.K_SPACE and game.saut_possible:
                game.saut_effectue = True
                game.player.jump(game.cible_x, game.cible_y)

        if event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        # ---------------------------
        # CLICS SOURIS
        # ---------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Ouvrir règles
            if info_rect.collidepoint(m_pos):
                affiche_regles, game.en_pause, menu.slide_actuelle = True, True, 0

            # Ouvrir boutique
            elif menu_rect.collidepoint(m_pos):
                affiche_boutique, game.en_pause = True, True

            # Navigation règles
            elif affiche_regles:
                if menu.clic_regles(m_pos[0], m_pos[1]) == "fermer":
                    affiche_regles, game.en_pause = False, False

            # Clics boutique
            elif affiche_boutique:

                menu.slide_boutique_logic(m_pos[0], m_pos[1], game)

                if bouton_close_boutique and bouton_close_boutique.collidepoint(m_pos):
                    affiche_boutique, game.en_pause = False, False

                local_m = (m_pos[0] - 90, m_pos[1] - 60)

                # SKINS
                if boutons_boutique.get("normal") and boutons_boutique["normal"].collidepoint(local_m):
                    game.changer_skin("normal")

                elif boutons_boutique.get("rose") and boutons_boutique["rose"].collidepoint(local_m):
                    if game.pingu_rose_debloque:
                        game.changer_skin("rose")
                    elif game.calamars >= 3:
                        game.calamars -= 3
                        game.pingu_rose_debloque = True

                elif boutons_boutique.get("dore") and boutons_boutique["dore"].collidepoint(local_m):
                    if game.pingu_dore_debloque:
                        game.changer_skin("dore")
                    elif game.niveau2_debloque and game.calamars >= 5:
                        game.calamars -= 5
                        game.pingu_dore_debloque = True

                # NIVEAU 2
                elif boutons_boutique.get("niveau2") and boutons_boutique["niveau2"].collidepoint(local_m):
                    print(game.acheter("niveau2"))

    # ---------------------------
    # AFFICHAGE
    # ---------------------------
    if menu_accueil:
        menu.afficher_menu_accueil(screen, logo, bouton_start, bouton_rect)

    else:

        if not game.en_pause and not game.game_over and not game.parcours_termine:

            if game.saut_possible:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:  game.cible_x -= 8
                if keys[pygame.K_RIGHT]: game.cible_x += 8
                if keys[pygame.K_UP]:    game.cible_y -= 8
                if keys[pygame.K_DOWN]:  game.cible_y += 8

                game.cible_x = max(50, min(1030, game.cible_x))
                game.cible_y = max(50, min(670, game.cible_y))

            game.update_timer()
            game.player.update()
            game.all_dechet.update()
            game.descendre_banquise()
            game.faire_monter_calamar()
            game.player.update_jump()
            game.gerer_collisions()
            game.update_animations()

        screen.blit(background, (0, 0))
        screen.blit(banquise, (0, game.banquise_y))
        game.all_dechet.draw(screen)
        screen.blit(game.player.image, game.player.rect)

        if game.saut_possible:
            screen.blit(game.calamar, game.calamar_rect)
            screen.blit(cible_img, (game.cible_x - 50, game.cible_y - 50))

        font_ui = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
        for i in range(game.vies):
            screen.blit(game.coeur, (1000 - i * 50, 20))

        screen.blit(font_ui.render(f"Points: {game.points}", True, (20, 40, 80)), (650, 70))
        screen.blit(icon_calamar, (920, 115))
        screen.blit(font_ui.render(str(game.calamars), True, (20, 40, 80)), (970, 115))
        screen.blit(icon_info, info_rect)
        screen.blit(icon_menu, menu_rect)

        if affiche_boutique:
            boutons_boutique, bouton_close_boutique = menu.afficher_boutique(
                screen, game, skin_normal_img, skin_rose_img, skin_dore_img
            )

        if affiche_regles:
            menu.afficher_regles(screen)

        if game.game_over:
            afficher_message_centre(screen, "GAME OVER !", "ENTER pour recommencer")

        elif game.parcours_termine:
            afficher_message_centre(screen, game.message_collision, "ENTER pour rejouer")

        elif game.en_pause and not affiche_regles and not affiche_boutique:
            afficher_message_centre(screen, game.message_collision, "ENTER pour continuer")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()