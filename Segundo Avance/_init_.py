# Módulos
import sys
import os
import time
import pygame
from pygame.locals import * #Va a importar clases predefinidas que ya existen
from tkinter import FALSE
import SBimestre.Proyecto_Island3.Escenario

# Constantes de ventana
WIDTH = 900 #Ancho
HEIGHT = 500 #Alto
#HposX = 50
#HposY = 290

#Para los sprites
#contador = 0
#direccion = True
#i=0
#xInicio_xFinal = {} #Inicial y final
#RxInicio_xFinal = {}

#Para el salto
#parabola = {}
#salto = False
#bajar = False
#salto_Parabolico = False


def main():

    Initialize()
    LoadContent()
    global time



    while True: #Este bucle impide que se cierre de inmediato al ejecutarse

        time = clock.tick(60)
        Updates()
        Draw()


    return 0

'''

def imagen(filename, transparente=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error():


        if transparente:
            color = image.get_at((0,0))
            image.set_colorkey(color)

    return image

'''
#TECLADO

'''
def teclado():

    global HposX #La posicion en X de Higgins, el muñeco
    global contador
    global direccion
    global salto


    teclado = pygame.key.get_pressed()

    if teclado[K_z]:
        salto = True

    if teclado[K_RIGHT]:
        HposX +=2
        contador +=1
        direccion = True

    elif teclado[K_LEFT]:
        HposX -=2
        contador +=1
        direccion = False

    else:
        contador = 3

    #Cerrar ventana
    for eventos in pygame.event.get():  # Vamos a correr todos los eventos
        if eventos.type == QUIT:  # Si damos clcik en quitar, entonces salimos del bucle y se cierra
            sys.exit(0)

    return
'''
#Control teclado
'''
    if teclado[K_z] and teclado[K_RIGHT] and salto_Parabolico == False:
        salto_Parabolico = True
    

    elif teclado[K_z] and teclado[K_LEFT] and salto_Parabolico == False:
        salto_Parabolico = True

    elif teclado[K_RIGHT] and salto == False and salto_Parabolico == False:
        HposX += 2
        contador += 1
        direccion = True

    elif teclado[K_LEFT] and salto == False and salto_Parabolico == False:
        HposX -= 2
        contador += 1
        direccion = False

    elif teclado[K_z] and salto == False and salto_Parabolico == False:
        salto = True

    else:
        contador = 3

    return
'''

#Sprites
'''
def sprite_Higgins():

    global contador
    p = 3
    global i

    if(contador == p):
        i=0
    if (contador == p*2):
        i = 1
    if (contador == p*3):
        i = 2
        contador = 0


    return
'''


def Initialize():

    global screen
    global nivel
    global clock
#    global xInicio_xFinal
#    global RxInicio_xFinal
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Adventure Island")
    clock = pygame.time.Clock()

    return screen

'''
    xInicio_xFinal = {}
    RxInicio_xFinal = {}

    xInicio_xFinal[0] = (400, 81, 81, 81)
    xInicio_xFinal[1] = (500, 81, 81, 81)
    xInicio_xFinal[2] = (600, 81, 81, 81)
    xInicio_xFinal[3] = (700, 81, 81, 81)  # Para el salto

    RxInicio_xFinal[0] = (300, 81, 81, 81)
    RxInicio_xFinal[1] = (200, 81, 81, 81)
    RxInicio_xFinal[2] = (100, 81, 81, 81)
    RxInicio_xFinal[3] = (0, 81, 81, 81)
'''



def LoadContent():

    global fondo
    global higgins
#    global higgins_inverso
    global nivel

#    higgins = Personajes.Higgins()


    nivel = Escenario.Mapa()
    nivel.cargarMapa("Nivel1")

    fondo = imagen("Fondo.png")
    #higgins = imagen("Sprites.png", True)
    #higgins_inverso = pygame.transform.flip(higgins, True, False)

    #fondo = pygame.transform.scale(fondo, (1000, 400))

    return

def Updates():

    global higgins

    #Util.teclado()
    #Escena
    #sprite_Higgins()
    #Enemigo()
    #Colisiones()

    return

def Draw():
    #global salto
    #global salto_Parabolico
    #global bajar_Parabolico
    #global bajar

    global time

    screen.blit(fondo, (0, 0))

    for i in range(nivel._MapaH):
        for j in range(nivel._MapaW):
            pos = nivel._matrizMapa[i][j]
            screen.blit(nivel._mapaImagenes[pos - 1], (j * 32, i * 32))

    pygame.display.flip()
    return

#    global HposX
#    global HposY

    #Direcciones
#    if (direccion == True and salto == False):
#        screen.blit(higgins, (HposX, HposY), (xInicio_xFinal[i]))

#    if (direccion == False and salto == False):
#        screen.blit(higgins_inverso, (HposX, HposY),(RxInicio_xFinal[i]))  # Le pasa por parametro la posicion donde se va a dibujar en X y en Y

    #Salto:

'''
    if salto == True:

        if direccion == True:
            screen.blit(higgins, (HposX, HposY), (xInicio_xFinal[3]))

        if direccion == False:
            screen.blit(higgins_inverso, (HposX, HposY), (RxInicio_xFinal[3]))

        if bajar == False:
            HposY -= 4

        if bajar == True:
            HposY += 4

        if HposY <= 186: #Hasta aqui llega el salto
            bajar = True

        if HposY >= 290: #Hasta aqui se detiene el salto
            bajar = False
            salto = False

'''


'''
    #Salto Parabolico
        if salto_Parabolico == True and direccion == True:

            screen.blit(higgins, (HposX, HposY), (xInicio_xFinal[3]))

            if bajar_Parabolico == False:
                HposY -= 3
                HposX += 2

            if bajar_Parabolico == True:
                HposY += 3
                HposX += 2

            if HposY == 140: #Si llega hasta una altura de
                bajar_Parabolico = True

            if HposY == 290: #Si toca el piso
                bajar_Parabolico = False
                salto_Parabolico = False

        elif salto_Parabolico == True and direccion == False:

            screen.blit(higgins_inverso, (HposX, HposY), (RxInicio_xFinal[3]))

            if bajar_Parabolico == False:
                HposY -= 3
                HposX -= 2

            if bajar_Parabolico == True:
                HposY += 3
                HposX -= 2

            if HposY == 140:
                bajar_Parabolico = True

            if HposY == 290:
                bajar_Parabolico = False
                salto_Parabolico = False
'''


if __name__ == '__main__':

    main()