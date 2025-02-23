import random

class Environment:
    """
    Representa el entorno donde se moverá el agente A*.
    """

    def __init__(self, rows=30, cols=30, obstacle_chance=0.2):
        """
        Crea una cuadrícula con obstáculos aleatorios.
        
        Parámetros:
            - rows: Número de filas en la cuadrícula.
            - cols: Número de columnas en la cuadrícula.
            - obstacle_chance: Probabilidad de que una celda sea un obstáculo (valor entre 0 y 1).
        """
        self.rows = rows
        self.cols = cols
        self.grid = self.generate_grid(obstacle_chance)

    def generate_grid(self, obstacle_chance):
        """Genera una cuadrícula con obstáculos aleatorios."""
        grid = [[0 if random.random() > obstacle_chance else 1 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Asegurar que el punto de inicio y destino sean transitables
        grid[0][0] = 0  # Punto de inicio
        grid[self.rows - 1][self.cols - 1] = 0  # Punto de llegada
        
        return grid

    def display(self):
        """Imprime la cuadrícula en la terminal (para depuración)."""
        for row in self.grid:
            print(" ".join("█" if cell == 1 else "." for cell in row))

# Prueba rápida del entorno
if __name__ == "__main__":
    env = Environment(rows=10, cols=10, obstacle_chance=0.2)
    env.display()
