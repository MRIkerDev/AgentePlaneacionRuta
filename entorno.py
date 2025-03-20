import random

class Environment:
    def __init__(self, rows=30, cols=30, obstacle_chance=0.2):
        self.rows = rows
        self.cols = cols
        self.grid = self.generate_grid(obstacle_chance)

    def generate_grid(self, obstacle_chance):
        grid = [[0 if random.random() > obstacle_chance else 1 for _ in range(self.cols)] for _ in range(self.rows)]
        grid[0][0] = 0  # Punto de inicio
        grid[self.rows - 1][self.cols - 1] = 0  # Punto de llegada
        
        return grid

    def display(self):
        for row in self.grid:
            print(" ".join("█" if cell == 1 else "." for cell in row))

