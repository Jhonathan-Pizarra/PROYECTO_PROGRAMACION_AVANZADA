
from Person import Person

class Jugador(Person):
    def __init__(self, raw_image, position):
        super(Jugador, self).__init__(raw_image, position)
        self.isJumping = 0
        self.onLadder = 0
        self.currentJumpSpeed = 0
        self.__gravity = 1  # Afecta el personaje la gravedad
        self.__speed = 5

    # Getters and Setters
    def getSpeed(self):
        return self.__speed

    def setSpeed(self):
        return self.__speed

    def continuousUpdate(self, wallGroupList, ladderGroupList):  # Solo el jugador puede saltar
        if self.onLadder == 0:
            wallsCollided = self.checkCollision(wallGroupList)
            if self.isJumping == 0:
                self.updateY(2)
                laddersCollided = self.checkCollision(ladderGroupList)
                wallsCollided = self.checkCollision(wallGroupList)
                self.updateY(-2)
                if len(wallsCollided) == 0 and len(laddersCollided) == 0:
                    self.isJumping = 1
                    self.currentJumpSpeed = 0
            if self.isJumping:
                if wallsCollided:
                    if wallsCollided[0].getPosition()[1] > self.getPosition()[1]:
                        self.isJumping = 0
                        self.setPosition(((self.getPosition()[0], wallsCollided[0].getPosition()[
                            1] - 16)))
                    elif wallsCollided[0].getPosition()[1] < self.getPosition()[1]:
                        self.currentJumpSpeed = 0
                        self.setPosition((self.getPosition()[0], wallsCollided[0].getPosition()[1] + 16))
                self.setCenter(self.getPosition())
                if self.isJumping:
                    self.updateY(-self.currentJumpSpeed)
                    self.setCenter(self.getPosition())
                    self.currentJumpSpeed -= self.__gravity
                    if self.currentJumpSpeed < -8:
                        self.currentJumpSpeed = -8
