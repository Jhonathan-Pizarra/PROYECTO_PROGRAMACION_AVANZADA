import pygame
import math
import random
import sys
import os

from pygame import mixer
from Person import Person
from OnBoard import OnBoard
from Ajustes import *
from Coin import Coin
from Jugador import Jugador
from Bola import Bola
from enemigo import enemigo
from Button import Button

# Inicializacion del mixer
mixer.init()



class Board:
    def __init__(self, width, height):
        self.__width = width
        self.__actHeight = height
        self.__height = self.__actHeight + 10
        self.score = 0
        self.gameState = 0
        self.cycles = 0  # Se utiliza para la animacion de los objetos
        self.direction = 0

        self.white = (255, 255, 255)


        self.map = []
        # Este array contiene todas las instancias de los objetos de nuestro juego
        self.Players = self.Enemies = self.Allies = self.Coins = self.Walls = self.Ladders = self.Fireballs = self.Hearts = self.Boards = self.FireballEndpoints = []

        # Reiniciamos los grupos y inicializamos de nuevo
        self.resetGroups()

        # Colocamos los botones que usamos
        self.Buttons = [Button(pygame.image.load('Assets/start.png'), (500, 400), "Inicio"),
                        Button(pygame.image.load('Assets/exit.png'), (700, 400), "Salir"),
                        Button(pygame.image.load('Assets/restart.png'), (500, 400), "Reiniciar"),
                        ]

        self.ActiveButtons = [1, 1, 0]  # Initially de los botones
        self.myfont = pygame.font.SysFont("comicsansms", 50)

        self.background = pygame.image.load('Assets/Fondo2.jpg')
        self.background = pygame.transform.scale(self.background, (width, height))
        self.startbackground = pygame.image.load('Assets/Revenge.jpg')
        #mixer.music.load('Assets/AdventureMP4.ogv')#InicioALV.wav
        #mixer.music.set_volume(1)
        pygame.mixer.music.load(os.path.join('Assets/AdventureMP4.ogv'))
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()
        self.startbackground = pygame.transform.scale(self.startbackground, (width, height))

        # Iniciamos grupos para otras instancias

        self.fireballGroup = pygame.sprite.RenderPlain(self.Fireballs)
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.enemyGroup = pygame.sprite.RenderPlain(self.Enemies)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.ladderGroup = pygame.sprite.RenderPlain(self.Ladders)
        self.coinGroup = pygame.sprite.RenderPlain(self.Coins)
        self.allyGroup = pygame.sprite.RenderPlain(self.Allies)
        self.fireballEndpointsGroup = pygame.sprite.RenderPlain(self.FireballEndpoints)
        self.boardGroup = pygame.sprite.RenderPlain(self.Boards)
        self.heartGroup = pygame.sprite.RenderPlain(self.Hearts)
    def resetGroups(self):

        self.score = 0
        self.map = []  # Nosotros creamos el mapa para luego poder reiniciar si es el caso
        self.Players = [Jugador(pygame.image.load('Assets/still.png'), (50, 440))]
        self.Enemies = [enemigo(pygame.image.load('Assets/rinoright.png'), (100, 117))]
        self.Allies = [Jugador(pygame.image.load('Assets/princess.png'), (50, 55))]
        self.Allies[0].updateWH(self.Allies[0].image, "H", 0, 25, 25)
        self.Coins = []
        self.Walls = []
        self.Ladders = []
        self.Fireballs = []
        self.Hearts = [OnBoard(pygame.image.load('Assets/heart.png'), (595, 490)),
                       OnBoard(pygame.image.load('Assets/heart.png'), (615, 490)),
                       OnBoard(pygame.image.load('Assets/heart.png'), (635, 490)),
                       ]
        self.Hearts[0].modifySize(pygame.image.load('Assets/heart.png'), 20, 20)
        self.Hearts[1].modifySize(pygame.image.load('Assets/heart.png'), 20, 20)
        self.Hearts[2].modifySize(pygame.image.load('Assets/heart.png'), 20, 20)
        self.Boards = [OnBoard(pygame.image.load('Assets/board.png'), (200, 480)),
                       OnBoard(pygame.image.load('Assets/board.png'), (550, 480)),
                       OnBoard(pygame.image.load('Assets/board.png'),(900,480))
                       ]

        self.Boards[0].modifySize(self.Boards[0].image, 40, 150)  #Modificamos los Boards
        self.Boards[1].modifySize(self.Boards[1].image, 40, 150)
        self.Boards[2].modifySize(self.Boards[2].image,40,150)

        self.FireballEndpoints = [OnBoard(pygame.image.load('Assets/higinright1.png'), (500, 900))]
        self.initializeGame()
        self.createGroups()

    def checkFireballDestroy(self, fireball):
        if pygame.sprite.spritecollide(fireball, self.fireballEndpointsGroup, False):
            self.DestroyFireball(fireball.index)  # usamos indeces para poder ver que la bola se destruya

    # Creamos una bola dentro de nuestro grupo
    def CreateFireball(self, location, kongIndex):
       if len(self.Fireballs) < len(self.Enemies) * 6+6:
            self.Fireballs.append(
                Bola(pygame.image.load('Assets/garyright.png'), (location[0], location[1] + 15), len(self.Fireballs),
                         2 + len(self.Enemies)/2))
            # Iniciamos la animacion de Donk King Kong
            self.Enemies[kongIndex].setStopDuration(15)
            self.Enemies[kongIndex].setPosition(
                (self.Enemies[kongIndex].getPosition()[0], self.Enemies[kongIndex].getPosition()[1] - 12))
            self.Enemies[kongIndex].setCenter(self.Enemies[kongIndex].getPosition())

            self.createGroups()  # Nosotros creamos el grupo nuevamente

    # Destroy a fireball
    def DestroyFireball(self, index):
        for fireBall in range(len(self.Fireballs)):
            if self.Fireballs[fireBall].index == index:
                self.Fireballs.remove(self.Fireballs[fireBall])
                for fireBallrem in range(
                        len(self.Fireballs)):  # Nosotros reducimos los indices de todas las bolas
                    if self.Fireballs[fireBallrem].index > index:
                        self.Fireballs[fireBallrem].index -= 1
                self.createGroups()  # Recrear los grupos para remover
                break

    # Generar monedas en el nivel
    def GenerateCoins(self):
        for i in range(6, len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 0 and ((i + 1 < len(self.map) and self.map[i + 1][j] == 1) or (
                            i + 2 < len(self.map) and self.map[i + 2][j] == 1)):
                    randNumber = math.floor(random.random() * 1000)
                    if randNumber % 35 == 0 and len(self.Coins) <= 25:  # Se va a crear un maximo de 26 monedas
                        self.map[i][j] = 3
                        if j - 1 >= 0 and self.map[i][j - 1] == 3:
                            self.map[i][j] = 0
                        if self.map[i][j] == 3:
                            # agregar un coin a nuestro grupo
                            self.Coins.append(Coin(pygame.image.load('Assets/Apple.png'), (j * 15 + 15 / 2, i * 15 + 15 / 2)))
        if len(self.Coins) <= 20:  # si estan menos de 21 coins el programa se vuelva a generar
            self.GenerateCoins()

    # Obtiene una  posiion y checkNo
    def checkMapForMatch(self, placePosition, floor, checkNo, offset):
        if floor < 1:
            return 0
        for i in range(0, 5):
            if self.map[floor * 5 - offset][placePosition + i] == checkNo:
                return 1
            if self.map[floor * 5 - offset][placePosition - i] == checkNo:
                return 1
        return 0

    # Crear una mapa de  30x80
    def makeMap(self):

        anchura = int(self.__height / 15 + 1)
        for point in range(0,anchura ):
            row = []
            altura = int(self.__width / 15)
            for point2 in range(0, altura):
                row.append(0)
            self.map.append(row)

    # Agregar pared a nuestro mapa y tambien a nuestras limites del piso
    def makeWalls(self):
        anchura = int((self.__height / 15) - 4)
        for i in range(0, anchura):
            indice = int(self.__width / 15 - 1)
            self.map[i][0] = self.map[i][indice] = 1
        altura = int((self.__height / (15 * 5)))
        for i in range(0, altura):
            limite = int(self.__width / 15)
            for j in range(0, limite):
                self.map[i * 5][j] = 1

    # Hacer la jaula para la princesa
    def makePrincessChamber(self):
        for j in range(0, 5):
            self.map[j][9] = 1

        limite = int((self.__width / 15) - 1)
        for j in range(10, limite):
            self.map[1 * 5][j] = 0
        for j in range(0, 5):
            self.map[1 * 5 + j][7] = self.map[1 * 5 + j][8] = 2

    # Generar las escaleras
    def makeLadders(self):
        anchura = int(self.__height / (15 * 5) - 1)
        for i in range(2, anchura):
            ladderPos = math.floor(random.random() * (self.__width / 15 - 20))
            ladderPos = int(10 + ladderPos)
            while self.checkMapForMatch(ladderPos, i - 1, 2, 0) == 1:
                ladderPos = math.floor(random.random() * (self.__width / 15 - 20))
                ladderPos = int(10 + ladderPos)
            for k in range(0, 5):
                self.map[i * 5 + k][ladderPos] = self.map[i * 5 + k][ladderPos + 1] = 2

    # Generar las escaleras rotas
    def makeBrokenLadders(self):
        anchura = int(self.__height / (15 * 5)-1)
        for i in range(2, anchura):
            if i % 2 == 1:
                brokenLadderPos = math.floor(random.random() * (self.__width / 15 - 20))
                brokenLadderPos = int(10 + brokenLadderPos)
                while self.checkMapForMatch(brokenLadderPos, i - 1, 2, 0) == 1 or self.checkMapForMatch(brokenLadderPos,i, 2,0) == 1 or self.checkMapForMatch(brokenLadderPos, i + 1, 2, 0) == 1:
                    brokenLadderPos = math.floor(random.random() * (self.__width / 15 - 20))
                    brokenLadderPos = int(10 + brokenLadderPos)
                brokenRand = int(math.floor(random.random() * 100)) % 2
                brokenRand2 = int(math.floor(random.random() * 100)) % 2
                for k in range(0, 1):
                    self.map[i * 5 + k][brokenLadderPos] = self.map[i * 5 + k][brokenLadderPos + 1] = 2
                for k in range(3 + brokenRand, 5):
                    self.map[i * 5 + k][brokenLadderPos] = 2
                for k in range(3 + brokenRand2, 5):
                    self.map[i * 5 + k][brokenLadderPos + 1] = 2

    # Crear los pisos
    def makeHoles(self):
        anchura = int(self.__height / (15 * 5)-1)
        for i in range(3, anchura):
            for k in range(1, 6):
                if i % 2 == 0:
                    self.map[i * 5][k] = 0
                else:
                    indice = int(self.__width / 15 - 1 - k)
                    self.map[i * 5][indice] = 0



    def populateMap(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 1:
                    self.Walls.append(OnBoard(pygame.image.load('Assets/cesped.png'), (y * 15 + 15 / 2, x * 15 + 15 / 2)))
                elif self.map[x][y] == 2:
                    self.Ladders.append(OnBoard(pygame.image.load('Assets/Lianas2.png'), (y * 15 + 15 / 2, x * 15 + 10 / 2)))

    # Verificar si el personaje esta en la escalera
    def ladderCheck(self, laddersCollidedBelow, wallsCollidedBelow, wallsCollidedAbove):
        if laddersCollidedBelow and len(wallsCollidedBelow) == 0:
            for ladder in laddersCollidedBelow:
                if ladder.getPosition()[1] >= self.Players[0].getPosition()[1]:
                    self.Players[0].onLadder = 1
                    self.Players[0].isJumping = 0
                    # verificar si existe colision en la escalera
                    if wallsCollidedAbove:
                        self.Players[0].updateY(3)

        else:
            self.Players[0].onLadder = 0

    # Verificar las posiciones de la bola y ver si existe colision
    def fireballCheck(self):
        for fireball in self.fireballGroup:
            fireball.continuousUpdate(self.wallGroup, self.ladderGroup)
            if fireball.checkCollision(self.playerGroup, "V"):
                if len(self.Hearts) >= 2:  # Reduce en 1 vida si existe colision
                    self.Fireballs.remove(fireball)
                    self.Hearts.pop(len(self.Hearts) - 1)
                    self.Players[0].setPosition((50, 440))
                    death_sound.play()
                    """mixer.music.load('Assets/death.wav')
                    mixer.music.set_volume(2)
                    pygame.mixer.music.play()"""
                    self.score -= 25
                    if self.score < 0:
                        self.score = 0
                    self.createGroups()
                else:
                    self.gameState = 2
                    self.ActiveButtons[0] = 0
                    self.ActiveButtons[1] = 1
                    self.ActiveButtons[2] = 1
            self.checkFireballDestroy(fireball)

    # Verificar la moneda
    def coinCheck(self, coinsCollected):
        for coin in coinsCollected:
            self.score += coin.collectCoin()
            indice1 = int((coin.getPosition()[1] - 15 / 2) / 15)
            indice2 = int((coin.getPosition()[0] - 15 / 2) / 15)
            self.map[indice1][indice2] = 0
            # Remover la moneda si existe
            self.Coins.remove(coin)
            # Cargar los nuevos grupos
            self.createGroups()

    # Verificar si existe victoria o no
    def checkVictory(self, clock):
        # Si tu tocas a la princesa ganas
        if self.Players[0].checkCollision(self.allyGroup) or self.Players[0].getPosition()[1] < 5 * 15:
            self.load_Data(str(self.score))
            mixer.music.load('Assets/levelcomplete.wav')  # Victory sound
            mixer.music.set_volume(2)
            pygame.mixer.music.play()
            clock.tick(100)
            self.score += 50
            self.Fireballs = []
            self.Players[0].setPosition((50, 440))
            self.Coins = []
            self.GenerateCoins()

            # Agregar Monito
            if len(self.Enemies) == 1:
                self.Enemies.append(enemigo(pygame.image.load('Assets/rinoright.png'), (700, 117)))
            elif len(self.Enemies) == 2:
                self.Enemies.append(enemigo(pygame.image.load('Assets/rinoright.png'), (400, 117)))
            # Create el grupo de los enemigos
            self.createGroups()

    def processButton(self):
        if self.ActiveButtons[0] == 1 and self.Buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
            self.resetGroups()
            self.gameState = 1
            self.ActiveButtons[0] = 0
            self.ActiveButtons[1] = 0
            self.ActiveButtons[2] = 0
        if self.ActiveButtons[1] == 1 and self.Buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
            pygame.quit()
            sys.exit()
        if self.ActiveButtons[2] == 1 and self.Buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
            self.gameState = 0
            self.ActiveButtons[0] = 1
            self.ActiveButtons[1] = 1
            self.ActiveButtons[2] = 0

    def checkButton(self):
        mousePosition = pygame.mouse.get_pos()
        for button in range(len(self.Buttons)):
            if self.ActiveButtons[button] == 1 and self.Buttons[button].rect.collidepoint(mousePosition):
                if button == 0:
                    self.Buttons[button].changeImage(pygame.image.load('Assets/start1.png'))
                elif button == 1:
                    self.Buttons[button].changeImage(pygame.image.load('Assets/exit1.png'))
                elif button == 2:
                    self.Buttons[button].changeImage(pygame.image.load('Assets/restart1.png'))
            else:
                if button == 0:
                    self.Buttons[button].changeImage(pygame.image.load('Assets/start.png'))
                elif button == 1:
                    self.Buttons[button].changeImage(pygame.image.load('Assets/exit.png'))
                elif button == 2:
                    self.Buttons[button].changeImage(pygame.image.load('Assets/restart.png'))

    def redrawScreen(self, displayScreen, scoreLabel,timeLabel,width, height):
        displayScreen.fill((0, 0, 0))
        if self.gameState != 1:
            displayScreen.blit(self.startbackground, self.startbackground.get_rect())


            if self.gameState == 2:
                label = self.myfont.render("Tu score es " + str(self.score), 1, (255, 255, 255))
                displayScreen.blit(label, (410, 70))
            for button in range(len(self.ActiveButtons)):
                if self.ActiveButtons[button] == 1:
                    displayScreen.blit(self.Buttons[button].image, self.Buttons[button].getTopLeftPosition())
        if self.gameState == 1:
            displayScreen.blit(self.background, self.background.get_rect())
            self.ladderGroup.draw(displayScreen)
            self.playerGroup.draw(displayScreen)
            self.coinGroup.draw(displayScreen)
            self.wallGroup.draw(displayScreen)
            self.fireballGroup.draw(displayScreen)
            self.enemyGroup.draw(displayScreen)
            self.allyGroup.draw(displayScreen)
            self.boardGroup.draw(displayScreen)
            displayScreen.blit(scoreLabel, (265-scoreLabel.get_width()/2, 470))
            displayScreen.blit(timeLabel,(920,470))
            self.heartGroup.draw(displayScreen)
    def load_Data(self, puntaje):
        archivo = open('Puntajes.txt', 'a')
        archivo.write('Puntaje: ' + str(puntaje) + ' \n')
        archivo.close()

    def read_Data(self):
        archivo = open('Puntajes.txt', 'r')
        linea = archivo.readline()
        while linea != "":
            print(linea)
            linea = archivo.readline()
        archivo.close()
    # Crear grupos
    def createGroups(self):
        self.fireballGroup = pygame.sprite.RenderPlain(self.Fireballs)
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.enemyGroup = pygame.sprite.RenderPlain(self.Enemies)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.ladderGroup = pygame.sprite.RenderPlain(self.Ladders)
        self.coinGroup = pygame.sprite.RenderPlain(self.Coins)
        self.allyGroup = pygame.sprite.RenderPlain(self.Allies)
        self.fireballEndpointsGroup = pygame.sprite.RenderPlain(self.FireballEndpoints)
        self.boardGroup = pygame.sprite.RenderPlain(self.Boards)
        self.heartGroup = pygame.sprite.RenderPlain(self.Hearts)

    def initializeGame(self):
        #mixer.music.stop()

        self.makeMap()
        self.makeWalls()
        self.makePrincessChamber()
        self.makeLadders()
        self.makeBrokenLadders()
        self.makeHoles()
        self.GenerateCoins()
        self.populateMap()
        self.createGroups()

