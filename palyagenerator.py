import pygame
from copy import deepcopy  # Changed from copy to deepcopy
import random
import numpy as np
import heapq
import math

class Constants:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 900
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (175, 65, 84)
    BLUE = (50, 50, 255)
    RES = 10
    FULL_RES = 60
    DIMS = 25, 15
    COMP_SIZE = 6

grid = []
screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
metadata =[]
rotation_info= [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1, 1]
graph = []

def rotate_fragment(matrix, times):
    if not matrix:
        return []
    rows = len(matrix)
    cols = len(matrix[0])
    rotations = times % 4
    if rotations == 0:
        return matrix
    rotated_matrix = [[0] * rows for _ in range(cols)]
    for _ in range(rotations):
        for i in range(rows):
            for j in range(cols):
                rotated_matrix[j][rows - 1 - i] = matrix[i][j]
        rows, cols = cols, rows
        matrix = [row[:] for row in rotated_matrix]
    return rotated_matrix

def match_socket(socket, targetsocket):
    return socket == targetsocket

class Tile:
    def __init__(self, c, r):
        self.c = c
        self.r = r
        self.x = self.c * Constants.FULL_RES
        self.y = self.r * Constants.FULL_RES
        self.matrix = deepcopy(metadata[-1]["matrix"])  # Deepcopy metadata
        self.entropy = sum(rotation_info) + len(rotation_info)
        self.potentialTiles = deepcopy(metadata)  # Deepcopy metadata
        self.collapsed = False
        self.sockets = [-1 for _ in range(4)]
        self.right_n = {"collapsed" : None, "socket": False}
        self.left_n = {"collapsed" : None, "socket": False}
        self.up_n = {"collapsed" : None, "socket": False}
        self.down_n = {"collapsed" : None, "socket": False}
        self.directions = []
        self.index = (c,r)
        
    def draw(self):
        for j in range(len(self.matrix)):
            for i in range(len(self.matrix[j])):
                if self.matrix[j][i] == 1:
                    pygame.draw.rect(screen, Constants.RED, pygame.Rect(self.x + i * Constants.RES, self.y + j * Constants.RES, Constants.RES,Constants.RES)) 
                elif self.matrix[j][i] == 0:
                    pygame.draw.rect(screen, Constants.WHITE, pygame.Rect(self.x + i * Constants.RES, self.y + j * Constants.RES, Constants.RES,Constants.RES)) 
                elif self.matrix[j][i] == 2:
                    pygame.draw.rect(screen, Constants.BLUE, pygame.Rect(self.x + i * Constants.RES, self.y + j * Constants.RES, Constants.RES,Constants.RES)) 
                elif self.matrix[j][i] == 4:
                    pygame.draw.rect(screen, Constants.BLACK, pygame.Rect(self.x + i * Constants.RES, self.y + j * Constants.RES, Constants.RES,Constants.RES)) 
        #pygame.draw.rect(screen, Constants.BLACK, pygame.Rect(self.x, self.y , Constants.FULL_RES,Constants.FULL_RES),1) 
    
    def updateEntropy(self, lowestEntropy):
        placeHolderTileSet = []
        for potTile in self.potentialTiles:
            validTiles = True
            if self.right_n["collapsed"] and not match_socket(potTile["sockets"][2], self.right_n["socket"]):
                validTiles = False
            if self.down_n["collapsed"] and not match_socket(potTile["sockets"][3], self.down_n["socket"]):
                validTiles = False
            if self.left_n["collapsed"] and not match_socket(potTile["sockets"][0], self.left_n["socket"]):
                validTiles = False
            if self.up_n["collapsed"] and not match_socket(potTile["sockets"][1], self.up_n["socket"]):
                validTiles = False
            if validTiles:
                placeHolderTileSet.append(potTile) 
        self.potentialTiles = placeHolderTileSet
        seenTile = []
        for tile in self.potentialTiles:
            if tile["ID"] not in seenTile:
                seenTile.append(tile["ID"])
        self.entropy = len(seenTile)
        if lowestEntropy == None or self.entropy < lowestEntropy:
            return self.entropy
        return lowestEntropy
    
    def updateNeighbors(self):
        if not self.collapsed:
            if self.c < Constants.DIMS[0]-1:
                self.right_n = {"collapsed":grid[self.r][self.c+1].collapsed, "socket":grid[self.r][self.c+1].sockets[0]}
            if self.r < Constants.DIMS[1]-1:
                self.down_n = {"collapsed":grid[self.r+1][self.c].collapsed, "socket":grid[self.r+1][self.c].sockets[1]}
            if self.c > 0:
                self.left_n = {"collapsed":grid[self.r][self.c-1].collapsed, "socket":grid[self.r][self.c-1].sockets[2]}
            if self.r > 0:
                self.up_n = {"collapsed":grid[self.r-1][self.c].collapsed, "socket":grid[self.r-1][self.c].sockets[3]}
    
    def getID(self, matrix):
        for i in self.potentialTiles:
            if np.array_equal(i["matrix"], matrix): return i["ID"]
    def collapse(self):
        self.collapsed = True
        if len(self.potentialTiles) > 0:
            potTile = random.choice(self.potentialTiles)
        else:
            potTile = deepcopy(metadata[-1])  # Deepcopy metadata
        self.id = potTile["ID"]
        self.matrix = deepcopy(potTile["matrix"])  # Deepcopy matrix
        self.sockets = deepcopy(potTile["sockets"])  # Deepcopy sockets
        self.entropy = 0
    
    def collapse_from_data(self, matrix):
        self.collapsed = True
        self.id = self.getID(matrix)
        self.matrix = deepcopy(matrix)  # Deepcopy matrix
        print(matrix)
        self.sockets = [[k[0] for k in matrix], [k for k in matrix[0]], [k[-1] for k in matrix], [k for k in matrix[-1]]]
        self.entropy = 0
# Initialize Pygame

def draw():
    screen.fill(Constants.WHITE)
    for row in grid:
        for tile in row:
            tile.draw()
    pygame.display.flip()
def update():
    lowest_entropy = None
    for row in grid:
        for tile in row:
            if not tile.collapsed:
                tile.updateNeighbors()
                lowest_entropy = tile.updateEntropy(lowest_entropy)
    candidates = []
    for row in grid:
        for tile in row:
            if not tile.collapsed and tile.entropy == lowest_entropy:
                candidates.append(tile)
    if len(candidates) > 0:
        candidates[0].collapse()    
def generateMap(scrn):
    screen = scrn
    collapsed = 0
    map_fragments =  [
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]], #Teljes méretű akadály
        [[2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2]], #Egyenes szakasz
        [[2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2]], 
        [[2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2]],
        [[2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2]], #Kereszteződés
        [[2, 2, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2]],
        [[2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2]],
        
        [[2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2]],
        [[2, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2]],
        [[2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 0, 0, 2, 2, 2]],
        
        [[2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2]],
        [[2, 2, 2, 0, 0, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2]],
        [[2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 2]],
        #T elágazó
        # 1 felül
        [[2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2]],
        #2 felül
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2]],
        #3 felül
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 0, 0, 2, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 2, 2, 0, 0, 2]],
        
        #Derékszögű kanyar
        # 1 felül
        [[2, 2, 2, 2, 2, 2], [2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 0, 0, 0], [2, 2, 2, 0, 0, 0], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2]],
        #2 felül
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [2, 0, 0, 2, 2, 2], [2, 0, 0, 2, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2], [2, 2, 0, 0, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 0, 0, 0], [2, 2, 2, 0, 0, 0], [2, 2, 2, 0, 0, 2], [2, 2, 2, 0, 0, 2]],
        #3 felül
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0], [2, 0, 0, 2, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 0, 0, 0, 0], [2, 2, 0, 0, 0, 0], [2, 2, 0, 0, 2, 2]],
        [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 0, 0, 0], [2, 2, 2, 0, 0, 0], [2, 2, 2, 0, 0, 2]],
        [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], #Tér
        [[2, 0, 0, 2, 2, 2], [2, 0, 0, 0, 2, 2], [2, 0, 0, 0, 2, 2], [2, 2, 0, 0, 0, 2], [2, 2, 0, 0, 0, 2], [2, 2, 2, 0, 0, 2]], #Átlós kanyar
        [[2, 2, 2, 0, 0, 2], [2, 2, 0, 0, 0, 2], [2, 2, 0, 0, 0, 2], [2, 0, 0, 0, 2, 2], [2, 0, 0, 0, 2, 2], [2, 0, 0, 2, 2, 2]],
        ] 
    # 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1, 1
    for i in range(len(map_fragments)):
        for j in range(rotation_info[i]+1):
            r = rotate_fragment(map_fragments[i], j)
            rotated_collection = [[k[0] for k in r], [k for k in r[0]], [k[-1] for k in r], [k for k in r[-1]]]
            metadata.append({"ID": deepcopy(i), "matrix": deepcopy(r), "sockets": deepcopy(rotated_collection), "rotation": j})
    for r in range(Constants.DIMS[1]):
        row = [] 
        for c in range(Constants.DIMS[0]):
            tile = Tile(c,r)
            row.append(tile)
        grid.append(row)
    grid[0][0].collapse()
    collapsed = 1
    while collapsed < Constants.DIMS[0] * Constants.DIMS[1]:
        update()
        collapsed += 1

def grid_map_gen():
    rows = []
    for i in grid:
        rows.append(np.hstack([k.matrix for k in i]))
    return np.vstack(rows)

def generate_from_input(matrix):
    submatrices = [matrix[i*Constants.COMP_SIZE:(i+1)*Constants.COMP_SIZE, j*Constants.COMP_SIZE:(j+1)*Constants.COMP_SIZE] for i in range(matrix.shape[0] // Constants.COMP_SIZE) for j in range(matrix.shape[1] // Constants.COMP_SIZE)]
    for i in range(len(submatrices)): grid.append(Tile(i % Constants.COMP_SIZE,i // Constants.COMP_SIZE).collapse_from_data(submatrices[i])) 

def build_graph():
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if j < len(grid[i])-1 and 0 in grid[i][j].sockets[2]:
                grid[i][j].directions.append((0, 1))
            if i < len(grid)-1 and 0 in grid[i][j].sockets[3]:
                grid[i][j].directions.append((1, 0))
            if j > 0 and 0 in grid[i][j].sockets[0]:
                grid[i][j].directions.append((0, -1))
            if j > 0 and 0 in grid[i][j].sockets[1]:
                grid[i][j].directions.append((-1, 0))

