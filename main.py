# Classe Graph para a representacao do grafo
class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.counter = 0
        self.adjlist = [[] for _ in range(nodes)]
        self.vertices = {}
        self.capacity = {}

    # Metodo para o sistema de identificacao de
    # IDs unicos e sequenciais
    def get_vertex(self, i, j, kind):
        key = (i, j, kind)
        if key not in self.vertices:
            self.vertices[key] = self.counter
            self.counter += 1
        
        return self.vertices[key]
    
    # Metodo para a adicao de arestas no grafo
    def add_edge(self, u, v, cap):
        self.adjlist[u].append(v)
        self.adjlist[v].append(u)
        self.capacity[(u, v)] = self.capacity.get((u, v), 0) + cap
        # Note que sempre adiciona (caso nao exista),
        # alem da aresta u->v, uma aresta v->u de capacidade 0
        # (aresta reversa)
        self.capacity.setdefault((v, u), 0)

    # BFS modificado para visitar os vertices da forma costumeira, mas:
    def bfs(self, s, parent):
        visited = [False] * self.nodes
        visited[s] = True
        queue = [s]
        while queue:
            u = queue.pop(0)
            for v in self.adjlist[u]:
                # respeitar os limites de capacidade da aresta;
                if not visited[v] and self.capacity[(u, v)] > 0:
                    visited[v] = True
                    # armazenar o parent de cada vertice no caminho, para que seja
                    # possivel "rastrear" o caminho de volta depois;
                    parent[v] = u
                    queue.append(v)
        # retornar o vetor de vertices visitados, de forma que visited[i]
        # indica se o vertice de indice i foi ou nao encontrado em alguma
        # execucao da BFS (ie, se ele eh alcancavel a partir da fonte seguindo
        # apenas arestas de capacidade residual nao nula)
        return visited

    # Metodo para a execucao do algoritmo de Ford-Fulkerson
    def ford_fulkerson(self, source, sink):
        flow = 0
        parent = [-1] * self.nodes
        # Em cada iteracao, usa o BFS para achar um caminho da fonte ao destino
        visited = self.bfs(source, parent)
        while visited[sink]:
            path_flow = float('inf')
            # Caso o caminho exista, vai "voltando" do destino para a fonte,
            # recolhendo o fluxo e armazenando em path_flow
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.capacity[(u, v)])
                v = u
            v = sink
            # Depois, faz mais uma passada do destino->fonte atualizando a capacidade
            # das arestas (a capacidade eh mantida de forma dinamica: em vez de haver
            # dois numeros por aresta (capacidade total e residual), apenas a capacidade
            # residual eh mantida e vai sendo atualizada ao longo das iteracoes do FF
            while v != source:
                u = parent[v]
                self.capacity[(u, v)] -= path_flow
                self.capacity[(v, u)] += path_flow
                v = u
            # Por fim, atualiza o fluxo maximo encontrado ate o momento
            flow += path_flow
            visited = self.bfs(source, parent)
        # E, nao havendo mais caminhos possiveis, retorna esse valor maximo encontrado
        return flow

def main():
    # Leitura da entrada
    # Tabuleiro MxN
    size = input()
    m, n = tuple(map(int, size.split(' ')))
    matrix = []
    
    for _ in range(m):
        line = input().strip()
        line = list(map(int, line.split(' ')))
        matrix.append(line)
    
    # Leitura das coordenadas da capital
    # 0-based
    capital = input()
    capital = tuple(map(lambda n: int(n) - 1, capital.split(' ')))
    
    # Criacao do grafo
    # Cada item da matriz se transforma em 2 vertices (vertices "gemeos")
    # Um item da matriz corresponde a um vertice de entrada
    # e um vertice de saida
    # Grafo tem 2Mx2N = 4*M*N vertices
    graph = Graph(m * n * 4)
    for i in range(m):
        for j in range(n):
            # Somente prosseguir para vertices nao-montanha
            if matrix[i][j] == 0: continue

            # Sistema baseado em IDs para identificacao dos vertices
            # get_vertex() cria um ID automatico sequencial
            # Adiciona aresta entre cada par de vertices "gemeos"
            # com capacidade indicada na matriz; ou seja, adiciona
            # aresta entrada-saida em cada par de vertices gemeos
            u_in = graph.get_vertex(i, j, 'in')
            u_out = graph.get_vertex(i, j, 'out')
            graph.add_edge(u_in, u_out, matrix[i][j])

            # Adicionando arestas com capacidade infinita entre:
            # saida-do-atual e entrada-do-fronteirico.
            # Ou seja, conecta a saida de cada vertice
            # com a entrada dos vertices adjacentes (esq/dir, cima/baixo)
            # com capacidade infinita
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = i+dx, j+dy
                if 0 <= ni < m and 0 <= nj < n and matrix[ni][nj] != 0:
                    neighbor = graph.get_vertex(ni, nj, 'in')
                    graph.add_edge(u_out, neighbor, float('inf'))

    # Criacao da pseudo-fonte e pseudo-destino
    # Note que esses dois vertices nao tem
    # versao "entrada e saida" como os demais
    # Ou seja, sao vertices unicos (nao possuem
    # "duas representacoes")
    source = graph.counter
    sink = source + 1
    graph.counter += 2

    # Acrescentando arestas saindo da pseudo-fonte e entrando
    # no vertice de entrada das posicoes limites (fronteiricas)
    # do tabuleiro.
    # Para todos os elementos da matriz:
    for i in range(m):
        for j in range(n):
            # Se o elemento nao eh montanha e esta na fronteira:
            if matrix[i][j] != 0 and (i == 0 or j == 0 or i == m-1 or j == n-1):
                # Adiciona aresta fonte -> entrada-do-vertice
                limit = graph.get_vertex(i, j, 'in')
                graph.add_edge(source, limit, float('inf'))

    # Acrescentando aresta saida-da-capital -> pseudo-destino
    capital = graph.get_vertex(capital[0], capital[1], 'out')
    graph.add_edge(capital, sink, float('inf'))

    # Por fim, computando o fluxo maximo e imprimindo
    flow = graph.ford_fulkerson(source, sink)
    print(flow)

if __name__ == '__main__':
    main()
