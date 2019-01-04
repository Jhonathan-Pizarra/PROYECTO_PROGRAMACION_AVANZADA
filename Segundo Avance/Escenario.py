import base64
import json
import gzip
import pygame
import sys
from io import StringIO
from pygame.locals import *


class Mapa(object):
    _tileH = 0
    _tileW = 0
    _MapaW = 0
    _MapaH = 0

    _transparentcolor = -1
    _matrizMapa = []
    _mapaImagenes = []

    _fondo = object

    def __init__(self):

        return


#_tileWidth = 0
#_widhtMapa = 0
#_heighMapa = 0
#_tileHeight = 0



    def cargarMapa(self,Nivel):

    #global _widhtMapa, _heighMapa, _tileWidth, _tileHeight, _matrizMapa
        f = open("C:\Users\HP\Desktop\PythonPrograms\SBimestre\Proyecto_Island3\mapas"+Nivel+".json", "r") #LOOOOL
        data = json.load(f)
        f.close()

        i=0


#Obtener Mapa
        for item in data["layers"]:
            self.layers(item)
#        mapa = item["data"]

        for item in data["tilesets"]:
            self.tilesets(item)
            i+=1

        return

    '''
      _tileWidth = data["tilewidth"] #16
      _tileHeight = data["tileheight"] #48

      _widhtMapa = data["width"]
      _heighMapa = data ["height"]

      '''

    def layers(self, layer):
        self._MapaW = layer["width"]
        self._MapaH = layer["height"]

        mapa = layer["data"]

        # Decodificaaar
        mapa = base64.decodestring(mapa)
        #    print(mapa)

        # Descompimir
        cadena = gzip.zlib.decompress(mapa);
        #    print(cadena)

        # Convertir caracteres a numeros
        salida = []
        for idx in range(0, len(cadena), 4):
            val = ord(str(cadena[idx])) | (ord(str(cadena[idx + 1])) << 8) | \
                  (ord(str(cadena[idx + 2])) << 16 | (ord(str(cadena[idx + 3])) << 24))
            salida.append(val)

#        print(salida)

        matrizTemp =[]

#        self._matrizMapa = [[0] * self._MapaH for i in range(self._MapaW)]

        #Cnvertir en matriz
#        con = 0
        for i in range(0, len(salida), self._MapaW):
            matrizTemp.append(salida[i:i+self._MapaW])

        self._matrizMapa = matrizTemp[:]
#                con = con + 1

        return


    def tilesets(self, tileset):
        self._tileW = tileset["tilewidth"]
        self._tileH = tileset["tileheight"]

        imgTemp = tileset["C:\Users\HP\Desktop\PythonPrograms\SBimestre\Proyecto_Island3\imagenes"] #LOOOOOL

        self._transparentcolor = tileset["transparentcolor"]

        img = pygame.image.load("C:\Users\HP\Desktop\PythonPrograms\SBimestre\Proyecto_Island3\imagenes" + imgTemp).convert() #LOOOOOOL

        if self._transparentcolor != -1:
            alpha = self._transparentcolor
            alpha = alpha.lstrip('#')
            lv = len(alpha)
            alpha = tuple(int(alpha[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
            img.set_colorkey(alpha, RLEACCEL)

        self.array_Tileset(img)

        return


    def array_Tileset(self, img):
        for i in range(30):
            for j in range(27):
                self._mapaImagenes.append(img.subsurface((j * 18, i * 18, self._tileW, self._tileH)))

        for i in range(len(self._mapaImagenes)):
            self._mapaImagenes[i] = pygame.transform.scale2x(self._mapaImagenes[i])

        return

'''
   print(mapa)

#Decodificaaar
#    mapa = base64.decodestring(mapa)
#    print(mapa)

#Descompimir
#    cadena = gzip.zlib.decompress(mapa);
#    print(cadena)



#Convertir caracteres a numeros
    salida = []
    for idx in range (0, len(cadena), 4):

        val = ord(str(cadena[idx])) | (ord(str(cadena[idx +1])) << 8) | \
        (ord(str(cadena[idx + 2])) << 16 | (ord(str(cadena[idx +3])) << 24))
        salida.append(val)

    print(salida)


#Convertir Matriz a vector
    for i in range(0, len(salida), _widhtMapa):
        _matrizMapa.append(salida[i:i+_widhtMapa])

    for i in range(_heighMapa):
        print(_matrizMapa[i])

    return


def array_Tileset(img):

    x = 0
    y = 0

    hojaTiles =[]

    for i in range(29): #Dimensiones de la hoja de Tiles...
        for j in range(27):
            imagen = cortar(img, (x, y, 16,26))
            hojaTiles.append(imagen)
            x +=18

        x=0
        y+=18

    return hojaTiles


def cortar(img, rectangulo):

    rect = pygame.Rect(rectangulo)
    image = pygame.Surface(rect.size).convert()
    image.blit(img, (0,0), rect)

    return image



def main():

    pygame.init()
    screen = pygame.display.set_mode((1200,750))
    pygame.display.set_caption("Adventure Island")
    clock = pygame.time.Clock()


    img = pygame.image.load("Start.PNG")
    cargarMapa("Nivel1") #Carga los Jasons

    hoja = array_Tileset(img)

    while True:
        time = clock.tick(60)

        for i in range(_heighMapa):
            for j in range(_widhtMapa):
                numTile = _matrizMapa[i][j]
                tileImg = hoja[numTile-1]
                tileImg = pygame.transform.scale(tileImg, (_tileWidth*2, _tileHeight*2))
                screen.blit(tileImg, (j*_tileWidth*2, i*_tileHeight*2+100))

        pygame.display.update()

        #Cerrar
        for eventos in pygame.event.get():  # Vamos a correr todos los eventos
            if eventos.type == QUIT:  # Si damos clcik en quitar, entonces salimos del bucle y se cierra
                sys.exit(0)

        return

'''
