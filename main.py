import pygame
import time
import matplotlib.pyplot as plt
from qlearning import QLearningAgent  
from entorno import Environment
from visual import visualize_path  

pygame.init()

# ventana
WIDTH, HEIGHT = 500, 500  
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE  

# colores a utilizar
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
GREEN = (0, 255, 0)  
BLUE = (0, 0, 255)  
RED = (255, 0, 0)  
ORANGE = (255, 165, 0)  

MAX_PASOS_POR_INTENTO = 180
EPISODIOS_ENTRENAMIENTO = 350  


env = Environment(rows=GRID_SIZE, cols=GRID_SIZE, obstacle_chance=0)
start, goal = (0, 0), (GRID_SIZE-1, GRID_SIZE-1)
agent = QLearningAgent(GRID_SIZE, GRID_SIZE)


agent.recompensa_total = 0  


steps_per_episode = []
best_attempt = None  
best_attempt_steps = float("inf")  
attempts = []  

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación Q-Learning - Selección de Obstáculos")


editing_obstacles = True
training = False
running = True
waiting_for_training = True
episodes_completed = False

def draw_grid():
    screen.fill(WHITE)  
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = WHITE if env.grid[y][x] == 0 else BLACK  
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, BLUE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (goal[1] * CELL_SIZE, goal[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()  

def manejar_eventos():
    global running, editing_obstacles, training, waiting_for_training

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and editing_obstacles:
            mouse_x, mouse_y = event.pos
            grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE
            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                env.grid[grid_y][grid_x] = 1 - env.grid[grid_y][grid_x]  
                draw_grid()  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and editing_obstacles:
                editing_obstacles = False  
                waiting_for_training = True
            elif event.key == pygame.K_t and waiting_for_training:
                training = True
                waiting_for_training = False


while running:
    screen.fill(WHITE)
    manejar_eventos()

  
    draw_grid()

 
    if waiting_for_training:
        font = pygame.font.SysFont(None, 30)
        text = font.render("Presiona T para entrenar", True, (0, 0, 0))
        screen.blit(text, (10, 10))

    if training:
        for episodio in range(EPISODIOS_ENTRENAMIENTO):
            estado = start
            pasos = 0
            path = [estado]
            estados_visitados = set()

            while estado != goal and pasos < MAX_PASOS_POR_INTENTO:
                manejar_eventos()
                if not running:
                    break

                estados_visitados.add(estado)
                accion = agent.elegir_accion(estado)
                nuevo_estado = agent.mover(estado, accion, env)

                recompensa = -1  
                if nuevo_estado == goal:
                    recompensa = 100  
                    agent.recompensa_total += 10  
                elif env.grid[nuevo_estado[0]][nuevo_estado[1]] == 1:
                    recompensa = -10  
                    nuevo_estado = estado  
                elif nuevo_estado in estados_visitados:
                    recompensa -= 5  

                agent.actualizar_Q(estado, accion, recompensa, nuevo_estado, estados_visitados)
                estado = nuevo_estado
                path.append(estado)
                pasos += 1

                #se dibuja el recorrido 
                screen.fill(WHITE)
                draw_grid()
                for node in path:
                    pygame.draw.rect(screen, GREEN, (node[1] * CELL_SIZE, node[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                pygame.draw.rect(screen, ORANGE, (estado[1] * CELL_SIZE, estado[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.display.flip()
                time.sleep(0.001)

            if not running:
                break

            steps_per_episode.append(pasos)
            agent.reducir_epsilon()

            # se actualiza el mejor intento
            if estado == goal:
                attempts.append(path)  
                if pasos < best_attempt_steps:
                    best_attempt_steps = pasos
                    best_attempt = path

            print(f"Episodio {episodio+1}: {pasos} pasos | Mejor intento hasta ahora: {best_attempt_steps} pasos | Recompensa acumulada: {agent.recompensa_total}")

        training = False
        episodes_completed = True

    pygame.display.flip()

plt.plot(range(1, len(steps_per_episode) + 1), steps_per_episode, marker='o', linestyle='-')
plt.xlabel("Episodio (Intento)")
plt.ylabel("Número de pasos")
plt.title("Evolución del Aprendizaje")
plt.grid(True)
plt.show()

pygame.quit()


successful_attempts = [attempt for attempt in attempts if attempt[-1] == goal]
best_attempts = sorted(successful_attempts, key=len)[:5]  

if best_attempts:
    print(f"Se encontraron {len(best_attempts)} mejores caminos después de {EPISODIOS_ENTRENAMIENTO} episodios.")
    for i, attempt in enumerate(best_attempts):
        visualize_path(env.grid, attempt, start, goal)  
else:
    print("Ningún camino llegó a la meta.")
