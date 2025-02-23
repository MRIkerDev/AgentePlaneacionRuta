import pygame
import time
from astar import astar
from entorno import Environment
from visual import visualize_path  # Importamos la función de Matplotlib

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 500, 500  # Tamaño de la ventana
GRID_SIZE = 10  # Tamaño de la cuadrícula
CELL_SIZE = WIDTH // GRID_SIZE  # Tamaño de cada celda

# Colores
WHITE = (255, 255, 255)  # Camino libre
BLACK = (0, 0, 0)  # Obstáculos
GREEN = (0, 255, 0)  # Camino recorrido
BLUE = (0, 0, 255)  # Inicio
RED = (255, 0, 0)  # Destino
ORANGE = (255, 165, 0)  # Agente en movimiento

# Crear entorno
env = Environment(rows=GRID_SIZE, cols=GRID_SIZE, obstacle_chance=0)
start, goal = (0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)

# Crear ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación A* - Animación Paso a Paso")

# Posición inicial del agente
agent_pos = list(start)
visited_nodes = []  # Lista para pintar el camino recorrido

# Variables para controlar la edición de obstáculos
editing_obstacles = True

# Bucle principal
running = True
path_index = 0  # Índice para recorrer el camino paso a paso

while running:
    screen.fill(WHITE)  # Fondo blanco

    # Dibujar cuadrícula y obstáculos
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = WHITE if env.grid[y][x] == 0 else BLACK  # Blanco = libre, Negro = obstáculo
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Dibujar punto de inicio y fin
    pygame.draw.rect(screen, BLUE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Inicio
    pygame.draw.rect(screen, RED, (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Fin

    # Dibujar el camino recorrido hasta el momento
    for node in visited_nodes:
        pygame.draw.rect(screen, GREEN, (node[1] * CELL_SIZE, node[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Mover al agente paso a paso
    if not editing_obstacles and path and path_index < len(path):
        agent_pos = path[path_index]  # Obtener la siguiente posición en el camino
        visited_nodes.append(agent_pos)  # Guardar la posición para pintarla en verde
        pygame.draw.rect(screen, ORANGE, (agent_pos[1] * CELL_SIZE, agent_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Agente en movimiento
        path_index += 1  # Avanzar en el camino
    elif not editing_obstacles:
        running = False  # Detener el bucle cuando termine el recorrido

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and editing_obstacles:
            # Obtener la posición del clic
            mouse_x, mouse_y = event.pos
            grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
            # Verificar que los índices estén dentro de los límites de la cuadrícula
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                # Alternar el estado del obstáculo en la celda clicada
                env.grid[grid_y][grid_x] = 1 - env.grid[grid_y][grid_x]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Finalizar la edición de obstáculos y calcular el camino
                editing_obstacles = False
                path = astar(env.grid, start, goal)

    pygame.display.flip()  # Actualizar pantalla
    if not editing_obstacles:
        time.sleep(0.3)  # Controlar la velocidad de animación

pygame.quit()

# 📌 Llamar a Matplotlib después de cerrar Pygame
if path:
    visualize_path(env.grid, path, start, goal)  # Mostrar el mapa en Matplotlib