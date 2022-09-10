import tkinter as tk
import os, sys

'''
    Função para importar arquivos (imagens) do diretório temporario
    (serve para quando o .exe do programa é criado)
'''
def resource_path(relative_path):
    try:
        # O PyInstaller cria uma pasta chamada _MEIPASS no temp
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Classe da janela principal
class WorldMap():
    def __init__(self, start_pos, goal_pos, obstacle_map, map_size = 10, square_size = 50,):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.obstacle_map = obstacle_map
        self.map_size = map_size
        self.square_size = square_size
        self.path_find_callback = lambda a,b,c: ([], []) # Função para ser chamada quando um botão for clicado
        self.draw_history = False # Comuta entre desenhar o caminho e o histórico
        self.select_a_star = False # Comuta entre usar o path finding normal e o a*
        self.show_grid = False # Comuta entre desenhar ou não o grid
        

        # Cria a janela e configura
        self.win = tk.Tk()
        self.win.title("Pathfinding em um mundo 2D")
        self.win.geometry("+{}+{}".format(430, 100))
        self.win.resizable(False, False)
        self.win.iconbitmap(resource_path('Imagens/map.ico'))

        canvas_size = self.map_size*self.square_size + 2
        self.canvas = tk.Canvas(self.win, width=canvas_size,
                                height=canvas_size)
        self.canvas.pack()

        self.canvas.focus_set()
        self.canvas.bind("<Button-1>", self.mouse1_callback)
        self.canvas.bind("<Button-3>", self.mouse3_callback)

        self.canvas.bind('h', self.h_key_callback)
        self.canvas.bind('p', self.p_key_callback)
        self.canvas.bind('g', self.g_key_callback)

        self.draw_canvas()

    '''
        Retorna uma posição (x/y) a partir de um índice
    '''
    def idx_to_pos(self, index):
        # Soma 2 pra desenhar a borda dos quadrados da primeira coluna
        return 2 + index*self.square_size

    '''
        Retorna um índice a partir de um posição (x/y)
    '''
    def pos_to_idx(self, pos):
        return (pos-2)//self.square_size

    '''
        Desenha o mapa
    '''
    def draw_canvas(self):
        # Limpa antes de desenhar
        self.canvas.delete("all")

        # Percorre todos os pontos do mapa
        for i in range(self.map_size):
            y = self.idx_to_pos(i)
            for j in range(self.map_size):
                x = self.idx_to_pos(j)

                # Desenha o robo
                if (self.start_pos[0] == i and self.start_pos[1] == j):
                    sx = x + self.square_size//2
                    sy = y + self.square_size//2
                    self.canvas.create_oval(sx - 15, sy - 15, sx + 15, sy + 15, fill="#3498db")

                # Desenha o objetivo
                if (self.goal_pos[0] == i and self.goal_pos[1] == j):
                    sx = x + self.square_size//2
                    sy = y + self.square_size//2
                    self.canvas.create_polygon(sx - 15, sy, sx, sy + 15, sx + 15, sy, sx, sy - 15, fill="#f1c40f")

                fill = "Black" if self.obstacle_map[i][j] == 1 else ""

                if(fill == "Black" or self.show_grid):
                    self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size, fill=fill)

    '''
        Desenha um caminho obtido pelo Path Find
    '''
    def draw_path(self):
        path, closed = self.path_find_callback(self.start_pos, self.goal_pos, self.select_a_star)

        if not path:
            return
        
        self.draw_canvas()

        if self.draw_history:
            self.draw_visited_nodes(closed)
            return
            
        for i in range(len(path)-1):
            x1 = self.idx_to_pos(path[i][1]) + self.square_size//2
            y1 = self.idx_to_pos(path[i][0]) + self.square_size//2
            x2 = self.idx_to_pos(path[i+1][1]) + self.square_size//2
            y2 = self.idx_to_pos(path[i+1][0]) + self.square_size//2

            self.canvas.create_line(x1, y1, x2, y2)

    '''
        Indica os nós visitados
    '''
    def draw_visited_nodes(self, nodes):
        for i in nodes:
            y = self.idx_to_pos(i[0])
            x = self.idx_to_pos(i[1])

            self.canvas.create_rectangle(x, y, x + self.square_size, y + self.square_size, fill="red")

    '''
        Evento de quando o mouse é clicado
    '''
    def mouse1_callback(self, event):
        # x e y invertido por conta da referência linha x coluna
        x = self.pos_to_idx(event.y)
        y = self.pos_to_idx(event.x)

        # Verifica se tem um obstáculo
        if(self.obstacle_map[x][y] == 1):
            return

        self.goal_pos = [x, y]
        self.draw_path()

    def mouse3_callback(self, event):
        # x e y invertido por conta da referência linha x coluna
        x = self.pos_to_idx(event.y)
        y = self.pos_to_idx(event.x)

        # Verifica se tem um obstáculo
        if(self.obstacle_map[x][y] == 1):
            return

        self.start_pos = [x, y]
        self.draw_path()

    '''
        Altera entre o modo de desenhar o histórico
        e o modo de desenhar o caminho
    '''
    def h_key_callback(self, event):
        self.draw_history = not self.draw_history
        self.draw_path()

    '''
        Alterna entre os algoritmos de pathfinding
    '''
    def p_key_callback(self, event):
        self.select_a_star = not self.select_a_star

        if self.select_a_star:
            print("A* selecionado")
        else:
            print("Dijkstra selecionado")

    '''
        Altera entre mostrar ou esconder a grade
    '''
    def g_key_callback(self, event):
        self.show_grid = not self.show_grid
        self.draw_canvas()

    def loop(self):
        tk.mainloop()
