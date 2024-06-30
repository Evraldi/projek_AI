from collections import deque

def find_shortest_path(maze):
    if not maze or not maze[0]:
        return -1, []  # Maze kosong atau tidak valid
    
    rows, cols = len(maze), len(maze[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Atas, Bawah, Kiri, Kanan
    
    queue = deque([start])
    path = {start: None}  # Untuk melacak jalur
    
    found_path = False
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == end:
            found_path = True
            break
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in path:
                if maze[nx][ny] == ' ':
                    queue.append((nx, ny))
                    path[(nx, ny)] = (x, y)
    
    if not found_path:
        return -1, []  # Tidak ada jalur yang ditemukan
    
    # Bangun jalur terpendek dari end ke start
    shortest_path = []
    x, y = end
    while (x, y) != start:
        shortest_path.append((x, y))
        x, y = path[(x, y)]
    shortest_path.append(start)
    shortest_path.reverse()
    
    return len(shortest_path), shortest_path

# Contoh penggunaan
maze = [
    [' ', ' ', ' ', '#', ' '],
    [' ', '#', ' ', '#', ' '],
    [' ', '#', ' ', '#', ' '],
    [' ', '#', ' ', '#', ' '],
    [' ', '#', ' ', '#', ' '],
    [' ', ' ', ' ', '#', ' '],
    [' ', '#', ' ', '#', ' '],
    [' ', '#', ' ', ' ', ' '],
    [' ', '#', '#', ' ', ' '],
    [' ', '#', '#', '#', '#']
]

length, path = find_shortest_path(maze)
if length == -1:
    print("Tidak ada jalur yang ditemukan.")
else:
    print(f"Panjang jalur terpendek: {length}")
    print("Jalur terpendek:", path)
