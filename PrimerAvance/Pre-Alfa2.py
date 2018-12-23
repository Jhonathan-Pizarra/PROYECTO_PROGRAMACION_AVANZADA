# -*- coding: utf-8 -*-

#main
import pygame
import PreAlfa
import sys


#Vamo a poner las imagenes de fondo:
def imagen(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error():
        raise SystemExit()

    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color)
    return image



pygame.init()

# Definimos algunas variables que usaremos en nuestro código

ancho_ventana = 640
alto_ventana = 480
screen = pygame.display.set_mode((ancho_ventana, alto_ventana)) #Le estamos diciendo de qué tamaño queremos nuestra ventana
pygame.display.set_caption("Juego de Adventure Island") #Es un nombre a nuestro jeugo..
clock = pygame.time.Clock()
PreAlfa = PreAlfa.Kate((ancho_ventana/2, alto_ventana/2))
game_over = False
#Musica de fondo:
pygame.mixer_music.load("AdventureMusic.mp3")
pygame.mixer_music.play(2) #Loop o iteracion para cuantas veces tiene que reporoducirse el juego
#Imagen Fondo:
fondo = imagen("Fondo.png")
fondo = pygame.transform.scale(fondo,(640,480))



while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            pygame.mixer_music.stop() #Aqui se dentendría la musica, porque perdió

    PreAlfa.handle_event(event)
    #screen.fill(pygame.Color('gray'))
    screen.blit(fondo, (0,0))
    screen.blit(PreAlfa.image, PreAlfa.rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit ()
