import tkinter as tk
import time
from tkinter import Text
from collections import deque

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

# Starting and ending positions
start = (9, 0)
end = (0, 4)

# Global variables to store paths found by BFS and DFS
path_bfs = []
path_dfs = []

def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    queue = deque([start])
    path = [[None] * cols for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]

    visited[start[0]][start[1]] = True

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            break

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] == 1 or visited[nx][ny]:
                    continue
                queue.append((nx, ny))
                visited[nx][ny] = True
                path[nx][ny] = (x, y)

    # Trace the shortest path from end to start
    shortest_path = []
    x, y = end
    if not visited[x][y]:
        return -1, []  # Path not found

    while (x, y) != start:
        shortest_path.append((x, y))
        x, y = path[x][y]

    shortest_path.append(start)
    shortest_path.reverse()

    return len(shortest_path), shortest_path

def dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    stack = [(start, [start])]
    visited = [[False] * cols for _ in range(rows)]

    while stack:
        (x, y), path = stack.pop()
        if (x, y) == end:
            return len(path), path
        
        if visited[x][y]:
            continue
        
        visited[x][y] = True
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] == 0 and not visited[nx][ny]:
                    stack.append(((nx, ny), path + [(nx, ny)]))

    return -1, []  # Path not found

def explore_paths(maze, start, end):
    bfs_length, bfs_path = bfs(maze, start, end)
    dfs_length, dfs_path = dfs(maze, start, end)
    
    return bfs_length, bfs_path, dfs_length, dfs_path

def visualize_maze():
    global maze
    global start
    global end
    global path_bfs
    global path_dfs
    
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
        path_bfs, path_dfs
        
        # Clear previous paths
        canvas.delete("all")
        path_bfs.clear()
        path_dfs.clear()
        
        # Initialize paths for both algorithms
        bfs_length, path_bfs, dfs_length, path_dfs = explore_paths(maze, start, end)

        # Display paths
        create_grid()
        highlight_path(path_bfs, "green")  # Highlight BFS path in green
        highlight_path(path_dfs, "purple")  # Highlight DFS path in purple

        # Display lengths
        text_box.delete(1.0, tk.END)  # Clear previous text
        text_box.insert(tk.END, f"BFS Path length: {bfs_length}\n")
        text_box.insert(tk.END, f"DFS Path length: {dfs_length}\n")

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

    # Create text box to print path lengths
    text_box = Text(root, height=2, width=100)
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
    tk.Label(legend, text="BFS Path", fg="green").pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="DFS Path", fg="purple").pack(side=tk.LEFT, padx=10)
    tk.Label(legend, text="Wall", fg="gray").pack(side=tk.LEFT, padx=10)

    # Initialize paths for both algorithms
    bfs_length, path_bfs, dfs_length, path_dfs = explore_paths(maze, start, end)

    # Display paths
    highlight_path(path_bfs, "green")  # Highlight BFS path in green
    highlight_path(path_dfs, "purple")  # Highlight DFS path in purple

    # Start main loop
    root.mainloop()

# Start visualization
visualize_maze()
