import pygame
import random
import math
from player import Player
from dechet_trou import Dechet

class Game:
    def __init__(self, skin_path):
        self.player = Player(skin_path)
        self.player.game = self
        self.all_dechet = pygame.sprite.Group()
        self.pressed = {}
        self.niveau = 1
        self.temps_depart = pygame.time.get_ticks()
        self.temps_depart = pygame.time.get_ticks()
        self.partie_terminee = False
        self.niveau2_debloque = False
        self.pingu_rose_debloque = False
        self.pingu_dore_debloque = False
        self.skin_actuel = "normal"
        self.vies = 3
        self.en_pause = False
        self.pause_type = False
        self.message_collision = ""
        self.game_over = False
        self.parcours_termine = False
        self.message_delay = 0
        self.points = 0
        self.calamars = 0
        self.last_spawn_time = 0
        self.son_perdu = pygame.mixer.Sound("Pingu écolo! - assets/sounds/perdu.ogg")
        self.son_calamar = pygame.mixer.Sound("Pingu écolo! - assets/sounds/calamar.ogg")
        self.son_achat = pygame.mixer.Sound("Pingu écolo! - assets/sounds/nouveau_personnage.ogg")
        self.son_passage_1_2 = pygame.mixer.Sound("Pingu écolo! - assets/sounds/passage_1_a_2.ogg")
        # COEUR : PAS TOUCHÉ
        self.coeur = pygame.image.load("Pingu écolo! - assets/coeur.png").convert_alpha()
        self.coeur = pygame.transform.smoothscale(self.coeur, (60, 60))
        # banquise
        self.banquise_y = 0
        self.banquise_y_finale = 220
        self.positions_x = [180, 540, 900]
        self.spawn_pattern_step = 0
        self.spawn_y = 300
        self.spawn_gap = 260
        self.safe_line_every = 1  # 1 ligne vide après chaque ligne de danger
        self.last_spawn_x = None
        self.dechets_niveau_1 = [ "Pingu écolo! - assets/gateau dechet.png", "Pingu écolo! - assets/trou banquise.png" ]
        self.dechets_niveau_2 = [ "Pingu écolo! - assets/gateau dechet.png", "Pingu écolo! - assets/trou banquise.png", "Pingu écolo! - assets/bouteille dechet.png", "Pingu écolo! - assets/compote dechet.png" ]
        self.dico_message = { "Pingu écolo! - assets/gateau dechet.png": "Oh non ! Pingu a glissé sur un gâteau ! Cela est dû a la pollution. Si à l'école tu tombes sur un dechet de gateau pense à le ramasser et le mettre dans la poubelle. ", "Pingu écolo! - assets/trou banquise.png": "Aïe ! Pingu est tombé dans un trou ! Cela est dû au réchauffement climatique. Pour éviter cela si tu habites proche de l'école pense a y aller a pied ou a velo plutôt que d'y aller en voiture.", "Pingu écolo! - assets/bouteille dechet.png": "Pingu a trébuché sur une bouteille !Cela est dû a la pollution. Si tu trouves une bouteille dans la rue,pense à la  jeter dans la poubelle jaune ", "Pingu écolo! - assets/compote dechet.png": "Pingu a glissé sur une compote !Cela est dû a la pollution. Si tu vois une compote vide par terre dans la cour de récréation ramasse-la et jette la dans la poubelle." }
        # CALAMAR = 200×200
        self.calamar = pygame.image.load("Pingu écolo! - assets/calamar.png").convert_alpha()
        self.calamar = pygame.transform.scale(self.calamar, (200, 200))
        self.calamar_x = 400
        self.calamar_y = 350
        self.calamar_rect = self.calamar.get_rect()
        self.calamar_rect.x = self.calamar_x
        self.calamar_rect.y = self.calamar_y
        # CIBLE : PAS TOUCHÉE
        self.cible_x = 500
        self.cible_y = 400
        self.saut_possible = False
        self.saut_effectue = False
        self.animations_points = []
        self.banquise_bonus_donne = False
        self.target_cible_x = self.cible_x
        self.target_cible_y = self.cible_y
        self.cible_vitesse = 0.2

    def spawn_dechets(self):

        if self.partie_terminee or self.en_pause:
            return

        now = pygame.time.get_ticks()

        cooldown = 1100 if self.niveau == 1 else 900
        if now - self.last_spawn_time < cooldown:
            return

        self.last_spawn_time = now

        # -------------------------------------------------
        # 1 LIGNE SAFE GARANTIE (TOUJOURS UNE LANE LIBRE)
        # -------------------------------------------------
        if self.spawn_pattern_step % 2 == 1:
            self.spawn_pattern_step += 1
            return

        # -------------------------------------------------
        # LIGNE DANGEREUSE MAIS TOUJOURS PASSABLE
        # -------------------------------------------------

        all_lanes = [0, 1, 2]

        # choix d'obstacles (jamais 3)
        nb_obstacles = random.choice([1, 2])

        blocked = random.sample(all_lanes, nb_obstacles)

        safe_lane = list(set(all_lanes) - set(blocked))

        # sécurité absolue
        if len(safe_lane) == 0:
            blocked = [0, 1]
            safe_lane = [2]

        for i in blocked:

            x = self.positions_x[i]

            if self.niveau == 1:
                type_path = random.choice(self.dechets_niveau_1)
                velocity = 2
            else:
                type_path = random.choice(self.dechets_niveau_2)
                velocity = 3

            dechet = Dechet(type_path)
            dechet.image_path = type_path
            dechet.rect.centerx = x
            dechet.rect.y = self.spawn_y
            dechet.velocity = velocity

            self.all_dechet.add(dechet)

        self.spawn_pattern_step += 1

    def update_timer(self):
        if not self.partie_terminee:
            temps_ecoule = (pygame.time.get_ticks() - self.temps_depart) / 1000
            if temps_ecoule >= 10:
                self.partie_terminee = True

    def descendre_banquise(self):
        # La banquise descend tant que la partie est finie
        if self.partie_terminee and self.banquise_y < self.banquise_y_finale:
            self.banquise_y += 1.5

        # Quand elle arrive en bas
        if self.banquise_y >= self.banquise_y_finale:
            self.saut_possible = True

            # Donner le bonus UNE SEULE FOIS
            if not self.banquise_bonus_donne:
                self.points += 100
                self.ajouter_animation_points("+100", 540, 350)
                self.banquise_bonus_donne = True
    def faire_monter_calamar(self):
        temps = pygame.time.get_ticks() / 1000
        amplitude = 300
        vitesse = 0.8
        self.calamar_x = 450 + math.sin(temps * vitesse) * amplitude
        self.calamar_rect.x = self.calamar_x

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def gerer_collisions(self):
        if self.player.is_jumping:
            return
        if self.en_pause or self.partie_terminee:
            return

        collisions = self.check_collision(self.player, self.all_dechet)

        if collisions:
            dechet = collisions[0]
            chemin = dechet.image_path

            self.message_collision = self.dico_message.get(chemin, "Attention !")

            self.vies -= 1
            self.en_pause = True
            self.pause_type = "collision"

            if self.vies <= 0:
                self.partie_terminee = True
                self.game_over = True
                self.son_perdu.play()

    def fin_du_saut(self):
        dx = abs(self.cible_x - self.calamar_rect.centerx)
        dy = abs(self.cible_y - self.calamar_rect.centery)

        # --- SUCCÈS ---
        if dx < 80 and dy < 80:
            self.points += 50
            self.calamars += 1
            self.son_calamar.play()

            self.message_collision = "Bravo ! Tu as attrapé le calamar !"

        # --- ÉCHEC ---
        else:
            self.son_perdu.play()
            self.message_collision = "Dommage... tu n'as pas attrapé le calamar !"

        # FIN DE PARCOURS (PAS GAME OVER)
        self.parcours_termine = True
        self.game_over = False

    def ajouter_animation_points(self, texte, x, y):
        self.animations_points.append({
            "texte": texte,
            "x": x,
            "y": y,
            "alpha": 255
        })

    def update_animations(self):
        for anim in self.animations_points[:]:
            anim["y"] -= 1
            anim["alpha"] -= 3

            if anim["alpha"] <= 0:
                self.animations_points.remove(anim)

    def changer_skin(self, skin):
        if skin == "normal":
            self.skin_actuel = "normal"
            self.player = Player("Pingu écolo! - assets/Pingu simple .png")
        elif skin == "rose" and self.pingu_rose_debloque:
            self.skin_actuel = "rose"
            self.player = Player("Pingu écolo! - assets/Pingu rose.png")
        elif skin == "dore" and self.pingu_dore_debloque:
            self.skin_actuel = "dore"
            self.player = Player("Pingu écolo! - assets/Pingu dore.png")

        # IMPORTANT : On redonne l'accès au jeu au nouveau joueur
        self.player.game = self

    def acheter(self, item):
        if item == "niveau2":
            if self.niveau2_debloque:
                return "Niveau 2 déjà débloqué !"

            if self.points >= 500:
                self.points -= 500
                self.niveau2_debloque = True

                # son
                self.son_passage_1_2.play()

                return "Niveau 2 débloqué !"
            else:
                return "Pas assez de points !"

        # --- PINGU ROSE ---
        if item == "rose":
            if self.calamars >= 3:
                self.calamars -= 3
                self.pingu_rose_debloque = True
                self.son_achat.play()
                return "Pingu rose débloqué !"
            else:
                return "Pas assez de calamars !"

        # --- PINGU DORÉ ---
        if item == "dore":
            if not self.niveau2_debloque:
                return "Tu dois d'abord débloquer le niveau 2 !"

            if self.calamars >= 5:
                self.calamars -= 5
                self.pingu_dore_debloque = True
                self.son_achat.play()
                return "Pingu doré débloqué !"
            else:
                return "Pas assez de calamars !"

    def update_cible(self):
        self.cible_x += (self.target_cible_x - self.cible_x) * self.cible_vitesse
        self.cible_y += (self.target_cible_y - self.cible_y) * self.cible_vitesse