from worldmap import WorldMap
from pathfind import PathFind
import tkinter as tk
import time

map_size = 10

start_pos = [9, 9]
goal_pos = [4, 3]
obstacles1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             [1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
             [1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
             [1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
             [1, 0, 1, 1, 0, 1, 0, 0, 1, 0],
             [0, 0, 1, 0, 0, 1, 1, 0, 1, 0],
             [0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

obstacles = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
             [1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
             [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
             [1, 0, 1, 1, 0, 1, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
             [0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

def mouse_callback(start_pos, goal_pos, is_a_star):
    if not is_a_star:
        print("- Pathinder normal")
        start_time = time.perf_counter()
        path, closed = finder.normal_search(start_pos, goal_pos, obstacles)
        end_time = time.perf_counter()-start_time
    else:
        print("- A* pathinder")
        start_time = time.perf_counter()
        path, closed = finder.a_star_search(start_pos, goal_pos, obstacles)
        end_time = time.perf_counter()-start_time
    
    print("Custo total: %d"%path[-1][2])
    print("Nós acessados: %d"%len(closed))
    print("Tempo gasto: %.3fms\n"%(end_time*1000.0))
    
    return path, closed

print(" -----------------------------------------------\n\
Comandos:\n\
\t'h' para visualizar o histórico de nós visitados\n \
\t'p' para trocar o algoritmo de busca\n\
\t'g' para ativar a grade\n\
 -----------------------------------------------")

finder = PathFind()
map = WorldMap(start_pos, goal_pos, obstacles, map_size)
map.path_find_callback = mouse_callback
map.loop()
