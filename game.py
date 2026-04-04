import pygame
import random
import math
from player import Player
from dechet_trou import Dechet

class Game:
    def __init__(self, skin_path):
        self.player = Player(skin_path)
        self.all_dechet = pygame.sprite.Group()
        self.pressed = {}
        self.niveau = 1
        self.temps_depart = pygame.time.get_ticks()
        self.partie_terminee = False

        # banquise
        self.banquise_y = 0
        self.banquise_y_finale = 220

        # colonnes
        self.positions_x = [180, 540, 900]
        self.last_spawn_x = None

        # déchets
        self.dechets_niveau_1 = [
            "Pingu écolo! - assets/gateau dechet.png",
            "Pingu écolo! - assets/trou banquise.png"
        ]

        self.dechets_niveau_2 = [
            "Pingu écolo! - assets/gateau dechet.png",
            "Pingu écolo! - assets/trou banquise.png",
            "Pingu écolo! - assets/bouteille dechet.png",
            "Pingu écolo! - assets/compote dechet.png"
        ]

        # --- CALAMAR ---
        self.calamar = pygame.image.load("Pingu écolo! - assets/calamar.png").convert_alpha()

        # redimensionner SANS déformer (on garde le ratio)
        original_w = self.calamar.get_width()  # 2112
        original_h = self.calamar.get_height()  # 1408

        # taille finale plus petite (ajuste ici)
        nouvelle_hauteur = 150  # ← tu peux mettre 130, 120, 100 selon ce que tu veux
        ratio = nouvelle_hauteur / original_h
        nouvelle_largeur = int(original_w * ratio)

        self.calamar = pygame.transform.smoothscale(self.calamar, (nouvelle_largeur, nouvelle_hauteur))

        # position visible
        self.calamar_x = 400
        self.calamar_y = 400
        self.calamar_direction = 1  # 1 = droite, -1 = gauche
        self.calamar_speed = 2  # vitesse horizontale
        self.calamar_min_x = 300  # limite gauche
        self.calamar_max_x = 600  # limite droite
    # --- DÉCHETS ---
    def spawn_dechets(self):
        if self.partie_terminee:
            return

        if self.niveau == 1:
            type_path = random.choice(self.dechets_niveau_1)
        else:
            type_path = random.choice(self.dechets_niveau_2)

        # choisir une colonne différente de la précédente
        possible_x = [pos for pos in self.positions_x if pos != self.last_spawn_x]
        x = random.choice(possible_x)
        self.last_spawn_x = x

        dechet = Dechet(type_path)
        dechet.rect.centerx = x
        dechet.rect.y = 300

        dechet.velocity = 2 if self.niveau == 1 else 3
        self.all_dechet.add(dechet)
    # --- TIMER ---
    def update_timer(self):
        if not self.partie_terminee:
            temps_ecoule = (pygame.time.get_ticks() - self.temps_depart) / 1000
            if temps_ecoule >= 10:
                self.partie_terminee = True

    # --- BANQUISE ---
    def descendre_banquise(self):
        if self.partie_terminee and self.banquise_y < self.banquise_y_finale:
            self.banquise_y += 1.5

    # --- CALAMAR ---
    def faire_monter_calamar(self):
        # mouvement ondulé horizontal
        temps = pygame.time.get_ticks() / 1000  # temps en secondes
        amplitude = 120  # largeur du mouvement
        vitesse = 2  # vitesse de l'ondulation

        # position horizontale ondulée
        self.calamar_x = 450 + math.sin(temps * vitesse) * amplitude