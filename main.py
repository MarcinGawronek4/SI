import pygame

import constants


class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position



def map_create():
    new_map = [[ struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0,constants.MAP_WIDTH)]
    
    new_map[5][5].block_path = True
    new_map[5][7].block_path = True
    new_map[9][2].block_path = True
    new_map[8][6].block_path = True
    new_map[8][6].block_path = True
    new_map[2][8].block_path = True
    new_map[2][8].block_path = True
    new_map[7][3].block_path = True
    
    return new_map


def draw_game():
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    
    draw_map(GAME_MAP)
    
    SURFACE_MAIN.blit(constants.S_WAITER, (128, 125))
    

def draw_map(map_to_draw):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True:
                SURFACE_MAIN.blit(constants.S_TABLE, (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
            else:
                SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))

def draw_tile_rect(coords):
        x, y = coords
        
        
        
        new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
        new_surface.fill(constants.COLOR_WHITE)
        new_surface.set_alpha(150)
        SURFACE_MAIN.blit(new_surface, (x, y))
        
def astar(restaurant, start, end):

    """ Poczatkowy i koncowy wezel """
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    """ Tablice przejrzanych i nieprzejrzanych wierzcholkow """
    open_list = []
    closed_list = []

    """ Dodanie poczatkowego wierzcholka """
    open_list.append(start_node)

    """ Petla poki nie przejdzie wszystkich nieprzejrzanych wierzcholkow """
    while len(open_list) > 0:

        """ Podbranie obecnego wierzcholka """
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        """ Branie z otwartych wierzcholkow, wstawianie do zamknietych """
        open_list.pop(current_index)
        closed_list.append(current_node)

        """ Jak znajdziemy koncowy wierzcholek """
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] 
        """ Zwracamy odwrocona sciezke """

        """ Dodawanie sasiednich wiercholkow do dzieci"""
        children = []
        """Sasiednie wiercholki"""
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: 


            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])


            if node_position[0] > (len(restaurant) - 1) or node_position[0] < 0 or node_position[1] > (len(restaurant[len(restaurant)-1]) -1) or node_position[1] < 0:
                continue

            """Czy nie ma stolu po drodze"""
            if restaurant[node_position[0]][node_position[1]] != 0:
                continue

            """Nowy wierzcholek """
            new_node = Node(current_node, node_position)

            """Dodanie do dzieci"""
            children.append(new_node)

        """ Przechodzenie przez dzieci """
        for child in children:

            """ Jesli dziecko jest na liscie zamknietych przejrzacnych """
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            """ Wygenerowanie f, g, h """
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            """ Jesli dziecko jest juz na liście nieprzejrzanych"""
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            """ Dodajemy do listy nieprzejrzanych """
            open_list.append(child)
            
def find_shortest_path():
    restaurant = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    point_selected = target_select()
    list_of_tiles = astar(restaurant,(3,3),point_selected)
    print(list_of_tiles)
    
def target_select():
    menu_close = False
    CLOCK = pygame.time.Clock()
    while not menu_close:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        events_list = pygame.event.get()
        
        map_coord_x = mouse_x/64
        map_coord_y = mouse_y/64
        
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(map_coord_x, map_coord_y)
                    return(round(map_coord_x), round(map_coord_y))
                    
        draw_game()
        
        draw_tile_rect((map_coord_x,map_coord_y))
        pygame.display.flip()
        
        CLOCK.tick(60)
        
def game_main_loop():
    
    game_quit = False
    
    while not game_quit:
        
        keys_list = pygame.key.get_pressed()
        events_list = pygame.event.get()
        CLOCK = pygame.time.Clock()
        for event in events_list:
            if event.type ==pygame.QUIT:
                game_quit = True
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_p:
                    find_shortest_path()
        draw_game()
        pygame.display.flip()
        CLOCK.tick(60)
        
    pygame.quit()
    exit()

def game_initalize():
    
    global SURFACE_MAIN, GAME_MAP
    
    pygame.init()
    
    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT))
    
    GAME_MAP = map_create()
if __name__ == '__main__':
    game_initalize()
    game_main_loop()
