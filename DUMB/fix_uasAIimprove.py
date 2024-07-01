import tkinter as tk
import time
from tkinter import Text
from collections import deque
import sys  # For memory usage
import heapq  # For A* Search

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

start = (9, 0)
end = (0, 4)

def explore_paths(maze, start, end):
    """
    Finds the shortest path in a maze using A* Search algorithm.
    
    Args:
        maze (list of lists): The maze represented as a 2D grid of 0s (open) and 1s (walls).
        start (tuple): Coordinates (row, col) of the starting position.
        end (tuple): Coordinates (row, col) of the ending position.
        
    Returns:
        int: Length of the shortest path.
        list of tuples: List of coordinates representing the shortest path from start to end.
    """
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    
    def heuristic(x, y):
        return abs(end[0] - x) + abs(end[1] - y)
    
    queue = [(heuristic(start[0], start[1]), start)]
    path = {start: None}
    cost = {start: 0}
    
    while queue:
        _, (x, y) = heapq.heappop(queue)
        
        if (x, y) == end:
            break
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0:  # Check if valid move
                new_cost = cost[(x, y)] + 1
                if (nx, ny) not in cost or new_cost < cost[(nx, ny)]:
                    cost[(nx, ny)] = new_cost
                    priority = new_cost + heuristic(nx, ny)
                    heapq.heappush(queue, (priority, (nx, ny)))
                    path[(nx, ny)] = (x, y)
    
    # Trace the shortest path from end to start
    shortest_path = []
    x, y = end
    while (x, y) != start:
        shortest_path.append((x, y))
        x, y = path[(x, y)]
    
    shortest_path.append(start)
    shortest_path.reverse()
    
    return len(shortest_path), shortest_path

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

def get_memory_usage():
    # Get current memory usage in bytes
    memory_usage = sys.getsizeof(maze) + sys.getsizeof(start) + sys.getsizeof(end)
    return memory_usage

def visualize_maze():
    global maze
    global start
    global end
    
    rows, cols = len(maze), len(maze[0])
    cell_size = 50
    margin = 10  # Margin around the maze grid
    border_width = 2  # Border width for the canvas
    
    delay = 100  # milliseconds
    
    def create_grid():
        # Clear previous canvas items
        canvas.delete("all")
        
        # Draw border around the canvas
        canvas.create_rectangle(margin, margin, cols*cell_size + margin, rows*cell_size + margin, outline="black", width=border_width)
        
        for i in range(rows):
            for j in range(cols):
                color = "white"
                if maze[i][j] == 1:
                    color = "gray"  # Wall
                elif (i, j) == start:
                    color = "blue"  # Start
                elif (i, j) == end:
                    color = "red"  # End

                # Draw each cell within the grid
                cell = canvas.create_rectangle(j*cell_size + margin, i*cell_size + margin, (j+1)*cell_size + margin, (i+1)*cell_size + margin, fill=color)
                cells[(i, j)] = cell

                # Add text with coordinates (make text color red)
                text_x = j * cell_size + margin + cell_size // 2
                text_y = i * cell_size + margin + cell_size // 2
                canvas.create_text(text_x, text_y, text=f"({i},{j})", fill="black")

    def animate_path(path, color):
        for (i, j) in path:
            if (i, j) not in [start, end]:
                canvas.itemconfig(cells[(i, j)], fill=color)
                canvas.update()
                time.sleep(delay / 1000)

    def reset_visualization():
        maze, start, end
        
        # Check if start and end positions are within bounds
        if not (0 <= start[0] < rows and 0 <= start[1] < cols):
            raise ValueError("Start position is outside maze boundaries.")
        
        if not (0 <= end[0] < rows and 0 <= end[1] < cols):
            raise ValueError("End position is outside maze boundaries.")
        
        # Reset maze visualization
        length, path_taken = explore_paths(maze, start, end)
        
        # Clear previous text
        text_box.delete(1.0, tk.END)
        
        if length == -1:
            text_box.insert(tk.END, "Path not found.\n")
        else:
            text_box.insert(tk.END, f"Path length: {length}\n")
            animate_path(path_taken, "green")  # Highlight shortest path in green
        
        # Display memory usage
        memory_usage = get_memory_usage()
        text_box.insert(tk.END, f"Memory Usage: {memory_usage} bytes\n")
        
        # Display Big O notation
        text_box.insert(tk.END, f"Big O Complexity: {get_big_o_complexity(maze)}\n")
        
        create_grid()

    def set_start_position(new_start):
        start
        start = new_start
        reset_visualization()

    def set_end_position(new_end):
        end
        end = new_end
        reset_visualization()

    root = tk.Tk()
    root.title("Maze Path Visualization")
    
    # Retrieve screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set window width and height
    window_width = screen_width  # Example width (adjust as needed)
    window_height = screen_height  # Example height (adjust as needed)
    
    # Set window geometry
    root.geometry(f"{window_width}x{window_height}")
    
    # Create frame to hold canvas and text box
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Create canvas for maze
    canvas = tk.Canvas(frame, width=cols*cell_size + 2*margin, height=rows*cell_size + 2*margin)
    canvas.grid(row=0, column=0, sticky=tk.NSEW)  # Place canvas in grid (row 0, column 0)
    
    cells = {}
    create_grid()

    # Create text box to print reasons
    text_box = Text(frame, height=20, width=100)
    text_box.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)  # Place text box in grid (row 0, column 1)
    
    # Button to reset visualization
    reset_button = tk.Button(frame, text="Reset Visualization", command=reset_visualization)
    reset_button.grid(row=1, column=0, padx=10, pady=10, sticky=tk.EW)  # Place button in grid (row 1, column 0)
    
    # Button to set start position
    start_button = tk.Button(frame, text="Set Start Position", command=lambda: set_start_position((3, 0)))
    start_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)  # Place button in grid (row 1, column 1)
    
    # Button to set end position
    end_button = tk.Button(frame, text="Set End Position", command=lambda: set_end_position((6, 4)))
    end_button.grid(row=1, column=2, padx=10, pady=10, sticky=tk.EW)  # Place button in grid (row 1, column 2)

    root.mainloop()

# Start the maze visualization
visualize_maze()
