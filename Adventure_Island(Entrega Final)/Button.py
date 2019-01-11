
class Button:
    def __init__(self, raw_image, position, nameStr):
        self.image = raw_image
        self.__position = position
        self.rect = self.image.get_rect()
        self.rect.center = self.__position
        self.name = nameStr

    def changeImage(self, raw_image):
        self.image = raw_image

    def getTopLeftPosition(self):
        return (self.__position[0] - self.rect.width / 2, self.__position[1] - self.rect.height / 2)

    # Getters and Setters
    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position
