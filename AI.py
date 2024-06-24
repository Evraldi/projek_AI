import tkinter as tk
import time
from tkinter import Text
from collections import deque

# Define global variables to store maze and path
maze = [
    [0, 1, 0, 0, 2, 0, 0, 1],
    [0, 1, 0, 1, 1, 1, 2, 1],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 2, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 1],
    [2, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0]
]

path_taken = []

def explore_paths(maze):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    queue = deque([(0, 0)])
    path = [[None] * cols for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]
    reasons = [[""] * cols for _ in range(rows)]  # Array to store reasons
    distance = [[float('inf')] * cols for _ in range(rows)]  # Array to store distances
    
    visited[0][0] = True
    distance[0][0] = 0
    all_paths = []  # List to store all paths considered
    
    while queue:
        x, y = queue.popleft()
        all_paths.append((x, y))
        if (x, y) == (rows-1, cols-1):
            break
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] == 1:
                    reasons[nx][ny] = "Wall"
                elif visited[nx][ny]:
                    if distance[nx][ny] > distance[x][y] + 1:
                        reasons[nx][ny] = f"Already visited, but found shorter path from ({x},{y})"
                    else:
                        reasons[nx][ny] = f"Already visited, and current path from ({x},{y}) is not shorter"
                else:
                    if distance[nx][ny] > distance[x][y] + 1:
                        queue.append((nx, ny))
                        visited[nx][ny] = True
                        path[nx][ny] = (x, y)
                        distance[nx][ny] = distance[x][y] + 1
                        reasons[nx][ny] = f"Moved from ({x},{y})"

    # Trace the shortest path from end to start
    shortest_path = []
    x, y = rows - 1, cols - 1
    if not visited[x][y]:
        return -1, [], reasons, all_paths  # No path found
    
    while (x, y) != (0, 0):
        shortest_path.append((x, y))
        x, y = path[x][y]
    
    shortest_path.append((0, 0))
    shortest_path.reverse()
    
    return len(shortest_path), shortest_path, reasons, all_paths

def visualize_maze():
    global maze
    global path_taken
    
    rows, cols = len(maze), len(maze[0])
    cell_size = 50
    delay = 100  # milliseconds
    
    def create_grid():
        for i in range(rows):
            for j in range(cols):
                color = "white"
                if maze[i][j] == 1:
                    color = "gray"  # Wall
                elif (i, j) == (0, 0):
                    color = "blue"  # Start
                elif (i, j) == (rows-1, cols-1):
                    color = "red"  # End

                cell = canvas.create_rectangle(j*cell_size, i*cell_size, (j+1)*cell_size, (i+1)*cell_size, fill=color)
                cells[(i, j)] = cell

                # Add text with coordinates (make the text color red)
                text_x = j * cell_size + cell_size // 2
                text_y = i * cell_size + cell_size // 2
                canvas.create_text(text_x, text_y, text=f"({i},{j})", fill="black")

    def highlight_path(path, color):
        for (i, j) in path:
            if (i, j) not in [(0, 0), (rows-1, cols-1)]:
                canvas.after(delay, lambda i=i, j=j: canvas.itemconfig(cells[(i, j)], fill=color))
                canvas.update()
                time.sleep(delay / 1000)

    def reset_visualization():
        global path_taken
        length, path_taken, reasons, all_paths = explore_paths(maze)
        
        text_box.delete(1.0, tk.END)  # Clear previous text
        text_box.insert(tk.END, f"Path length: {length}\n")
        if length == -1:
            text_box.insert(tk.END, "No path found.\n")
            return
        
        text_box.insert(tk.END, "Reasons why certain paths were not taken:\n")
        for i in range(rows):
            for j in range(cols):
                if reasons[i][j]:
                    text_box.insert(tk.END, f"At position ({i}, {j}): {reasons[i][j]}\n")
        
        create_grid()
        highlight_path(all_paths, "yellow")  # Highlight all paths considered in yellow
        highlight_path(path_taken, "green")  # Highlight the shortest path in green

    # Initialize path_taken with the initial path
    length, path_taken, _, all_paths = explore_paths(maze)

    root = tk.Tk()
    root.title("Maze Path Visualization")
    
    # Create canvas for maze
    canvas = tk.Canvas(root, width=cols*cell_size, height=rows*cell_size)
    canvas.pack()
    
    cells = {}
    create_grid()
    highlight_path(all_paths, "yellow")  # Highlight all paths considered in yellow
    highlight_path(path_taken, "green")  # Highlight the shortest path in green

    # Create text box for printing reasons
    text_box = Text(root, height=10, width=75)
    text_box.pack()
    
    # Button to repeat visualization
    repeat_button = tk.Button(root, text="Repeat", command=reset_visualization)
    repeat_button.pack()

    # Add legend
    legend = tk.Frame(root)
    legend.pack()
    
    tk.Label(legend, text="Legend:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(legend, text="Start", bg="blue").grid(row=0, column=1, padx=5, pady=5)
    tk.Label(legend, text="End", bg="red").grid(row=0, column=2, padx=5, pady=5)
    tk.Label(legend, text="Wall", bg="gray").grid(row=0, column=3, padx=5, pady=5)
    tk.Label(legend, text="Shortest Path", bg="green").grid(row=0, column=4, padx=5, pady=5)
    tk.Label(legend, text="Considered Paths", bg="yellow").grid(row=0, column=5, padx=5, pady=5)

    root.mainloop()

# Start visualization
visualize_maze()
