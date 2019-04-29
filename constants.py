import pygame

pygame.init()

GAME_WIDTH = 640
GAME_HEIGHT = 640
CELL_WIDTH = 64
CELL_HEIGHT = 64


MAP_WIDTH = 10
MAP_HEIGHT = 10

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)

COLOR_DEFAULT_BG = COLOR_GREY

S_WAITER = pygame.image.load("C:/Users/Shaman/Desktop/WAZNE/SZI/waiter.png")
S_TABLE = pygame.image.load("C:/Users/Shaman/Desktop/WAZNE/SZI/table.png")
S_FLOOR = pygame.image.load("C:/Users/Shaman/Desktop/WAZNE/SZI/floor.png")