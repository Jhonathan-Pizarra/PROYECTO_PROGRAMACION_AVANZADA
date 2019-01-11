import pygame


class OnBoard(pygame.sprite.Sprite):
    def __init__(self, raw_image, position):
        super(OnBoard, self).__init__()
        self.__position = position
        self.image = raw_image
        self.image = pygame.transform.scale(self.image,
                                            (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = self.__position

    # Getters and Setters
    def setCenter(self, position):
        self.rect.center = position

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    # Actualizar imagenes
    def updateImage(self, raw_image):  # Abstracto metodo
        raise NotImplementedError("Subclass must implement this")

    # Modificar el tamaño
    def modifySize(self, raw_image, height, width):
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (width, height))
    def cro(self):
        segundos = pygame.time.get_ticks() / 1000
        return segundos

