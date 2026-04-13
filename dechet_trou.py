import pygame

dico_message = {
    'Pingu écolo! - assets/compote dechet.png': " compote",
    'Pingu écolo! - assets/bouteille dechet.png': " bouteille",
    'Pingu écolo! - assets/gateau dechet.png': " gateau",
    'Pingu écolo! - assets/trou banquise.png': "trou "
}

class Dechet(pygame.sprite.Sprite):
    def __init__(self, type_path):
        super().__init__()

        self.image = pygame.image.load(type_path).convert_alpha()

        # NOUVELLE TAILLE FIXE : 200×200
        self.image = pygame.transform.scale(self.image, (190, 190))

        self.rect = self.image.get_rect()
        self.message = dico_message[type_path]
        self.velocity = 2

    def update(self):
        self.rect.y += self.velocity