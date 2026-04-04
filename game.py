import pygame
import random
from player import Player
from dechet_trou import Dechet

class Game:
    def __init__(self,skin_path):
        self.player=Player(skin_path)
        self.all_dechet=pygame.sprite.Group()
        self.pressed={}
        self.niveau = 1  # niveau actuel
        self.temps_depart = pygame.time.get_ticks()
        self.partie_terminee = False

        # position initiale de la banquise
        self.banquise_y = 0

        # position finale (où elle doit s’arrêter)
        self.banquise_y_finale = 220  # tu peux ajuster
        # colonnes (écran 1080px)
        self.positions_x = [180, 540, 900]

        # déchets par niveau
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
        self.calamar = pygame.image.load("Pingu écolo! - assets/calamar.png")
        self.calamar_y = 900  # il commence caché sous l’eau
        self.calamar_x = 400  # position horizontale (à ajuster selon ton image)

    def spawn_dechets(self):
        if self.partie_terminee:
            return
        # choisir les déchets selon le niveau
        if self.niveau == 1:
            type_path = random.choice(self.dechets_niveau_1)
        else:
            type_path = random.choice(self.dechets_niveau_2)

        x = random.choice(self.positions_x)

        dechet = Dechet(type_path)

        # CENTRAGE CORRECT
        dechet.rect.centerx = x

        # position verticale
        dechet.rect.y = 300
        # vitesse selon le niveau
        if self.niveau == 1:
            dechet.velocity = 2
        else:
            dechet.velocity = 3

        self.all_dechet.add(dechet)

    def update_timer(self):
        if not self.partie_terminee:
            temps_ecoule = (pygame.time.get_ticks() - self.temps_depart) / 1000  # en secondes

            if temps_ecoule >= 90:  # 1 min 30
                self.partie_terminee = True

    def descendre_banquise(self):
        if self.partie_terminee and self.banquise_y < self.banquise_y_finale:
            self.banquise_y += 1.5  # vitesse douce

    def faire_monter_calamar(self):
        if self.partie_terminee and self.calamar_y > 500:  # hauteur finale
            self.calamar_y -= 2  # vitesse de montée