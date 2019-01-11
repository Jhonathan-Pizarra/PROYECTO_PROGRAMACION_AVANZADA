
import pygame
import random
import math
from OnBoard import OnBoard


class Bola(OnBoard):
    def __init__(self, raw_image, position, index,speed):
        super(Bola,self).__init__(raw_image, position)
        self.__direction = int(math.floor(random.random() * 100)) % 2
        self.index = index
        self.wallsBelow = []
        self.laddersBelow = []
        self.__fall = 0
        self.__speed = speed

    #Cargar la imagen de la bola
    def updateImage(self, raw_image):
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (15, 15))

    #Getters and Setters
    def getSpeed(self):
        return self.__speed
    def setSpeed(self,speed):
        self.__speed = speed
    def getFall(self):
        return self.__fall
    def getDirection(self):
        return self.__direction

    def continuousUpdate(self, wallGroup, ladderGroup):

        #la bola esta cayendo
        if self.__fall == 1:
            self.update(self.image, "V", self.__speed)
            if self.checkCollision(wallGroup, "V"):
                self.__fall = 0
                self.__direction = int(math.floor(random.random() * 100)) % 2

        else:

            if self.checkCollision(ladderGroup, "V") and len(self.checkCollision(wallGroup, "V")) == 0:
                randVal = int(math.floor(random.random() * 100)) % 20
                if randVal < 15:
                    self.__fall = 0
                else:
                    self.__fall = 1

            if len(self.checkCollision(ladderGroup, "V")) == 0 and len(self.checkCollision(wallGroup, "V")) == 0:
                self.__fall = 1

            if self.__direction == 0:
                self.update(pygame.image.load('Assets/garyright.png'), "H", self.__speed)
                if self.checkCollision(wallGroup, "H"):
                    self.__direction = 1
                    self.update(self.image, "H", -self.__speed)

            else:
                self.update(pygame.image.load('Assets/garyleft.png'), "H", -self.__speed)
                if self.checkCollision(wallGroup, "H"):
                    self.__direction = 0
                    self.update(self.image, "H", self.__speed)

    def update(self, raw_image, direction, value):
        if direction == "H":
            self.setPosition((self.getPosition()[0] + value, self.getPosition()[1]))
            self.image = raw_image
            self.image = pygame.transform.scale(self.image, (15, 15))
        if direction == "V":
            self.setPosition((self.getPosition()[0], self.getPosition()[1] + value))
        self.rect.center = self.getPosition()

    def checkCollision(self, colliderGroup, direction):
        if direction == "H":
            if self.__direction == 0:
                self.update(self.image, "H", self.__speed)
            if self.__direction == 1:
                self.update(self.image, "H", -self.__speed)
            Colliders = pygame.sprite.spritecollide(self, colliderGroup, False)
            if self.__direction == 0:
                self.update(self.image, "H", -self.__speed)
            if self.__direction == 1:
                self.update(self.image, "H", self.__speed)
        else:
            self.update(self.image, "V", self.__speed)
            Colliders = pygame.sprite.spritecollide(self, colliderGroup, False)
            self.update(self.image, "V", -self.__speed)
        return Colliders
