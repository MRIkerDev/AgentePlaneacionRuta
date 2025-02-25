import numpy as np
import random

class QLearningAgent:
    def __init__(self, rows, cols, q_table_cargada=None, alpha=0.1, gamma=0.9, epsilon=1.0, 
                 epsilon_decay=0.995, min_epsilon=0.1, max_repeticiones=10):
        self.rows = rows
        self.cols = cols
        self.alpha = alpha  # Tasa de aprendizaje
        self.gamma = gamma  # Factor de descuento
        self.epsilon = epsilon  # Probabilidad de exploración
        self.epsilon_decay = epsilon_decay  # Reducción de epsilon por episodio
        self.min_epsilon = min_epsilon  # Límite mínimo de epsilon
        self.max_repeticiones = max_repeticiones  # Número máximo de veces que puede visitar un estado
        self.penalizacion_estado_repetido = -5  # 🔥 Penalización por repetir estados

        # Inicializar Q-table (si no se carga una existente)
        self.q_table = q_table_cargada if q_table_cargada else {}

    def inicializar_estado(self, estado):
        """Inicializa un estado en la tabla Q si no existe."""
        if estado not in self.q_table:
            self.q_table[estado] = [0] * 4  # Cuatro acciones posibles: arriba, abajo, izquierda, derecha

    def elegir_accion(self, estado):
        """Selecciona la mejor acción usando ε-greedy."""
        self.inicializar_estado(estado)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(4))  # Exploración aleatoria
        else:
            return np.argmax(self.q_table[estado])  # Explotación de la mejor opción

    def mover(self, estado, accion, env):
        """Calcula el nuevo estado basado en la acción, evitando salir del mapa u obstáculos."""
        x, y = estado
        movimientos = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Izquierda, Derecha, Arriba, Abajo

        nx, ny = x + movimientos[accion][0], y + movimientos[accion][1]

        # Validar si está dentro de los límites y no es obstáculo
        if 0 <= nx < self.rows and 0 <= ny < self.cols and env.grid[nx][ny] == 0:
            return (nx, ny)  # Movimiento válido
        return estado  # Si el movimiento es inválido, se queda en el mismo lugar

    def actualizar_Q(self, estado, accion, recompensa, nuevo_estado, estados_visitados):
        """Actualiza la tabla Q con la ecuación de aprendizaje Q-learning."""
        self.inicializar_estado(nuevo_estado)

        # 🔥 Aplicar penalización si el agente repite estados muchas veces
        if nuevo_estado in estados_visitados:
            recompensa += self.penalizacion_estado_repetido  

        max_q_nuevo_estado = max(self.q_table[nuevo_estado])
        self.q_table[estado][accion] += self.alpha * (recompensa + self.gamma * max_q_nuevo_estado - self.q_table[estado][accion])

    def reducir_epsilon(self):
        """Reduce la exploración conforme avanza el entrenamiento."""
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
