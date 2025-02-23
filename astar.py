import heapq

def astar(grid, start, goal):
    """
    Implementación del algoritmo A* en una cuadrícula.
    
    Parámetros:
        - grid: Matriz (lista de listas) que representa el entorno (0 = libre, 1 = obstáculo).
        - start: Coordenada inicial (fila, columna).
        - goal: Coordenada destino (fila, columna).
    
    Retorna:
        - Lista con el camino óptimo [(fila1, col1), (fila2, col2), ...] o None si no hay camino.
    """

    # Dimensiones de la cuadrícula
    rows, cols = len(grid), len(grid[0])

    # Cola de prioridad (nodos abiertos)
    open_list = []
    heapq.heappush(open_list, (0, start))  # (costo total f, nodo actual)

    # Diccionarios para rastrear el mejor camino encontrado
    came_from = {start: None}  # Nodo previo de cada posición
    g_score = {start: 0}  # Costo acumulado desde el inicio

    def heuristic(a, b):
        """Función heurística: Distancia Manhattan entre dos puntos."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while open_list:
        _, current = heapq.heappop(open_list)  # Extrae el nodo con menor costo f(n)

        if current == goal:  # Si llegamos al destino, reconstruimos el camino
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Devuelve el camino desde inicio hasta destino

        # Movimientos posibles (arriba, abajo, izquierda, derecha)
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            # Validar si está dentro de los límites y no es un obstáculo
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor[0]][neighbor[1]] == 0:
                temp_g_score = g_score[current] + 1  # Cada paso tiene un costo de 1

                # Si es un camino mejor, lo guardamos
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    g_score[neighbor] = temp_g_score
                    f_score = temp_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score, neighbor))
                    came_from[neighbor] = current

    return None  # No hay camino posible