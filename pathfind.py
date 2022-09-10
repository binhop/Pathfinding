class PathFind():
    def __init__(self):
        self.d_cost = 14
        self.n_cost = 10
        self.movements = [(-1,-1,self.d_cost), (1,0,self.n_cost), (-1,1,self.d_cost),
                          (0,-1,self.n_cost),                     (0,1,self.n_cost),
                          (1,-1,self.d_cost), (-1,0,self.n_cost), (1,1,self.d_cost)]

        #self.movements = [(-1,0,self.n_cost), (0,-1,self.n_cost), (0,1,self.n_cost), (1,0,self.n_cost)]

    '''
        Informa se o nó está na lista dos
        nós abertos ou dos nós fechados
    '''
    def detect_open(self, pos, open, closed, cost):
        # Verifica se o nó está na lista dos abertos
        for i in range(len(open)):
            if(open[i][0] == pos[0] and open[i][1] == pos[1]):
                open[i][2] = min(cost, open[i][2])
                return 1
 
        for i in range(len(closed)):
            if(closed[i][0] == pos[0] and closed[i][1] == pos[1]):
                return 1

        return 0

    '''
        Encontra o caminho a partir de uma lista de nós percorridos
    '''
    def inverse_search(self, start_pos, closed):
        path = [closed[-1]]
        found = False

        while not found:
            node = path[-1] # Nó atual
            
            if(node[0] == start_pos[0] and node[1] == start_pos[1]):
                found = True
                break

            # Adiciona o nó origem ao caminho
            idx = node[3]
            path.append(closed[idx])

        path.reverse()
        return path, closed

    '''
        Encontra o melhor caminho utilizando o
        algoritmo Dijkstra's
    '''
    def normal_search(self, start_pos, goal_pos, map):
        # Nós abertos: x, y, custo, index do no de origem
        open = [[start_pos[0], start_pos[1], 0, 0]]
        # Nós fechados
        closed = []

        found = False
        while len(open):
            current_node = open[0]
            # Abre o nó com menor custo
            for i in open:
                if i[2] < current_node[2]:
                    current_node = i
            
            # Remove o nó da lista e adiciona à lista de fechados
            open.remove(current_node)
            closed.append(current_node)

            # Verifica se alcançou o objetivo
            if (current_node[0] == goal_pos[0] and current_node[1] == goal_pos[1]):
                found = True
                break

            # Adiciona os nós vizinhos à lista de abertos
            for i in self.movements:
                x = current_node[0] + i[0]
                y = current_node[1] + i[1]

                # Verifica se o nó está dentro do mapa
                if(x < 0 or y < 0 or x >= len(map) or y >= len(map)):
                    continue

                # Verifica se o vizinho é um obstáculo
                if(map[x][y] == 1):
                    continue
                
                cost = current_node[2] + i[2]

                # Verifica se o nó já foi descoberto
                # e se já tiver sido, atualiza o custo
                if (self.detect_open((x,y), open, closed, cost)):
                    continue
                
                open.append([x, y, cost, len(closed)-1])

        if found:
            return self.inverse_search(start_pos, closed)
        else:
            return []

    def heuristic(self, node, goal_pos):
        x = abs(node[0] - goal_pos[0])
        y = abs(node[1] - goal_pos[1])

        if x > y:
            return y*self.d_cost + (x-y)*self.n_cost
        else:
            return x*self.d_cost + (y-x)*self.n_cost

    '''
        Encontra o melhor caminho utilizando o
        algoritmo A*
    '''
    def a_star_search(self, start_pos, goal_pos, map):
        # Nós abertos: x, y, custo, index do no de origem
        open = [[start_pos[0], start_pos[1], 0, 0]]
        # Nós fechados
        closed = []

        found = False
        while len(open):
            current_node = open[0]
            # Abre o nó com menor custo
            for i in open:
                if i[2] < current_node[2]:
                    current_node = i
            
            # Remove o nó da lista e adiciona à lista de fechados
            open.remove(current_node)
            closed.append(current_node)

            # Verifica se alcançou o objetivo
            if (current_node[0] == goal_pos[0] and current_node[1] == goal_pos[1]):
                found = True
                break

            # Adiciona os nós vizinhos à lista de abertos
            for i in self.movements:
                x = current_node[0] + i[0]
                y = current_node[1] + i[1]

                # Verifica se o nó está dentro do mapa
                if(x < 0 or y < 0 or x >= len(map) or y >= len(map)):
                    continue

                # Verifica se o vizinho é um obstáculo
                if(map[x][y] == 1):
                    continue
                
                # g_cost = last_g_cost + movement
                # g_cost = last_f_cost - last_h_cost + movement
                if(current_node[2] != 0):
                    g_cost = current_node[2] - self.heuristic((current_node[0], current_node[1]), goal_pos) + i[2]
                else:
                    g_cost = i[2]

                h_cost = self.heuristic((x, y), goal_pos)
                f_cost = g_cost + h_cost

                # Verifica se o nó já foi descoberto
                # e se já tiver sido, atualiza o custo
                if (self.detect_open((x,y), open, closed, f_cost)):
                    continue
                
                open.append([x, y, f_cost, len(closed)-1])

        if found:
            return self.inverse_search(start_pos, closed)
        else:
            return []
