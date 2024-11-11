import numpy as np
import matplotlib.pyplot as plt
import math
import csv
from matplotlib.path import Path
import random
from shapely.geometry import Polygon as ShapelyPolygon, Point
import pointpats
import matplotlib.animation as animation
from matplotlib.patches import RegularPolygon, Polygon as MplPolygon

# ================================
# Configuration and Parameters
# ================================

minSpeed = 1    # m/s
maxSpeed = 15   # m/s
minT = 1        # s
maxT = 6        # s

# Simulation Parameters
map_x_min = -1500
map_x_max = 1500
map_y_min = -1500
map_y_max = 1500
map_size_x = map_x_max - map_x_min
map_size_y = map_y_max - map_y_min

Ttotal = 900
T = 300
bandwidth = 10**7
P_t_dbm = 33
P_t = 10**((P_t_dbm - 30) / 10)
P_m_dbm = 23
P_m = 10**((P_m_dbm-30)/10)
h_bs = 51.5
h_md=1.5
G_t_db = 14
G_r_db = 14
G_t = 10**(14/10)
G_r = 10**(14/10)
k=1.38*(10**-23)

P_noise = k * T * bandwidth

# SINR Threshold for Handoff
SINR_threshold_dB = 10  # in dB

a = -250/3**0.5
b = 250
isd = 500
pos= [(0, 0),
     (0, isd),
     (0, -isd),
     (isd * np.sqrt(3) / 2, isd / 2),

      (-isd * np.sqrt(3) / 2, -isd / 2),
      (-isd * np.sqrt(3) / 2, isd / 2),
      (isd * np.sqrt(3) / 2, -isd / 2),
      
      (isd * np.sqrt(3), isd),
      (isd * np.sqrt(3), 0),
      (isd * np.sqrt(3), -isd),
      
      (isd * np.sqrt(3) / 2, -3 * isd / 2),
      (0, -2 * isd),
      
      (-isd * np.sqrt(3) / 2, -3 * isd / 2),
      (-isd * np.sqrt(3), -isd),
      (-isd * np.sqrt(3), 0),
      (-isd * np.sqrt(3), isd),
      (-isd * np.sqrt(3) / 2, 3 * isd / 2),
      (0, 2 * isd),
      (isd * np.sqrt(3) / 2, 3 * isd / 2)]
      

      
      

    
    
outsidecell = [
      (isd * np.sqrt(3)*1.5, isd*1.5),
      (isd * np.sqrt(3)*1.5, isd/2),
      (isd * np.sqrt(3)*1.5, -isd/2),
      (isd * np.sqrt(3)*1.5, -3*isd/2),
      (isd * np.sqrt(3), -2*isd),
      
      (isd * np.sqrt(3) / 2, -5 * isd / 2),
      
      (0, -3 * isd),
      
      (-isd * np.sqrt(3) / 2, -5 * isd / 2),
      (-isd * np.sqrt(3), -2*isd),
      
      (-isd * np.sqrt(3)*1.5, -3*isd/2),
      (-isd * np.sqrt(3)*1.5, -isd/2),
      (-isd * np.sqrt(3)*1.5, isd/2),
      (-isd * np.sqrt(3)*1.5, 3*isd/2),
      
      
      (-isd * np.sqrt(3), 2*isd),
      (-isd * np.sqrt(3) / 2, 5 * isd / 2),
      (0, 3 * isd),
      
      
      (isd * np.sqrt(3) / 2, 5 * isd / 2),
      (isd * np.sqrt(3), 2*isd),
      ]

id = [
        12,
        16,
        15,
        14,
        18,
        17,
        16,
        8,
        19,
        18,
        10,
        9,
        8,
        12,
        11,
        10,
        14,
        13
      ]
      
      
      
      
      
      
      
      
      
allcell = pos+outsidecell


NUM_CELLS = len(pos)

csv_filename = 'handoff_events_bonus.csv'

def plot_cells(ax, bs_positions, isd):
    side_length = isd / math.sqrt(3)
    for idx, bs in enumerate(bs_positions, start=1):
        if idx>19:
            idx = id[idx-20]
            
            
            
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
    ax.set_xlim(map_x_min - buffer, map_x_max + buffer)
    ax.set_ylim(map_y_min - buffer, map_y_max + buffer)

    ax.set_title('19-Cell with their id')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_aspect('equal')
    ax.grid(True)
fig, ax = plt.subplots(figsize=(12, 12))

# ================================
# bonus 1
# ================================
plot_cells(ax,allcell,isd)
#plt.show()
# ================================
# bonus 1
# ================================


def generate_uniform_point(polygon):
    min_x, min_y, max_x, max_y = polygon.bounds
    while True:
        random_x = np.random.uniform(min_x, max_x)
        random_y = np.random.uniform(min_y, max_y)
        random_point = Point(random_x, random_y)
        if polygon.contains(random_point):
            return (random_x, random_y)

devices = []
def plot_points(ax, bs_positions, isd, a, b):
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
        # Label the base station
        ax.text(bs[0], bs[1], str(idx), color='blue', fontsize=10,
                ha='center', va='center', fontweight='bold')
    tempid = np.random.randint(0, len(bs_positions))
    BSx, BSy = bs_positions[tempid]
    coords = [
        (BSx + a, BSy + b),
        (BSx - a, BSy + b),
        (BSx - 2 * a, BSy),
        (BSx - a, BSy - b),
        (BSx + a, BSy - b),
        (BSx + 2 * a, BSy)
    ]
    pgon = ShapelyPolygon(coords)  # 使用 Shapely 的 Polygon
    x_poly, y_poly = pgon.exterior.xy
    ax.plot(x_poly, y_poly, color='blue', linestyle='-', linewidth=1)
    x, y = generate_uniform_point(pgon)
    ax.scatter(x, y, color='red')
    devices.append((x,y))

# ================================
# bonus 2
# ================================
for i in range(100):
    plot_points(ax,pos,isd,a,b)
plt.show()
# ================================
# bonus 2
# ================================


def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_received_power(bs_position, md_position):
    d = distance(bs_position, md_position)
    P_received = P_m*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4)
    return P_received

def calculate_SINR(md_position, serving_bs_id, bs_positions, devices):
    P_signal = calculate_received_power(bs_positions[serving_bs_id - 1], md_position)
    P_interference = 0
    for device in devices:
        if device != md_position:
            P_interference += calculate_received_power(bs_positions[serving_bs_id - 1], md_position) + P_noise

    SINR_linear = P_signal / (P_interference)
    SINR_dB = 10 * math.log10(SINR_linear)
    return SINR_linear

def generate_movement():
    theta = np.random.uniform(0, 2 * np.pi)
    v = np.random.uniform(minSpeed, maxSpeed)
    t = np.random.randint(minT, maxT)
    return [theta, v, t]



def checknearestcell(allcell , id , md_position):
    temp = float('inf')
    for q in range(len(allcell)):
        if temp> distance(md_position,allcell[q]):
            temp = distance(md_position,allcell[q])
            idtemp = q
    return idtemp

def checkconnectcell(bs_positions , md_position,devices):
    tempSINR = -float('inf')
    connectcell = 1
    for q in range(len(bs_positions)):
        if tempSINR < calculate_SINR(md_position,q+1,bs_positions, devices ):
            tempSINR = calculate_SINR(md_position,q+1,bs_positions, devices )
            connectcell = q+1
    return connectcell






info = [ [0,0,0,0,0] for _ in range(len(devices)) ]
for i in range(len(devices)):
    info[i][3] = checknearestcell(allcell , id , devices[i])

for i in range(len(devices)):
    info[i][4] = checkconnectcell(pos , devices[i] , devices)

#print(info)

handoff_events = []
def simulation_step(current_time):
    for i in range(len(devices)):
        x, y = devices[i]
        theta, v, t, bsid , connectid= info[i]
        if t == 0:
            q = generate_movement()
            theta, v, t = q
        new_x = x + v * np.cos(theta)
        new_y = y + v * np.sin(theta)
        
        devices[i] = (new_x, new_y)
        idtemp = checknearestcell(allcell, id , devices[i])
        if idtemp >= 19 :
            bs_x , bs_y = outsidecell[idtemp-19]
            devices[i] = (new_x - bs_x + pos[id[idtemp-19]-1][0] , new_y - bs_y + pos[id[idtemp-19]-1][1])
            bsid = id[idtemp-20]
            
        tempconnectbs = checkconnectcell(pos , devices[i] , devices)
        if tempconnectbs != connectid:
            connectid = tempconnectbs
            handoff_event = {
                'time': current_time,
                'device_id': i,
                'source': connectid,
                'destination': tempconnectbs
            }
            handoff_events.append(handoff_event)
   #         print(f"Handoff: Device {i} from {connectid} to {tempconnectbs} at time {current_time}s")
        
        info[i] = [theta, v, t-1, bsid,connectid]


def save_handoff_events_to_csv(handoff_events, filename):
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ['Time (s)', 'Device ID', 'Source Cell ID', 'Destination Cell ID']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for event in handoff_events:
            writer.writerow({
                'Time (s)': f"{event['time']}s",
                'Device ID': event['device_id'],
                'Source Cell ID': event['source'],
                'Destination Cell ID': event['destination']
            })
    print(f"\nHandoff events have been saved to '{filename}'.")
    print(f"there are {len(handoff_events)} times of handoff")
    
    
    
    
    
    

# ================================
# Animation
# ================================
fig, ax = plt.subplots(figsize=(12, 12))
plot_cells(ax, pos, isd)


scatter = ax.scatter([device[0] for device in devices],
                     [device[1] for device in devices],
                     c='red', s=30, label='Devices')

time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12,
                    verticalalignment='top')

ax.legend()

def animate_func(frame_num, devices, scatter, pos, ax, time_text):
    simulation_step(frame_num)
    scatter.set_offsets(devices)
    
    current_time = frame_num
    time_text.set_text(f'Current Time: {current_time} s')
    
    ax.set_title('simulation')
    return scatter, time_text


ani = animation.FuncAnimation(
    fig,
    animate_func,
    fargs=(devices, scatter, pos, ax, time_text),
    frames=Ttotal,
    interval=50,
    blit=False,
    repeat=False
)

plt.show()

# ================================
# Animation
# ================================


save_handoff_events_to_csv(handoff_events, csv_filename)
