import time
from random import random
import algorithmgenetic
import pygame
import D_tree_bill
import banana
import constants
from Table import Table
import Waiter

waiter = None

objectslist = []

rng_object = random()

estimator = D_tree_bill.BuildTree()
class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path


def map_create_hardcore():
    new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]
    map = constants.REST
    for y in range(0, 10):
        for x in range(0, 10):
            if map[x][y] == 1:
                new_map[y][x].block_path = True
    return new_map


def add_objects_to_game():
    global objectslist
    map = constants.REST
    for y in range(0, 10):
        for x in range(0, 10):
            if map[y][x] == 1:
                objectslist.append(Table(x, y))
    map = constants.BANANA
    for y in range(0, 10):
        for x in range(0, 10):
            if map[y][x] == 1:
                objectslist.append(banana.Banana(x, y))
    global waiter
    waiter = Waiter.Waiter(1, 1, 0, objectslist)
    objectslist.append(waiter)


def draw_game():
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    draw_floor()
    # draw_map(GAME_MAP)
    for entity in objectslist:
        draw_entity(entity)


def draw_entity(entity):
    if entity.drawable:
        angle = 90 * abs(entity.w - 4)
        entityimg = pygame.transform.rotate(entity.image, angle)
        SURFACE_MAIN.blit(entityimg, (entity.x * constants.CELL_WIDTH, entity.y * constants.CELL_HEIGHT))


def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path:
                SURFACE_MAIN.blit(constants.S_TABLE, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
            else:
                SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def draw_floor():
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def draw_tile_rect(coords):
    x, y = coords

    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
    new_surface.fill(constants.COLOR_WHITE)
    new_surface.set_alpha(150)
    SURFACE_MAIN.blit(new_surface, (x, y))


def target_select():
    menu_close = False
    CLOCK = pygame.time.Clock()
    while not menu_close:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        events_list = pygame.event.get()

        map_coord_x = mouse_x / 64
        map_coord_y = mouse_y / 64

        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(map_coord_x, map_coord_y)
                    return (round(map_coord_x), round(map_coord_y))


def proc_tick():
    for entity in objectslist:
        action = getattr(entity, "do", None)
        if not (action is None):
            action()


def get_elements(x, y):
    return [objects for objects in objectslist if objects.x == x and objects.y == y]


def find_path_new():
    mouse_x, mouse_y = pygame.mouse.get_pos()

    x = int(mouse_x / constants.CELL_WIDTH)
    y = int(mouse_y / constants.CELL_HEIGHT)
    print(x+1, " ", y)
    waiter.go_to(x, y-1, 0)



def game_main_loop():
    game_quit = False

    while not game_quit:

        keys_list = pygame.key.get_pressed()
        events_list = pygame.event.get()
        CLOCK = pygame.time.Clock()
        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if(D_tree_bill.PredictBill(estimator)==1):
                        find_path_new()
                        print ("wydano rachunek")
                        waiter.addorder("go_to2")
                        waiter.addorder(1)
                        waiter.addorder(1)
                        waiter.addorder(2)
                        waiter.addorder("generate_random_payment")
#                         waiter.from_to()
                        
                    
        proc_tick()
        draw_game()
        pygame.display.flip()
        CLOCK.tick(2)

    pygame.quit()
    exit()


def game_initialize():
    global SURFACE_MAIN, GAME_MAP

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))

    GAME_MAP = map_create_hardcore()


if __name__ == '__main__':
    game_initialize()
    add_objects_to_game()
    game_main_loop()
