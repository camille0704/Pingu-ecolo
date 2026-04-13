import pygame

slide_actuelle = 0
slide_boutique = 0
slides_regles = []


def afficher_skin_ligne(box, image, nom, etat, prix, y, font):
    # Forcer la taille pour la boutique (80x80)
    image_mini = pygame.transform.smoothscale(image, (80, 80))

    # Rectangle de la ligne
    rect_v = pygame.Rect(40, y, 450, 100)
    # Fond de la ligne arrondi
    pygame.draw.rect(box, (210, 230, 255), rect_v, border_radius=15)

    box.blit(image_mini, (55, y + 10))
    box.blit(font.render(nom, True, (20, 40, 80)), (160, y + 30))

    btn_r = pygame.Rect(550, y + 20, 300, 60)
    if etat == "actuel":
        col, txt = (100, 200, 100), "EQUIPE"
    elif etat == "debloque":
        col, txt = (100, 150, 255), "CHOISIR"
    else:
        col, txt = (180, 180, 180), str(prix)

    pygame.draw.rect(box, col, btn_r, border_radius=12)
    s_txt = font.render(txt, True, (0, 0, 0))
    box.blit(s_txt, (btn_r.centerx - s_txt.get_width() // 2, btn_r.centery - s_txt.get_height() // 2))
    return btn_r


def afficher_boutique(screen, game, skin_normal_img, skin_rose_img, skin_dore_img):
    global slide_boutique
    overlay = pygame.Surface((1080, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    # On crée une surface transparente pour la box
    box = pygame.Surface((900, 600), pygame.SRCALPHA)

    # DESSIN DU FOND ARRONDIS (Remplissage)
    pygame.draw.rect(box, (240, 240, 255), (0, 0, 900, 600), border_radius=25)
    # DESSIN DU CONTOUR ARRONDIS (Bordure)
    pygame.draw.rect(box, (80, 120, 200), (0, 0, 900, 600), 6, border_radius=25)

    font = pygame.font.SysFont("Comic Sans MS", 30, bold=True)
    boutons = {}

    if slide_boutique == 0:  # PAGE SKINS
        titre = font.render("Boutique de Skins", True, (20, 40, 80))
        box.blit(titre, (450 - titre.get_width() // 2, 20))

        boutons["normal"] = afficher_skin_ligne(box, skin_normal_img, "Pingu simple",
                                                "actuel" if game.skin_actuel == "normal" else "debloque", "Gratuit",
                                                100, font)
        boutons["rose"] = afficher_skin_ligne(box, skin_rose_img, "Pingu rose",
                                              "actuel" if game.skin_actuel == "rose" else (
                                                  "debloque" if game.pingu_rose_debloque else "bloque"), "3 Calamars",
                                              230, font)
        boutons["dore"] = afficher_skin_ligne(box, skin_dore_img, "Pingu dore",
                                              "actuel" if game.skin_actuel == "dore" else (
                                                  "debloque" if game.pingu_dore_debloque else "bloque"), "5 Calamars",
                                              360, font)

        pygame.draw.rect(box, (80, 100, 180), (600, 520, 250, 60), border_radius=15)
        box.blit(font.render("NIVEAUX ->", True, (255, 255, 255)), (630, 530))
    else:  # PAGE NIVEAUX
        titre = font.render("Choix du Niveau", True, (20, 40, 80))
        box.blit(titre, (450 - titre.get_width() // 2, 20))

        # Niveau 1
        pygame.draw.rect(box, (210, 230, 255), (100, 150, 700, 100), border_radius=15)
        box.blit(font.render("Niveau 1" + (" (ACTIF)" if game.niveau == 1 else ""), True, (20, 40, 80)), (130, 175))

        # Niveau 2
        rect_nv2 = pygame.Rect(100, 300, 700, 100)
        pygame.draw.rect(box, (200, 255, 200) if game.niveau2_debloque else (255, 200, 200), rect_nv2, border_radius=15)
        boutons["niveau2"] = rect_nv2  # ⭐ LE BOUTON QUI MANQUAIT ⭐

        txt_nv2 = "Niveau 2" + (
            " (ACTIF)" if game.niveau == 2 else "") if game.niveau2_debloque else "Niveau 2 (500 pts requis)"
        box.blit(font.render(txt_nv2, True, (20, 40, 80)), (130, 325))

        # Retour
        pygame.draw.rect(box, (80, 100, 180), (50, 520, 250, 60), border_radius=15)
        box.blit(font.render("<- SKINS", True, (255, 255, 255)), (80, 530))
    # Croix de fermeture
    pygame.draw.rect(box, (255, 50, 50), (840, 10, 50, 50), border_radius=10)
    box.blit(font.render("X", True, (255, 255, 255)), (852, 12))

    screen.blit(overlay, (0, 0))
    screen.blit(box, (90, 60))
    return boutons, pygame.Rect(90 + 840, 60 + 10, 50, 50)


def slide_boutique_logic(x, y, game):
    global slide_boutique
    dx, dy = 90, 60
    if slide_boutique == 0:
        if 600 + dx <= x <= 850 + dx and 520 + dy <= y <= 580 + dy: slide_boutique = 1
    else:
        if 50 + dx <= x <= 300 + dx and 520 + dy <= y <= 580 + dy: slide_boutique = 0
        if 100 + dx <= x <= 800 + dx and 150 + dy <= y <= 250 + dy: game.niveau = 1
        if 100 + dx <= x <= 800 + dx and 300 + dy <= y <= 400 + dy and game.niveau2_debloque: game.niveau = 2


def afficher_regles(screen):
    global slide_actuelle, slides_regles
    overlay = pygame.Surface((1080, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    # Surface transparente pour les règles
    box = pygame.Surface((900, 550), pygame.SRCALPHA)

    # Fond ARRONDI
    pygame.draw.rect(box, (220, 240, 255), (0, 0, 900, 550), border_radius=25)
    # Contour ARRONDI
    pygame.draw.rect(box, (80, 120, 200), (0, 0, 900, 550), 5, border_radius=25)

    font = pygame.font.SysFont("Comic Sans MS", 30, bold=True)
    if slide_actuelle < len(slides_regles):
        for i, ligne in enumerate(slides_regles[slide_actuelle]):
            txt = font.render(ligne, True, (20, 40, 80))
            box.blit(txt, (450 - txt.get_width() // 2, 100 + i * 50))

    if slide_actuelle > 0:
        pygame.draw.rect(box, (100, 150, 255), (50, 460, 180, 60), border_radius=12)
        box.blit(font.render("RETOUR", True, (255, 255, 255)), (70, 470))
    if slide_actuelle < len(slides_regles) - 1:
        pygame.draw.rect(box, (100, 150, 255), (670, 460, 180, 60), border_radius=12)
        box.blit(font.render("SUIVANT", True, (255, 255, 255)), (690, 470))

    pygame.draw.rect(box, (255, 50, 50), (840, 10, 50, 50), border_radius=10)
    box.blit(font.render("X", True, (255, 255, 255)), (852, 12))

    screen.blit(overlay, (0, 0))
    screen.blit(box, (90, 80))
    pygame.display.flip()


def clic_regles(x, y):
    global slide_actuelle
    dx, dy = 90, 80
    if 840 + dx <= x <= 890 + dx and 10 + dy <= y <= 60 + dy: return "fermer"
    if slide_actuelle < len(
        slides_regles) - 1 and 670 + dx <= x <= 850 + dx and 460 + dy <= y <= 520 + dy: slide_actuelle += 1
    if slide_actuelle > 0 and 50 + dx <= x <= 230 + dx and 460 + dy <= y <= 520 + dy: slide_actuelle -= 1
    return None


def afficher_menu_accueil(screen, logo, bouton_start, bouton_rect):
    screen.fill((200, 230, 255))
    screen.blit(logo, (540 - logo.get_width() // 2, 100))
    screen.blit(bouton_start, bouton_rect)