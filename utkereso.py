from tkinter import *
import numpy as np
import math
import heapq
mapW = 11
mapH = 11
endpoints = []
obstacles = []
window = Tk()
buttonMap = [[Button(window, height= 5, width=10) for column in range(mapW)] for row in range(mapH)]
map = [[0 for column in range(mapW)] for row in range(mapH)]

def rightButton_click(event):
    event.widget.config(bg ='black')
    for i in buttonMap:
        if event.widget in i: 
            obstacles.append((buttonMap.index(i),i.index(event.widget)))
            return

def addEndpoint(event):
    event.widget.config(bg ='blue')
    event.widget["state"] = DISABLED
    for i in buttonMap:
        if event.widget in i: 
            endpoints.append((buttonMap.index(i),i.index(event.widget)))
            return
    
def leftButton_click(event):
    addEndpoint(event)
    if len(endpoints) >= 2 :
        for i in obstacles:
            map[i[0]][i[1]] = 1
        path = astar(map, endpoints[0], endpoints[1])
        for i in path:
            buttonMap[i[0]][i[1]].config(bg ='red')

def heuristic(actual, end):
    return abs(actual[0] - end[0]) + abs(actual[1] - end[1])

def astar(grid, start, goal):
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
            if 0 <= neighbor_node[0] < rows and 0 <= neighbor_node[1] < cols and grid[neighbor_node[0]][neighbor_node[1]] == 0:
                buttonMap[neighbor_node[0]][neighbor_node[1]].config(bg ='orange')
                tentative_g_score = g_score[current_node] + 1
                if neighbor_node not in g_score or tentative_g_score < g_score[neighbor_node]:
                    g_score[neighbor_node] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor_node, goal)
                    heapq.heappush(open_set, (f_score, neighbor_node))
                    came_from[neighbor_node] = current_node

    return None


def generateButtons():
    for i in range(mapW):
        for j in range(mapH):
            print(j)
            buttonMap[i][j].grid(row = i, column = j)
            buttonMap[i][j].bind("<Button-3>", rightButton_click)
            buttonMap[i][j].bind("<Button-1>", leftButton_click)

generateButtons()

window.title("A*")
window.mainloop()
