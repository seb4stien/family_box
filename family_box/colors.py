#!/usr/bin/python2

import time
import pygame
from random import randrange

import sys, signal

print("Init")
pygame.display.init()

print("Size")
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print(size)

print("Screen")
screen = pygame.display.set_mode((640, 480))
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
exit(0)
print("Mouse")
pygame.mouse.set_visible(False)

while True:
  print("Fill")
  screen.fill((randrange(255),randrange(255),randrange(233)))
  print("Update")
  pygame.display.update()
  print("Sleep")
  time.sleep(5)
