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

        # --- VIES ---
        self.vies = 3
        self.en_pause = False
        self.message_collision = ""
        self.game_over = False

        # --- SON PERDU ---
        self.son_perdu = pygame.mixer.Sound("Pingu écolo! - assets/sounds/perdu.ogg")

        # --- COEUR PNG ---
        self.coeur = pygame.image.load("Pingu écolo! - assets/coeur.png").convert_alpha()
        self.coeur = pygame.transform.smoothscale(self.coeur, (40, 40))

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

        # --- TON DICTIONNAIRE ---
        self.dico_message = {
            "Pingu écolo! - assets/gateau dechet.png": "Oh non ! Pingu a glissé sur un gâteau !",
            "Pingu écolo! - assets/trou banquise.png": "Aïe ! Pingu est tombé dans un trou !",
            "Pingu écolo! - assets/bouteille dechet.png": "Pingu a trébuché sur une bouteille !",
            "Pingu écolo! - assets/compote dechet.png": "Pingu a glissé sur une compote !"
        }

        # --- CALAMAR ---
        self.calamar = pygame.image.load("Pingu écolo! - assets/calamar.png").convert_alpha()

        original_w = self.calamar.get_width()
        original_h = self.calamar.get_height()
        nouvelle_hauteur = 150
        ratio = nouvelle_hauteur / original_h
        nouvelle_largeur = int(original_w * ratio)

        self.calamar = pygame.transform.smoothscale(self.calamar, (nouvelle_largeur, nouvelle_hauteur))

        self.calamar_x = 400
        self.calamar_y = 400

    # --- DÉCHETS ---
    def spawn_dechets(self):
        if self.partie_terminee or self.en_pause:
            return

        if self.niveau == 1:
            type_path = random.choice(self.dechets_niveau_1)
        else:
            type_path = random.choice(self.dechets_niveau_2)

        possible_x = [pos for pos in self.positions_x if pos != self.last_spawn_x]
        x = random.choice(possible_x)
        self.last_spawn_x = x

        dechet = Dechet(type_path)
        dechet.image_path = type_path  # indispensable
        dechet.rect.centerx = x
        dechet.rect.y = 300

        dechet.velocity = 2 if self.niveau == 1 else 3
        self.all_dechet.add(dechet)

    # --- TIMER ---
    def update_timer(self):
        if not self.partie_terminee:
            temps_ecoule = (pygame.time.get_ticks() - self.temps_depart) / 1000
            if temps_ecoule >= 40:
                self.partie_terminee = True

    # --- BANQUISE ---
    def descendre_banquise(self):
        if self.partie_terminee and self.banquise_y < self.banquise_y_finale:
            self.banquise_y += 1.5

    # --- CALAMAR ---
    def faire_monter_calamar(self):
        temps = pygame.time.get_ticks() / 1000
        amplitude = 120
        vitesse = 2
        self.calamar_x = 450 + math.sin(temps * vitesse) * amplitude

    # --- COLLISIONS ---
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def gerer_collisions(self):
        if self.en_pause or self.partie_terminee:
            return

        collisions = self.check_collision(self.player, self.all_dechet)

        if collisions:
            dechet = collisions[0]
            chemin = dechet.image_path

            self.message_collision = self.dico_message.get(chemin, "Attention !")

            self.vies -= 1
            self.en_pause = True

            if self.vies <= 0:
                self.partie_terminee = True
                self.game_over = True
                self.son_perdu.play()