import pygame

class SoundManager:

    def __init__(self):
        self.sounds = {
            'calamar' : pygame.mixer.Sound("sounds/calamar.ogg"),
            'deplacement_personnage': pygame.mixer.Sound("sounds/deplacement_perso.ogg"),
            'nouveau_personnage': pygame.mixer.Sound("sounds/nouveau_personnage.ogg"),
            'passage_niveau_2': pygame.mixer.Sound("sounds/passage_1_a_2.ogg"),
            'perdu': pygame.mixer.Sound("sounds/perdu.ogg"),
        }


    def play(self, sound):
        self.sounds[sound].play()