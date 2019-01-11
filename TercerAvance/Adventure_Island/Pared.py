
from OnBoard import OnBoard
import pygame

class Pared(OnBoard):
    def __init__(self, raw_image, position):
        super(Pared, self).__init__(raw_image, position)

    def updateImage(self, raw_image):
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (15, 15))