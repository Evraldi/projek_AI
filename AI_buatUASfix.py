import tkinter as tk
import time
from tkinter import Text
from collections import deque
import sys
import psutil

# Variabel global untuk menyimpan labirin dan jalur
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

# Posisi awal dan akhir
start = (9, 0)
end = (0, 4)

def get_cpu_usage():
    return psutil.cpu_percent(interval=0.1)

def explore_paths(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Atas, bawah, kiri, kanan
    queue = deque([start])
    path = [[None] * cols for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]
    reasons = [[""] * cols for _ in range(rows)]  # Array untuk menyimpan alasan
    distance = [[float('inf')] * cols for _ in range(rows)]  # Array untuk menyimpan jarak
    
    visited[start[0]][start[1]] = True
    distance[start[0]][start[1]] = 0
    all_paths = []  # List untuk menyimpan semua jalur yang dipertimbangkan
    
    while queue:
        x, y = queue.popleft()
        all_paths.append((x, y))
        if (x, y) == end:
            break
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] == 1:
                    reasons[nx][ny] = "ada dinding coyyy"
                elif visited[nx][ny]:
                    if distance[nx][ny] > distance[x][y] + 1:
                        reasons[nx][ny] = f"Jalan sudah dikunjungi, tapi sudah ditemukan jalan yang lebih pendek dari ({x},{y})"
                    else:
                        reasons[nx][ny] = f"Jalan sudah dikunjungi, dan jalan saat ini dari ({x},{y}) tidak lebih pendek dari yang sebelumnya"
                else:
                    if distance[nx][ny] > distance[x][y] + 1:
                        queue.append((nx, ny))
                        visited[nx][ny] = True
                        path[nx][ny] = (x, y)
                        distance[nx][ny] = distance[x][y] + 1
                        reasons[nx][ny] = f"Bergerak dari ({x},{y})"

    # Lacak jalur terpendek dari akhir ke awal
    shortest_path = []
    x, y = end
    if not visited[x][y]:
        return -1, [], reasons, all_paths  # Jalur tidak ditemukan
    
    while (x, y) != start:
        shortest_path.append((x, y))
        x, y = path[x][y]
    
    shortest_path.append(start)
    shortest_path.reverse()
    
    return len(shortest_path), shortest_path, reasons, all_paths

def get_big_o_complexity(maze):
    rows, cols = len(maze), len(maze[0])
    total_cells = rows * cols

    # Hitung kompleksitas Big O berdasarkan jumlah sel
    if total_cells <= 10:
        return "O(1)"
    elif total_cells <= 100:
        return "O(n)"
    elif total_cells <= 1000:
        return "O(n log n)"
    elif total_cells <= 10000:
        return "O(n^2)"
    else:
        return "O(n^2) atau lebih"

def get_memory_usage():
    # Dapatkan penggunaan memori saat ini dalam byte
    memory_usage = sys.getsizeof(maze) + sys.getsizeof(path_taken) + sys.getsizeof(start) + sys.getsizeof(end)
    
    # Penggunaan memori tambahan untuk seluruh proses
    process = psutil.Process()
    total_memory_usage = process.memory_info().rss  # Dapatkan penggunaan memori total dalam byte
    
    return total_memory_usage

def visualize_maze():
    global maze
    global path_taken
    global start
    global end
    
    rows, cols = len(maze), len(maze[0])
    cell_size = 50
    margin = 10  # Jarak dari tepi grid labirin
    border_width = 2  # Lebar border untuk canvas
    
    delay = 100  # milidetik
    
    def create_grid():
        # Hapus item canvas sebelumnya
        canvas.delete("all")
        
        # Gambar border di sekitar canvas
        canvas.create_rectangle(margin, margin, cols*cell_size + margin, rows*cell_size + margin, outline="black", width=border_width)
        
        for i in range(rows):
            for j in range(cols):
                color = "white"
                if maze[i][j] == 1:
                    color = "gray"  # Dinding
                elif (i, j) == start:
                    color = "blue"  # Awal
                elif (i, j) == end:
                    color = "red"  # Akhir

                # Gambar setiap sel dalam grid
                cell = canvas.create_rectangle(j*cell_size + margin, i*cell_size + margin, (j+1)*cell_size + margin, (i+1)*cell_size + margin, fill=color)
                cells[(i, j)] = cell

                # Tambahkan teks dengan koordinat (warna teks merah)
                text_x = j * cell_size + margin + cell_size // 2
                text_y = i * cell_size + margin + cell_size // 2
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
        
        text_box.delete(1.0, tk.END)  # Hapus teks sebelumnya
        text_box.insert(tk.END, f"Panjang jalur: {length}\n")
        if length == -1:
            text_box.insert(tk.END, "Jalur tidak ditemukan.\n")
            return
        
        text_box.insert(tk.END, "Alasan mengapa jalur lain tidak diambil:\n")
        for i in range(rows):
            for j in range(cols):
                if reasons[i][j]:
                    text_box.insert(tk.END, f"Pada posisi ({i}, {j}): {reasons[i][j]}\n")
        
        create_grid()
        highlight_path(all_paths, "yellow")  # Sorot semua jalur yang dipertimbangkan dengan kuning
        highlight_path(path_taken, "green")  # Sorot jalur terpendek dengan hijau

        # Tampilkan penggunaan memori
        memory_usage = get_memory_usage()
        text_box.insert(tk.END, f"Penggunaan Memori: {memory_usage} byte\n")

    def show_big_o_notation():
        top = tk.Toplevel(root)
        top.title("Notasi Big O")
        
        # Teks untuk penjelasan Notasi Big O
        reasons_text = "Alasan untuk Kompleksitas Big O:\n"
        reasons_text += "---------------------------------\n"
        reasons_text += "- Algoritma mengiterasi setiap sel dalam labirin sekali, yang menghasilkan kompleksitas linear.\n"
        reasons_text += "- Ini menggunakan pendekatan pencarian lebar dengan antrian untuk menjelajahi jalur dengan efisien.\n"
        reasons_text += "- Penggunaan memori dikelola dengan struktur data yang meningkat secara linear dengan jumlah sel.\n"
    
        label = tk.Label(top, text=f"Kompleksitas Big O: {get_big_o_complexity(maze)}\n\n{reasons_text}", padx=20, pady=20)
        label.pack()

    # Inisialisasi path_taken dengan path awal
    length, path_taken, _, all_paths = explore_paths(maze, start, end)

    root = tk.Tk()
    root.title("Visualisasi Jalur Labirin")
    
    # Dapatkan lebar dan tinggi layar
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Atur lebar dan tinggi jendela
    window_width = screen_width  # Contoh lebar (sesuaikan jika perlu)
    window_height = screen_height  # Contoh tinggi (sesuaikan jika perlu)
    
    # Atur geometri jendela
    root.geometry(f"{window_width}x{window_height}")
    
    # Buat frame untuk menampung canvas dan text box
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Buat canvas untuk labirin
    canvas = tk.Canvas(frame, width=cols*cell_size + 2*margin, height=rows*cell_size + 2*margin)
    canvas.grid(row=0, column=0, sticky=tk.NSEW)  # Letakkan canvas di grid (baris 0, kolom 0)
    
    cells = {}
    create_grid()
    highlight_path(all_paths, "yellow")  # Sorot semua jalur yang dipertimbangkan dengan kuning
    highlight_path(path_taken, "green")  # Sorot jalur terpendek dengan hijau

    # Buat text box untuk mencetak alasan
    text_box = Text(frame, height=20, width=100)
    text_box.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NS)  # Letakkan text box di grid (baris 0, kolom 1)

    # Label untuk menampilkan penggunaan CPU dan memori
    cpu_label = tk.Label(frame, text="Penggunaan CPU: ", padx=10, pady=10)
    cpu_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    
    memory_label = tk.Label(frame, text="Penggunaan Memori: ", padx=10, pady=10)
    memory_label.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    
    # Tombol untuk mereset visualisasi
    reset_button = tk.Button(frame, text="Reset Visualisasi", command=reset_visualization)
    reset_button.grid(row=1, column=0, padx=10, pady=10, sticky=tk.EW)  # Letakkan tombol di grid (baris 1, kolom 0)
    
    # Tombol untuk menampilkan Notasi Big O
    big_o_button = tk.Button(frame, text="Tampilkan Notasi Big O", command=show_big_o_notation)
    big_o_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)  # Letakkan tombol di grid (baris 1, kolom 1)

    def update_metrics():
        # Perbarui label penggunaan CPU
        cpu_usage = get_cpu_usage()
        cpu_label.config(text=f"Penggunaan CPU: {cpu_usage}%")
        
        # Perbarui label penggunaan memori
        memory_usage= get_memory_usage()
        memory_label.config(text=f"Penggunaan Memori: {memory_usage} byte")

        # Jadwalkan pembaruan berikutnya setelah 1 detik
        root.after(1000, update_metrics)

    # Mulai memperbarui metrik
    update_metrics()
    
    root.mainloop()

# Mulai visualisasi labirin
visualize_maze()
