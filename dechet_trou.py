import pygame

dico_message = {
    'Pingu écolo! - assets/compote dechet.png': " ",
    'Pingu écolo! - assets/bouteille dechet.png': " ",
    'Pingu écolo! - assets/gateau dechet.png': " ",
    'Pingu écolo! - assets/trou banquise.png': " "
}

class Dechet(pygame.sprite.Sprite):
    def __init__(self, type_path):
        super().__init__()

        # Charger l'image avec transparence
        self.image = pygame.image.load(type_path).convert_alpha()

        # Redimensionner SANS déformer (hauteur fixe)
        nouvelle_hauteur = 150
        original_width = self.image.get_width()
        original_height = self.image.get_height()

        ratio = nouvelle_hauteur / original_height
        nouvelle_largeur = int(original_width * ratio)

        self.image = pygame.transform.scale(self.image, (nouvelle_largeur, nouvelle_hauteur))

        # Le rect doit être créé APRÈS le scale
        self.rect = self.image.get_rect()

        self.message = dico_message[type_path]

        # vitesse par défaut
        self.velocity = 2

    def update(self):
        self.rect.y += self.velocity