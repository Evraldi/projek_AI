import tkinter as tk
import time
from tkinter import Text
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

def dfs(maze, current, end, visited, path, reasons, all_paths, distances):
    if current == end:
        return path
    
    x, y = current
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    rows, cols = len(maze), len(maze[0])
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if maze[nx][ny] == 1:
                reasons[nx][ny] = "Wall"
            elif visited[nx][ny]:
                reasons[nx][ny] = "Already Visited"
            else:
                visited[nx][ny] = True
                all_paths.append((nx, ny))
                distances[nx][ny] = distances[x][y] + 1
                path.append((nx, ny))
                result = dfs(maze, (nx, ny), end, visited, path, reasons, all_paths, distances)
                if result is not None:
                    return result
                path.pop()
                visited[nx][ny] = False
                reasons[nx][ny] = f"Backtracking from ({nx},{ny})"
    
    return None

def explore_paths(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    path = []
    reasons = [[""] * cols for _ in range(rows)]
    distances = [[float('inf')] * cols for _ in range(rows)]
    all_paths = []

    visited[start[0]][start[1]] = True
    distances[start[0]][start[1]] = 0
    path.append(start)
    all_paths.append(start)
    
    shortest_path = dfs(maze, start, end, visited, path, reasons, all_paths, distances)
    
    if shortest_path is None:
        return -1, [], reasons, all_paths
    
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
    tk.Label(legend, text="Path", fg="green").pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="Wall", fg="gray").pack(side=tk.LEFT, padx=10)

    # Label to display Big O complexity
    big_o_label = tk.Label(root, text="")
    big_o_label.pack()

    # Display initial Big O complexity
    big_o_complexity = get_big_o_complexity(maze)
    big_o_label.config(text=f"Big O Complexity: {big_o_complexity}")

    # Start main loop
    root.mainloop()

# Start visualization
visualize_maze()
