import numpy as np
import matplotlib.pyplot as plt
import math
import csv
from matplotlib.patches import RegularPolygon

minSpeed = 1
maxSpeed = 15
minT = 1
maxT = 6
map_x_min = -1000
map_x_max = 1000
map_y_min = -1250
map_y_max = 1250
map_size_x = map_x_max - map_x_min
map_size_y = map_y_max - map_y_min
x, y = 250, 0
Ttotal = 900

isd = 500


pos= [(0, 0),(0, isd),(0, -isd),(isd * np.sqrt(3) / 2, isd / 2),(-isd * np.sqrt(3) / 2, -isd / 2),(-isd * np.sqrt(3) / 2, isd / 2),(isd * np.sqrt(3) / 2, -isd / 2),(isd * np.sqrt(3), 0),(-isd * np.sqrt(3), 0),(isd * np.sqrt(3), isd),(-isd * np.sqrt(3), isd),(isd * np.sqrt(3), -isd),(-isd * np.sqrt(3), -isd),(isd * np.sqrt(3) / 2, 3 * isd / 2),(-isd * np.sqrt(3) / 2, 3 * isd / 2),(isd * np.sqrt(3) / 2, -3 * isd / 2),(-isd * np.sqrt(3) / 2, -3 * isd / 2),(0, 2 * isd),(0, -2 * isd)]

NUM_CELLS = 19
maxRange = isd * 5
csv_filename = 'handoff_events.csv'

def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_nearest_cell(position, bs_positions):
    min_dist = float('inf')
    nearest_cell_id = None
    for idx, bs in enumerate(bs_positions, start=1):
        dist = distance(position, bs)
        if dist < min_dist:
            min_dist = dist
            nearest_cell_id = idx
    return nearest_cell_id

def wrap_position(x, y, max_range):
    wrapped_x = x
    wrapped_y = y
    if wrapped_x > max_range:
        wrapped_x -= 2 * max_range
    elif wrapped_x < -max_range:
        wrapped_x += 2 * max_range

    if wrapped_y > max_range:
        wrapped_y -= 2 * max_range
    elif wrapped_y < -max_range:
        wrapped_y += 2 * max_range

    return wrapped_x, wrapped_y

def generate_movement():
    theta = np.random.uniform(0, 2 * np.pi)
    v = np.random.uniform(minSpeed, maxSpeed)
    t = np.random.uniform(minT, maxT)
    return theta, v, t

def plot_cells(ax, bs_positions, isd):

    side_length = isd / math.sqrt(3)
    
    for idx, bs in enumerate(bs_positions, start=1):
        hexagon = RegularPolygon(
            (bs[0], bs[1]),
            numVertices=6,
            radius=side_length,
            orientation=np.pi / 6,
            edgecolor='k',
            facecolor='none',
            linewidth=1
        )
        ax.add_patch(hexagon)
        ax.text(bs[0], bs[1], str(idx), color='black', fontsize=10,
                ha='center', va='center', fontweight='bold')
    buffer = side_length * 2
    all_x = [bs[0] for bs in bs_positions]
    all_y = [bs[1] for bs in bs_positions]
    ax.set_xlim(min(all_x) - buffer, max(all_x) + buffer)
    ax.set_ylim(min(all_y) - buffer, max(all_y) + buffer)
    
    ax.set_title('19-Cell Layout with Mobile Device Trajectory')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_aspect('equal')
    ax.grid(True)

def plot_path(ax, path, handoff_points):
    path = np.array(path)
    ax.plot(path[:,0], path[:,1], color='blue', linewidth=1, label='path')
    
    if handoff_points:
        handoff_points = np.array(handoff_points)
        ax.scatter(handoff_points[:,0], handoff_points[:,1], color='red', marker='x',
                   s=15, label='Handoff Points')
    
    ax.scatter(path[0,0], path[0,1], color='green', marker='o',
               s=50, label='Start')
    ax.scatter(path[-1,0], path[-1,1], color='purple', marker='o',
               s=50, label='End')
    
    ax.legend()

def save_handoff_events_to_csv(handoff_events, filename):

    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ['Time (s)', 'Source Cell ID', 'Destination Cell ID']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for event in handoff_events:
            writer.writerow({
                'Time (s)': f"{event['time']}s",
                'Source Cell ID': event['source'],
                'Destination Cell ID': event['destination']
            })



def simulation():
    time_elapsed = 0
    position = (x, y)
    current_cell = find_nearest_cell(position, pos)
    path = [position]
    handoff_points = []
    handoff_events = []

    while time_elapsed < Ttotal:
        theta, v, t = generate_movement()
        
        if time_elapsed + t > Ttotal:
            t = Ttotal - time_elapsed
        dx = v * t * math.cos(theta)
        dy = v * t * math.sin(theta)
        new_x = position[0] + dx
        new_y = position[1] + dy
        new_x, new_y = wrap_position(new_x, new_y, maxRange)
        new_position = (new_x, new_y)
        new_cell = find_nearest_cell(new_position, pos)
        
        if new_cell != current_cell:
            handoff_time = round(time_elapsed + t, 2)
            handoff_events.append({
                'time': handoff_time,
                'source': current_cell,
                'destination': new_cell
            })
            handoff_points.append(new_position)
            current_cell = new_cell
        
        time_elapsed += t
        position = new_position
        path.append(position)
    save_handoff_events_to_csv(handoff_events, csv_filename)
    fig, ax = plt.subplots(figsize=(12, 12))
    plot_cells(ax, pos, isd)
    plot_path(ax, path, handoff_points)
    plt.show()



if __name__ == "__main__":
    simulation()

