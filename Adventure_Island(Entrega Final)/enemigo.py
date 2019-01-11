import pygame
from Person import Person
import random

class enemigo(Person):
    def __init__(self, raw_image, position):
        super(enemigo, self).__init__(raw_image, position)
        self.__speed = 2
        self.__direction = int(random.random() * 100) % 2
        self.__cycles = 0
        self.__stopDuration = 0

    # Getters and Setters
    def getSpeed(self):
        return self.__speed

    def setSpeed(self):
        return self.__speed

    def getStopDuration(self):
        return self.__stopDuration

    def setStopDuration(self, stopDuration):
        self.__stopDuration = stopDuration

    def checkWall(self, colliderGroup):
        if self.__direction == 0:
            self.updateWH(self.image, "H", 20, 40, 40)
        if self.__direction == 1:
            self.updateWH(self.image, "H", -20, 40, 40)
        Colliders = pygame.sprite.spritecollide(self, colliderGroup, False)
        if self.__direction == 0:
            self.updateWH(self.image, "H", -20, 40, 40)
        if self.__direction == 1:
            self.updateWH(self.image, "H", 20, 40, 40)
        return Colliders

    def continuousUpdate(self, GroupList, GroupList2):

        if self.__stopDuration == 0:
            if self.__direction == 0:
                self.__cycles += 1
                if self.__cycles % 24 < 6:
                    self.updateWH(pygame.image.load('Assets/rinoright.png'), "H", self.__speed, 40, 40)
                elif self.__cycles % 24 < 12:
                    self.updateWH(pygame.image.load('Assets/rinoright.png'), "H", self.__speed, 40, 40)
                elif self.__cycles % 24 < 18:
                    self.updateWH(pygame.image.load('Assets/rinoright.png'), "H", self.__speed, 40, 40)
                else:
                    self.updateWH(pygame.image.load('Assets/rinoright.png'), "H", self.__speed, 40, 40)
                if self.checkWall(GroupList):
                    self.__direction = 1
                    self.__cycles = 0
                    self.updateWH(self.image, "H", -self.__speed, 40, 40)
            else:
                self.__cycles += 1
                if self.__cycles % 24 < 6:
                    self.updateWH(pygame.image.load('Assets/rinoleft.png'), "H", -self.__speed, 45, 45)
                elif self.__cycles % 24 < 12:
                    self.updateWH(pygame.image.load('Assets/rinoleft.png'), "H", -self.__speed, 45, 45)
                elif self.__cycles % 24 < 18:
                    self.updateWH(pygame.image.load('Assets/rinoleft.png'), "H", -self.__speed, 45, 45)
                else:
                    self.updateWH(pygame.image.load('Assets/rinoleft.png'), "H", -self.__speed, 45, 45)
                if self.checkWall(GroupList):
                    self.__direction = 0
                    self.__cycles = 0
                    self.updateWH(self.image, "H", self.__speed, 45, 45)
        else:
            self.__stopDuration -= 1
            if self.__stopDuration == 0:
                self.updateWH(self.image, "V", 12, 50, 50)
            if self.__stopDuration >= 10:
                if self.__direction == 0:
                    self.updateWH(pygame.image.load('Assets/rinoright.png'), "H", 0, 50, 50)
                else:
                    self.updateWH(pygame.image.load('Assets/rinoleft.png'), "H", 0, 50, 50)
            elif self.__stopDuration >= 5:
                if self.__direction == 0:
                    self.updateWH(pygame.image.load('Assets/rinoright.png'), "H", 0, 50, 50)
                else:
                    self.updateWH(pygame.image.load('Assets/rinoleft.png'), "H", 0, 50, 50)
            else:
                if self.__direction == 0:
                    self.updateWH(pygame.image.load('Assets/rinoright.png'), "H", 0, 50, 50)
                else:
                    self.updateWH(pygame.image.load('Assets/rinoleft.png'), "H", 0, 50, 50)
