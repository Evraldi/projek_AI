import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt

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
    from collections import deque
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

class MazeVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Maze Path Visualization')
        self.setGeometry(100, 100, 800, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Maze grid layout
        self.grid_layout = QGridLayout()
        self.cells = {}
        
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                cell = QLabel()
                cell.setFixedSize(50, 50)
                cell.setAlignment(Qt.AlignCenter)
                
                if maze[i][j] == 1:
                    cell.setStyleSheet('background-color: gray;')
                elif (i, j) == (0, 0):
                    cell.setStyleSheet('background-color: blue;')
                elif (i, j) == (len(maze)-1, len(maze[0])-1):
                    cell.setStyleSheet('background-color: red;')
                else:
                    cell.setStyleSheet('background-color: white;')
                
                self.grid_layout.addWidget(cell, i, j)
                self.cells[(i, j)] = cell
        
        main_layout.addLayout(self.grid_layout)
        
        # Button and reasons layout
        button_reasons_layout = QHBoxLayout()
        
        # Button to reset visualization
        self.reset_button = QPushButton('Repeat')
        self.reset_button.clicked.connect(self.reset_visualization)
        button_reasons_layout.addWidget(self.reset_button)
        
        # Reasons text box
        self.text_box = QTextEdit()
        self.text_box.setFixedHeight(200)
        button_reasons_layout.addWidget(self.text_box)
        
        main_layout.addLayout(button_reasons_layout)
        
        # Start initial visualization
        self.reset_visualization()
    
    def highlight_path(self, path, color):
        delay = 200  # Milliseconds between each step
        
        def animate_path(path):
            for (i, j) in path:
                if (i, j) not in [(0, 0), (len(maze)-1, len(maze[0])-1)]:
                    QTimer.singleShot(delay, lambda i=i, j=j: self.cells[(i, j)].setStyleSheet(f'background-color: {color};'))
                    QTimer.singleShot(delay, lambda: None)
                    QApplication.processEvents()  # Process events to update GUI
        
        animate_path(path)
    
    def reset_visualization(self):
        global path_taken
        length, path_taken, reasons, all_paths = explore_paths(maze)
        
        self.text_box.clear()
        self.text_box.append(f"Path length: {length}")
        if length == -1:
            self.text_box.append("No path found.")
            return
        
        self.text_box.append("Reasons why certain paths were not taken:")
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if reasons[i][j]:
                    self.text_box.append(f"At position ({i}, {j}): {reasons[i][j]}")
        
        # Reset grid colors
        for (i, j) in self.cells:
            if maze[i][j] == 1:
                self.cells[(i, j)].setStyleSheet('background-color: gray;')
            elif (i, j) == (0, 0):
                self.cells[(i, j)].setStyleSheet('background-color: blue;')
            elif (i, j) == (len(maze)-1, len(maze[0])-1):
                self.cells[(i, j)].setStyleSheet('background-color: red;')
            else:
                self.cells[(i, j)].setStyleSheet('background-color: white;')
        
        # Highlight paths
        self.highlight_path(all_paths, 'yellow')
        self.highlight_path(path_taken, 'green')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    visualizer = MazeVisualizer()
    visualizer.show()
    sys.exit(app.exec_())
