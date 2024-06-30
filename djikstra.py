import tkinter as tk
import time
from collections import deque
import matplotlib.pyplot as plt
import math

# Global variables to store maze and path
maze = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 1, 1]
]

path_taken = []

# Starting and ending positions
start = (9, 0)
end = (0, 4)

def explore_paths(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    dist = [[float('inf')] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = 0
    prev = [[None] * cols for _ in range(rows)]
    reasons = [[""] * cols for _ in range(rows)]  # Array to store reasons
    all_paths = []  # List to store all considered paths
    
    queue = [(0, start[0], start[1])]  # Priority queue with (distance, x, y)

    while queue:
        queue.sort()  # Naive sorting to pick the minimum distance vertex
        d, x, y = queue.pop(0)
        all_paths.append((x, y))
        
        if (x, y) == end:
            break
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] == 1:
                    reasons[nx][ny] = "Wall"
                elif dist[nx][ny] > d + 1:
                    dist[nx][ny] = d + 1
                    prev[nx][ny] = (x, y)
                    queue.append((dist[nx][ny], nx, ny))
                    reasons[nx][ny] = f"Updated distance from ({x},{y})"

    # Trace the shortest path from end to start
    shortest_path = []
    x, y = end
    if dist[x][y] == float('inf'):
        return -1, [], reasons, all_paths  # Path not found
    
    while (x, y) != start:
        shortest_path.append((x, y))
        x, y = prev[x][y]
    
    shortest_path.append(start)
    shortest_path.reverse()
    
    return len(shortest_path), shortest_path, reasons, all_paths

def get_big_o_complexity(maze):
    rows, cols = len(maze), len(maze[0])
    total_cells = rows * cols

    # Calculate Big O complexity based on number of cells
    if total_cells <= 10:
        return "O(1)"
    elif total_cells <= 100:
        return "O(n)"
    elif total_cells <= 1000:
        return "O(n log n)"
    elif total_cells <= 10000:
        return "O(n^2)"
    else:
        return "O(n^2) or more"

def visualize_maze():
    global maze
    global path_taken
    global start
    global end
    
    rows, cols = len(maze), len(maze[0])
    cell_size = 50
    delay = 100  # milliseconds
    
    def create_grid():
        for i in range(rows):
            for j in range(cols):
                color = "white"
                if maze[i][j] == 1:
                    color = "gray"  # Wall
                elif (i, j) == start:
                    color = "blue"  # Start
                elif (i, j) == end:
                    color = "red"  # End

                cell = canvas.create_rectangle(j*cell_size, i*cell_size, (j+1)*cell_size, (i+1)*cell_size, fill=color)
                cells[(i, j)] = cell

                # Add text with coordinates (make text color red)
                text_x = j * cell_size + cell_size // 2
                text_y = i * cell_size + cell_size // 2
                canvas.create_text(text_x, text_y, text=f"({i},{j})", fill="black")

    def highlight_path(path, color):
        for (i, j) in path:
            if (i, j) not in [start, end]:
                canvas.after(delay, lambda i=i, j=j: canvas.itemconfig(cells[(i, j)], fill=color))
                canvas.update()
                time.sleep(delay / 1000)

    def reset_visualization():
        global path_taken
        length, path_taken, reasons, all_paths = explore_paths(maze, start, end)
        
        text_box.delete(1.0, tk.END)  # Clear previous text
        text_box.insert(tk.END, f"Path length: {length}\n")
        if length == -1:
            text_box.insert(tk.END, "Path not found.\n")
            return
        
        text_box.insert(tk.END, "Reasons why other paths were not taken:\n")
        for i in range(rows):
            for j in range(cols):
                if reasons[i][j]:
                    text_box.insert(tk.END, f"At position ({i}, {j}): {reasons[i][j]}\n")
        
        create_grid()
        highlight_path(all_paths, "yellow")  # Highlight all considered paths in yellow
        highlight_path(path_taken, "green")  # Highlight shortest path in green

        # Display Big O complexity after visualization reset
        big_o_complexity = get_big_o_complexity(maze)
        big_o_label.config(text=f"Big O Complexity: {big_o_complexity}")

        # Display and plot Big O complexity
        plot_big_o_complexity()

    def plot_big_o_complexity():
        total_cells = len(maze) * len(maze[0])
        x = range(total_cells)
        y = [1 if total_cells <= 10 else (n if n <= 100 else (n * math.log(n) if n <= 1000 else (n ** 2 if n <= 10000 else (n ** 2)))) for n in x]
        plt.plot(x, y)
        plt.title('Big O Complexity')
        plt.xlabel('Number of Cells')
        plt.ylabel('Time Complexity')
        plt.figtext(0.5, 0.01, f"Number of Cells: {total_cells}", ha="center", fontsize=10, bbox={"facecolor":"white", "edgecolor":"white", "alpha":0.5})
        plt.show()

    # Initialize path_taken with initial path
    length, path_taken, _, all_paths = explore_paths(maze, start, end)

    root = tk.Tk()
    root.title("Maze Path Visualization")
    
    # Set window size
    window_width = cols * cell_size + 50  # Extra space for padding and scrollbar
    window_height = rows * cell_size + 200  # Extra space for text box and button
    root.geometry(f"{window_width}x{window_height}")
    
    # Create canvas for maze
    canvas = tk.Canvas(root, width=cols*cell_size, height=rows*cell_size)
    canvas.pack()
    
    cells = {}
    create_grid()
    highlight_path(all_paths, "yellow")  # Highlight all considered paths in yellow
    highlight_path(path_taken, "green")  # Highlight shortest path in green

    # Create text box to print reasons
    text_box = Text(root, height=7, width=100)
    text_box.pack()
    
    # Button to reset visualization
    repeat_button = tk.Button(root, text="Reset", command=reset_visualization)
    repeat_button.pack()

    # Add legend
    legend = tk.Frame(root)
    legend.pack()
    
    tk.Label(legend, text="Legend:").pack(side=tk.LEFT)
    tk.Label(legend, text="Start", fg="blue").pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="End", fg="red").pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="Wall", fg="gray").pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="Path Taken", fg="green").pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="Considered Paths", fg="yellow").pack(side=tk.LEFT, padx=10)

    # Create label for Big O complexity
    big_o_label = tk.Label(root, text="")
    big_o_label.pack()
    
    # Display Big O complexity initially
    big_o_complexity = get_big_o_complexity(maze)
    big_o_label.config(text=f"Big O Complexity: {big_o_complexity}")

    root.mainloop()

visualize_maze()
