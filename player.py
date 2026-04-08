import pygame
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, skin_path):
        super().__init__()
        self.vie = 3
        self.max_vie = 3
        self.velocity = 5
        self.image = pygame.image.load(skin_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (360, 240))
        self.rect = self.image.get_rect()
        self.rect.x = 360
        self.rect.y = 500

    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    # --- AJOUT POUR CHANGER DE SKIN ---
    def change_skin(self, skin_path):
        """Change l'image du joueur sans modifier le reste."""
        self.image = pygame.image.load(skin_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (360, 240))