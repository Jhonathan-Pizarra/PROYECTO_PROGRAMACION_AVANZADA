import os
import pygame
from pygame import mixer
mixer.init()

jump_sound = pygame.mixer.Sound(os.path.join('Assets/jump.wav'))
coin_sound = pygame.mixer.Sound(os.path.join("Assets/coin.wav"))
death_sound = pygame.mixer.Sound(os.path.join('Assets/death.wav'))
pygame.mixer.music.load(os.path.join('Assets/AdventureMP4.ogv'))
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play()
