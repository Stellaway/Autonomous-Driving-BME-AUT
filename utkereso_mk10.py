import pygame
import sys
import math
import heapq
import numpy as np
import palyagenerator as pg

class PathFinder:
    def heuristic(self, actual, end):
        return math.sqrt(pow(actual[0]-end[0],2) + pow(actual[1]-end[1],2))

    def astar(self, grid, start, goal):
        rows, cols = len(grid), len(grid[0])
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}

        while open_set:
            current_node = heapq.heappop(open_set)[1]
            if current_node == goal:
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                path.append(start)
                return path[::-1]

            for neighbor in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                neighbor_node = (current_node[0] + neighbor[0], current_node[1] + neighbor[1])
                if 0 <= neighbor_node[0] < rows and 0 <= neighbor_node[1] < cols and grid[neighbor_node[0]][neighbor_node[1]] != 2:
                    grid[neighbor_node[0]][neighbor_node[1]] = 3
                    tentative_g_score = g_score[current_node] + 1
                    if neighbor_node not in g_score or tentative_g_score < g_score[neighbor_node]:
                        g_score[neighbor_node] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor_node, goal)
                        heapq.heappush(open_set, (f_score, neighbor_node))
                        came_from[neighbor_node] = current_node

        return None

class PathSpline:
    control_points = []
    spline_points = []
    def convert_to_main_coordinate(self, value,cell_height):
        return (value[1]*cell_height+0.5*cell_height+gui.textbox_margin,value[0]*cell_height+0.5*cell_height+gui.textbox_margin*2)

    def distance(self, p1, p2):
        return math.sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))
    def control_point_smoothing(self, path, cell_height):
        for i in range(0,len(path)-2):
            if self.convert_to_main_coordinate(path[i], cell_height) in self.control_points:
                control_index = self.control_points.index(self.convert_to_main_coordinate(path[i], cell_height))
                if self.convert_to_main_coordinate(path[i+1], cell_height) in self.control_points and self.convert_to_main_coordinate(path[i+2], cell_height):
                    j = i+1
                    while self.convert_to_main_coordinate(path[j], cell_height) in self.control_points and j < len(path)-1:
                        self.control_points.remove(self.convert_to_main_coordinate(path[j], cell_height))
                        j+=1
                    if j <len(path)-2:
                        self.control_points.insert(control_index+1, self.convert_to_main_coordinate(path[j], cell_height))
                elif self.convert_to_main_coordinate(path[i+1], cell_height) in self.control_points:
                    self.control_points.remove(self.convert_to_main_coordinate(path[j], cell_height))
                    self.control_points.insert(control_index+1, self.convert_to_main_coordinate(path[i+2], cell_height))
        self.controlSpline()
    
    def controlSpline(self):
        i = 1
        while i < len(self.control_points):
            if self.distance(self.control_points[i], self.control_points[i-1]) > 110:
                self.control_points.insert(i, ((self.control_points[i-1][0] + self.control_points[i][0])/2,(self.control_points[i-1][1] + self.control_points[i][1])/2))
                i-= 1
            i += 1
    def create_catmull_rom_spline(self):
        self.control_points = [self.control_points[0]] + self.control_points + [self.control_points[-1]]
        for i in range(1, len(self.control_points) - 2):
            for t in np.linspace(0, 1, 100):
                self.spline_point = self.catmull_rom_spline(self.control_points[i - 1], self.control_points[i], self.control_points[i + 1],  self.control_points[i + 2], t)
                self.spline_points.append(self.spline_point)
        self.spline_points = np.array(self.spline_points)

    def drawSpline(self):
        for point in self.spline_points:
            pygame.draw.circle(gui.screen, Constants.WHITE, (int(point[0]), int(point[1])), 2)
        for point in self.control_points:
            pygame.draw.circle(gui.screen, Constants.SECONDARY_BLUE, point, 5)

    # Catmull-Rom spline interpolation function
    def catmull_rom_spline(self, p0, p1, p2, p3, t):
        t2 = t * t
        t3 = t2 * t
        return 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3), 0.5 * ((2 * p1[1]) +(-p0[1] + p2[1]) * t +(2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +(-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
    
    def setupSpline(self):
        path = pf.astar(gui.grid_map, gui.endpoints[0], gui.endpoints[1])
        direction = (path[1][0]-path[0][0], path[1][1]-path[0][1])
        newDirection = direction
        actual = path[0] 
        self.control_points.append(self.convert_to_main_coordinate(actual, gui.cell_height))
        for i in range(0,len(path)):
            gui.grid_map[path[i][0]][path[i][1]] = 4
            if i != 0: 
                newDirection = (path[i][0]-path[i-1][0], path[i][1]-path[i-1][1])
            if(direction != newDirection):
                direction = newDirection
                self.control_points.append(self.convert_to_main_coordinate(actual, gui.cell_height))
            actual = path[i]
        self.control_points.append(self.convert_to_main_coordinate(path[-1], gui.cell_height))
        self.control_point_smoothing(path, gui.cell_height)
        self.create_catmull_rom_spline()

class Constants:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 900
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (150, 150, 150)
    PRIMARY_BLUE = (50, 50, 255)
    SECONDARY_BLUE = (70, 70, 255)
    ORANGE = (242, 121, 53)
    RED = (175, 65, 84)
    GREEN = (0, 66, 37)
    FONT_SIZE = 36
    TEXT_COLOR = (0, 0, 0)
    CURSOR_COLOR = (0, 0, 0)
# Initialize Pygame
pygame.init()
pygame.display.set_caption("GUMIGYÁR")

class GUI:
    textbox_width = 150
    textbox_height = 40
    textbox_margin = 5
    textbox_rect1 = pygame.Rect((Constants.SCREEN_WIDTH - 3 * textbox_width - 2 * textbox_margin) // 2, Constants.SCREEN_HEIGHT - textbox_height - textbox_margin, textbox_width, textbox_height)
    textbox_rect2 = pygame.Rect(textbox_rect1.right + textbox_margin, Constants.SCREEN_HEIGHT - textbox_height - textbox_margin, textbox_width, textbox_height)
    button_rect = pygame.Rect(textbox_rect2.right + textbox_margin, Constants.SCREEN_HEIGHT - textbox_height - textbox_margin, textbox_width, textbox_height)
    input_text1 = ""
    input_text2 = ""
    cursor_blink_timer = 0
    cursor_visible = True
    active_textbox = 1
    cell_height = pg.Constants.RES
    font = pygame.font.Font(None, Constants.FONT_SIZE)
    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    drawing_spline = False
    number1 = pg.Constants.DIMS[1]*pg.Constants.COMP_SIZE
    number2 = pg.Constants.DIMS[0]*pg.Constants.COMP_SIZE
    grid_map = None
    endpoints = []
    def drawComponents(self):
        self.drawGrid()

    def drawGrid(self):
        for i in range(self.number1):
            for j in range(self.number2):
                cell_rect = pygame.Rect(j * self.cell_height + self.textbox_margin, i * self.cell_height + 2 * self.textbox_margin, self.cell_height, self.cell_height)
                if self.grid_map[i][j] == 1:
                    pygame.draw.rect(self.screen, Constants.PRIMARY_BLUE, cell_rect)
                elif self.grid_map[i][j] == 2:
                    pygame.draw.rect(self.screen, Constants.SECONDARY_BLUE, cell_rect)
                elif self.grid_map[i][j] == 3:
                    pygame.draw.rect(self.screen, Constants.ORANGE, cell_rect)
                elif self.grid_map[i][j] == 4:
                    pygame.draw.rect(self.screen, Constants.RED, cell_rect)
    
    def setupGrid(self):      
        pg.generateMap(self.screen)
        self.grid_map = pg.grid_map_gen()
        print(self.grid_map)
    def is_numeric(self,text):
        try:
            int(text)
            return True
        except ValueError:
            return False

    def okButtonPress(self):
        return self.setupGrid()
    
    def handleKeyDown(self):
        if event.key == pygame.K_TAB:
                    self.active_textbox = 3 - self.active_textbox
        elif event.key == pygame.K_RETURN:
            return self.setupGrid()
        elif event.key == pygame.K_BACKSPACE:
            if self.active_textbox == 1:
                self.input_text1 = self.input_text1[:-1]
            elif self.active_textbox == 2:
                self.input_text2 = self.input_text2[:-1]
        elif event.unicode.isnumeric():
            if self.active_textbox == 1:
                self.input_text1 += event.unicode
            elif self.active_textbox == 2:
                self.input_text2 += event.unicode
        return False
    
    def handleClick(self):
        for i in range(self.number1):
            for j in range(self.number2):
                cell_rect = pygame.Rect(j * self.cell_height + self.textbox_margin, i * self.cell_height + 2 * self.textbox_margin, self.cell_height, self.cell_height)
                if cell_rect.collidepoint(event.pos):
                    if event.button == 1:
                        self.grid_map[i][j] = 2
                        return False
                    elif event.button == 3:
                        self.endpoints.append((i,j))
                        self.grid_map[i][j] = 1 
                        return True
        return False

class Vehicle:
    move_interval = 1 
    model = None
    position = 0
    angle = 0
    width = 0.5
    def blitRotate(self,surf, image, pos, originPos, angle):
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        surf.blit(rotated_image, rotated_image_rect)
        
    def drawVehicle(self):
        if len(spline.spline_points)-1 <= self.position:
            self.position = 0
        if pygame.time.get_ticks() % self.move_interval == 0:
            vector = (spline.spline_points[self.position][0] - spline.spline_points[self.position+1][0], spline.spline_points[self.position][1] - spline.spline_points[self.position+1][1])
            self.blitRotate(gui.screen, self.model, (spline.spline_points[self.position][0], spline.spline_points[self.position][1]), (self.model.get_width()/2, self.model.get_height()/2), -math.degrees(math.atan2(vector[1], vector[0])))
            gui.screen.blit(self.model, (1, 1))
            self.position += 1
            pygame.draw.rect(self.model, (0, 233, 0), (1, 1, self.model.get_width(), self.model.get_height())) 

# Main loop
running = True
clock = pygame.time.Clock()
step = 1
spline = PathSpline()
pf = PathFinder()
gui = GUI()
vehicle = Vehicle()
gui.setupGrid()
while running:
    gui.screen.fill(Constants.WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if step == 1 or step == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                vehicle.model = pygame.Surface((gui.cell_height, gui.cell_height/2), pygame.SRCALPHA)
                if gui.handleClick():
                    step+=1
                if step == 3: 
                    spline.setupSpline()
    gui.drawComponents()
    if step == 3: 
        spline.drawSpline()
        vehicle.drawVehicle()
    pygame.display.flip()
    clock.tick(120)
    
pygame.quit()
sys.exit()
