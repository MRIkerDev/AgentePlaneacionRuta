import matplotlib.pyplot as plt
import numpy as np

def visualize_path(grid, path, start, goal):

    rows, cols = len(grid), len(grid[0])
    grid_array = np.array(grid)  

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.imshow(grid_array, cmap="gray_r")

 
    if path:
        path_x, path_y = zip(*path)
        ax.plot(path_y, path_x, marker="o", color="lime", markersize=5, linewidth=2, label="Camino A*")

    ax.scatter(start[1], start[0], marker="s", color="blue", s=100, label="Inicio")  # Azul
    ax.scatter(goal[1], goal[0], marker="s", color="red", s=100, label="Destino")  # Rojo

    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle="-", linewidth=0.5)
    ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

    ax.legend(loc="upper right")

    plt.show()
