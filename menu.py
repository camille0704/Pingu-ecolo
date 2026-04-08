import pygame
slide_actuelle = 0
slides_regles = []

def afficher_menu_accueil(screen, logo, bouton_start, bouton_rect):
    overlay = pygame.Surface((1080, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    box = pygame.Surface((800, 500), pygame.SRCALPHA)
    pygame.draw.rect(box, (220, 240, 255), (0, 0, 800, 500), border_radius=25)
    pygame.draw.rect(box, (50, 120, 210), (0, 0, 800, 500), width=6, border_radius=25)

    box.blit(logo, (125, 20))

    screen.blit(overlay, (0, 0))
    screen.blit(box, (140, 100))
    screen.blit(bouton_start, bouton_rect)

    pygame.display.flip()


def afficher_regles(screen):
    global slide_actuelle, slides_regles

    overlay = pygame.Surface((1080, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    box = pygame.Surface((900, 550), pygame.SRCALPHA)
    pygame.draw.rect(box, (220, 240, 255), (0, 0, 900, 550), border_radius=25)
    pygame.draw.rect(box, (50, 120, 210), (0, 0, 900, 550), width=6, border_radius=25)

    font = pygame.font.SysFont("Comic Sans MS", 36, bold=True)
    lignes = slides_regles[slide_actuelle]

    # CENTRAGE VERTICAL
    total_height = len(lignes) * 60
    start_y = (550 - total_height) // 2

    y = start_y
    for ligne in lignes:
        txt = font.render(ligne, True, (20, 40, 80))
        box.blit(txt, (450 - txt.get_width() // 2, y))
        y += 60

    # BOUTONS
    font_btn = pygame.font.SysFont("Comic Sans MS", 28, bold=True)
    btn_suiv = font_btn.render("Suivant", True, (0, 0, 80))
    btn_prec = font_btn.render("Précédent", True, (0, 0, 80))

    if slide_actuelle > 0:
        box.blit(btn_prec, (50, 500))

    if slide_actuelle < len(slides_regles) - 1:
        box.blit(btn_suiv, (700, 500))

    # CROIX
    font_close = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
    btn_close = font_close.render("X", True, (200, 0, 0))
    box.blit(btn_close, (850, 10))

    screen.blit(overlay, (0, 0))
    screen.blit(box, (90, 80))
    pygame.display.flip()


def clic_regles(x, y):
    global slide_actuelle, slides_regles

    # Décalage de la boîte
    dx = 90
    dy = 80

    # CROIX
    if 850 + dx <= x <= 880 + dx and 10 + dy <= y <= 50 + dy:
        return "fermer"

    # SUIVANT
    if slide_actuelle < len(slides_regles) - 1:
        if 700 + dx <= x <= 850 + dx and 500 + dy <= y <= 540 + dy:
            slide_actuelle += 1

    # PRECEDENT
    if slide_actuelle > 0:
        if 50 + dx <= x <= 200 + dx and 500 + dy <= y <= 540 + dy:
            slide_actuelle -= 1

    return None


def afficher_menu_options(screen):
    overlay = pygame.Surface((1080, 720), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    box = pygame.Surface((700, 550), pygame.SRCALPHA)
    pygame.draw.rect(box, (240, 240, 255), (0, 0, 700, 550), border_radius=25)
    pygame.draw.rect(box, (80, 120, 200), (0, 0, 700, 550), width=6, border_radius=25)

    font = pygame.font.SysFont("Comic Sans MS", 40, bold=True)
    titre = font.render("Menu Options", True, (20, 40, 80))
    box.blit(titre, (350 - titre.get_width()//2, 20))

    screen.blit(overlay, (0, 0))
    screen.blit(box, (190, 80))
    pygame.display.flip()