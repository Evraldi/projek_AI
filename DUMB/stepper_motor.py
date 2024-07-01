import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configuration
steps_per_revolution = 200
angle_per_step = 360 / steps_per_revolution

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.grid(True)

# Motor body (circle) and shaft (line)
motor_body = plt.Circle((0, 0), 0.5, fill=False, color='blue', linestyle='--')
ax.add_patch(motor_body)
shaft, = ax.plot([], [], lw=2, color='red')

# Text to display the step number
step_text = ax.text(-1.5, 1.7, '', fontsize=12)

# Animation control variables
running = True

# Function to initialize the plot
def init():
    shaft.set_data([], [])
    step_text.set_text('')
    return shaft, step_text

# Function to update the plot for each frame
def update(frame):
    if not running:
        return shaft, step_text

    angle = frame * angle_per_step
    x = np.cos(np.radians(angle))
    y = np.sin(np.radians(angle))
    shaft.set_data([0, x], [0, y])
    step_text.set_text(f'Step: {frame + 1}')
    return shaft, step_text

# Animation function
ani = animation.FuncAnimation(fig, update, frames=steps_per_revolution, init_func=init, blit=True, repeat=True)

# Event handler to start and stop the animation
def on_click(event):
    global running
    running = not running

# Connecting the click event to the handler
fig.canvas.mpl_connect('button_press_event', on_click)

# Display the plot
plt.title("Stepper Motor Visualization")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
