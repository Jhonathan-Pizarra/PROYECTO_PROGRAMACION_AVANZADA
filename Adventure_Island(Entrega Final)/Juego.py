
import pygame
import sys
from pygame.locals import *
from Board import Board
from Button import Button
from Ajustes import *
from pygame import mixer

class Game:

    def __init__(self):

        self.height = 520
        self.width = 1200
        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.displayScreen = pygame.display.set_mode((self.width, self.height))


        self.myFont = pygame.font.SysFont("comicsansms", 30)


        self.newGame = Board(self.width, self.height)
        self.fireballTimer = 0
        self.playerGroup = self.newGame.playerGroup
        self.wallGroup = self.newGame.wallGroup
        self.ladderGroup = self.newGame.ladderGroup


    def runGame(self):


        while 1:

            self.clock.tick(self.FPS)
            self.scoreLabel = self.myFont.render(str(self.newGame.score), 1,(0, 0, 0))
            segundos = pygame.time.get_ticks() / 1000
            self.timeLabel= self.myFont.render(str(segundos),1,(0,0,0))

            if self.newGame.gameState != 1:


                self.newGame.checkButton()
                self.newGame.redrawScreen(self.displayScreen, self.scoreLabel,self.timeLabel, self.width,
                                          self.height)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.newGame.processButton()
                        self.playerGroup = self.newGame.playerGroup
                        self.wallGroup = self.newGame.wallGroup
                        self.ladderGroup = self.newGame.ladderGroup
            if self.newGame.gameState == 1:

                self.fireballGroup = self.newGame.fireballGroup
                self.coinGroup = self.newGame.coinGroup

                if self.fireballTimer == 0:
                    self.newGame.CreateFireball(self.newGame.Enemies[0].getPosition(), 0)
                elif len(self.newGame.Enemies) >= 2 and self.fireballTimer == 23:
                    self.newGame.CreateFireball(self.newGame.Enemies[1].getPosition(), 1)
                elif len(self.newGame.Enemies) >= 3 and self.fireballTimer == 46:
                    self.newGame.CreateFireball(self.newGame.Enemies[2].getPosition(), 2)
                self.fireballTimer = (self.fireballTimer + 1) % 70
                #Animacion del coin
                for coin in self.coinGroup:
                    coin.animateCoin()
                self.newGame.Players[0].updateY(2)
                self.laddersCollidedBelow = self.newGame.Players[0].checkCollision(self.ladderGroup)
                self.wallsCollidedBelow = self.newGame.Players[0].checkCollision(self.wallGroup)
                self.newGame.Players[0].updateY(-2)
                self.newGame.Players[0].updateY(-2)
                self.wallsCollidedAbove = self.newGame.Players[0].checkCollision(self.wallGroup)
                self.newGame.Players[0].updateY(2)
                self.newGame.ladderCheck(self.laddersCollidedBelow, self.wallsCollidedBelow, self.wallsCollidedAbove)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:

                        self.laddersCollidedExact = self.newGame.Players[0].checkCollision(self.ladderGroup)
                        if event.key == K_q:
                            self.newGame.gameState = 2
                            self.newGame.ActiveButtons[0] = 0
                            self.newGame.ActiveButtons[1] = 1
                            self.newGame.ActiveButto
                            ns[2] = 1
                            self.Button = Button(pygame.load.image("Assets/score.png"), (900,400),"Score")

                        if (event.key == K_SPACE and self.newGame.Players[0].onLadder == 0) or (
                                event.key == K_w and self.laddersCollidedExact):
                            self.direction = 2
                            if self.newGame.Players[0].isJumping == 0 and self.wallsCollidedBelow:
                                self.newGame.Players[0].isJumping = 1
                                self.newGame.Players[0].currentJumpSpeed = 7
                                if event.key == K_SPACE:
                                    jump_sound.play()
                                    """mixer.music.load('Assets/jump.wav')
                                    mixer.music.set_volume(2)
                                    pygame.mixer.music.play()"""




                self.newGame.Players[0].continuousUpdate(self.wallGroup, self.ladderGroup)

                keyState = pygame.key.get_pressed()
                if keyState[pygame.K_d]:
                    if self.newGame.direction != 4:
                        self.newGame.direction = 4
                        self.newGame.cycles = -1
                    self.newGame.cycles = (self.newGame.cycles + 1) % 10
                    if self.newGame.cycles < 5:
                        self.newGame.Players[0].updateWH(pygame.image.load('Assets/higinright1.png'), "H",
                                                         self.newGame.Players[0].getSpeed(), 20, 20)
                    else:
                        self.newGame.Players[0].updateWH(pygame. image.load('Assets/higinright2.png'), "H",
                                                         self.newGame.Players[0].getSpeed(), 20, 20)
                    wallsCollidedExact = self.newGame.Players[0].checkCollision(self.wallGroup)


                if keyState[pygame.K_a]:
                    if self.newGame.direction != 3:
                        self.newGame.direction = 3
                        self.newGame.cycles = -1
                    self.newGame.cycles = (self.newGame.cycles + 1) % 10
                    if self.newGame.cycles < 5:
                        self.newGame.Players[0].updateWH(pygame.image.load('Assets/higinleft1.png'), "H",
                                                         -self.newGame.Players[0].getSpeed(), 20, 20)
                    else:
                        self.newGame.Players[0].updateWH(pygame.image.load('Assets/higinleft2.png'), "H",
                                                         -self.newGame.Players[0].getSpeed(), 20, 20)
                    wallsCollidedExact = self.newGame.Players[0].checkCollision(self.wallGroup)
                    if wallsCollidedExact:
                        self.newGame.Players[0].updateWH(pygame.image.load('Assets/higinleft1.png'), "H",
                                                         self.newGame.Players[0].getSpeed(), 20, 20)
                if keyState[pygame.K_w] and self.newGame.Players[0].onLadder:
                    self.newGame.Players[0].updateWH(pygame.image.load('Assets/still.png'), "V",
                                                     -self.newGame.Players[0].getSpeed() / 2, 25, 25)
                    if len(self.newGame.Players[0].checkCollision(self.ladderGroup)) == 0 or len(
                            self.newGame.Players[0].checkCollision(self.wallGroup)) != 0:
                        self.newGame.Players[0].updateWH(pygame.image.load('Assets/higinright1.png'), "V",
                                                         self.newGame.Players[0].getSpeed() / 2, 25,25 )
                if keyState[pygame.K_s] and self.newGame.Players[0].onLadder:
                    self.newGame.Players[0].updateWH(pygame.image.load('Assets/still2.png'), "V",
                                                     self.newGame.Players[0].getSpeed() / 2, 25, 25)
                self.newGame.redrawScreen(self.displayScreen, self.scoreLabel,self.timeLabel, self.width, self.height)
                self.newGame.fireballCheck()
                coinsCollected = pygame.sprite.spritecollide(self.newGame.Players[0], self.coinGroup, True)
                self.newGame.coinCheck(coinsCollected)
                self.newGame.checkVictory(self.clock)
                for enemy in self.newGame.Enemies:
                    enemy.continuousUpdate(self.wallGroup, self.ladderGroup)

            pygame.display.update()




if __name__ == "__main__":

    pygame.init()
    mixer.init()
    createdGame = Game()
    createdGame.runGame()



