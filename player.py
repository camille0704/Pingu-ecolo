import pygame
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, skin_path):
        super().__init__()

        self.vie = 3
        self.max_vie = 3

        # --- LANES ---
        self.lanes = [180, 540, 900]
        self.lane_index = 1

        self.image = pygame.image.load(skin_path).convert_alpha()
        self.rect = self.image.get_rect()

        # position de départ
        self.rect.centerx = self.lanes[self.lane_index]
        self.rect.y = 460

        # vitesse de glissement (PLUS GRAND = plus rapide)
        self.lane_speed = 0.12

        # position cible
        self.target_x = self.rect.centerx
        self.target_x_jump = self.rect.centerx

        # saut
        self.is_jumping = False
        self.jump_time = 0
        self.jump_duration = 80

        self.start_x = 0
        self.start_y = 0
        self.target_y = 0

    # -------------------------------------------------
    # INPUT LANES (ne change plus instantanément)
    # -------------------------------------------------
    def move_left(self):
        # seulement si pas déjà tout à gauche
        if self.lane_index > 0:
            self.lane_index -= 1
            self.target_x = self.lanes[self.lane_index]

    def move_right(self):
        # seulement si pas déjà tout à droite
        if self.lane_index < 2:
            self.lane_index += 1
            self.target_x = self.lanes[self.lane_index]

    # -------------------------------------------------
    # UPDATE SMOOTH MOVEMENT
    # -------------------------------------------------
    def update(self):
        # déplacement vers la lane cible
        dx = self.target_x - self.rect.centerx

        # vitesse plus stable (anti dépassement)
        self.rect.centerx += dx * self.lane_speed

        # snap final pour éviter glitch
        if abs(dx) < 1:
            self.rect.centerx = self.target_x

    # -------------------------------------------------
    def change_skin(self, skin_path):
        self.image = pygame.image.load(skin_path).convert_alpha()

    # -------------------------------------------------
    def jump(self, calamar_x, calamar_y):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_time = 0

            self.start_x = self.rect.centerx
            self.start_y = self.rect.centery

            self.target_y = calamar_y
            self.target_x_jump = calamar_x

    # -------------------------------------------------
    def update_jump(self):
        if self.is_jumping:
            t = self.jump_time / self.jump_duration

            self.rect.centerx = (1 - t) * self.start_x + t * self.target_x_jump

            h = -300
            y = (1 - t) * self.start_y + t * self.target_y + h * (1 - (2 * t - 1) ** 2)
            self.rect.centery = y

            self.jump_time += 1

            if self.jump_time >= self.jump_duration:
                self.is_jumping = False
                self.rect.centery = self.target_y + 50
                self.game.fin_du_saut()