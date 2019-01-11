
import pygame



class Person(pygame.sprite.Sprite):
    def __init__(self, raw_image, position):
        super(Person, self).__init__()
        self.__position = position
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = self.__position

    def getSpeed(self):  # Metodo Abstracto
        raise NotImplementedError("Subclass must implement this")

    def setSpeed(self):  # Metodo Abstracto
        raise NotImplementedError("Subclass must implement this")

    # Getters and Setters
    def setCenter(self, position):
        self.rect.center = position

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    # Mover la persona horizontal ("H") o vertical ("V")
    def updateWH(self, raw_image, direction, value, height, width):
        if direction == "H":
            self.__position = (self.__position[0] + value, self.__position[1])
        if direction == "V":
            self.__position = (self.__position[0], self.__position[1] + value)
        self.image = raw_image
        # Carga la imagen con el tamaño especifico
        self.image = pygame.transform.scale(self.image, (height, width))
        self.rect.center = self.__position

    # Para el movimiento Vertical
    def updateY(self, value):
        self.__position = (self.__position[0], self.__position[1] + value)
        self.rect.center = self.__position

    # obtiene una lista de colisiones para poder chequear si person tiene una colision con algo
    def checkCollision(self, colliderGroup):
        Colliders = pygame.sprite.spritecollide(self, colliderGroup, False)
        return Colliders

    #Este es otro metodo Abstracto
    def continuousUpdate(self, GroupList,GroupList2):
    # continuousUpdate mira los objetos de colision
        raise NotImplementedError("Subclass must implement this")
