import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import pointpats
  

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
# 1-1

a = -250/3**0.5
b = 250

# 1-1
coords = [[a,b],[-a,b],[-2*a,0],[-a,-b],[a,-b],[2*a,0],]
pgon = Polygon(coords)
points = pointpats.random.poisson(pgon, size=50)
x_points = [point[0] for point in points]
y_points = [point[1] for point in points]
x_pgon, y_pgon = pgon.exterior.xy
plt.plot(x_pgon, y_pgon, color='blue', linewidth=2, label="cell")
plt.scatter(0, 0, color='green',label="central BS")
plt.scatter(x_points, y_points, color='red', label="mobile device")
plt.xlabel('X-axis(m)')
plt.ylabel('Y-axis(m)')
plt.title('random distributed mobile devices in the central cell')
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

#1-2
dlist = []
gainp = []
for i,j in zip(x_points,y_points):
    d= (i**2+j**2)**0.5
    dlist += [d]
    gainp += [10 * np.log10(P_t*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4))]

#Pr = P_t*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4)
plt.scatter(dlist, gainp, color='blue')
plt.xlabel("Distance (m)")
plt.ylabel("Received Power (dB)")
plt.title("Received Power (Only consider path loss)vs Distance")
plt.show()

#1-3

gainSINR = []
thermal_noise=T*bandwidth*k
bslistx = [0,250*(3**0.5),250*(3**0.5),0,-250*(3**0.5),-250*(3**0.5)]
bslisty = [500,250,-250,-500,-250,250]

for i,j in zip(x_points,y_points):
    intfere = 0
    for k,z in zip(bslistx,bslisty):
            d= ((i-k)**2+(z-j)**2)**0.5
            intfere += P_t*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4)
    d = (i**2+j**2)**0.5
    intfere += thermal_noise
    gainSINR += [10 * np.log10(P_t*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4))-10 * np.log10(intfere)]
    
plt.scatter(dlist, gainSINR, color='blue')
plt.xlabel("Distance (m)")
plt.ylabel("SINR (dB)")
plt.title("SINR vs Distance")
plt.show()








# 2-1
coords = [[a,b],[-a,b],[-2*a,0],[-a,-b],[a,-b],[2*a,0],]
pgon = Polygon(coords)
points = pointpats.random.poisson(pgon, size=50)
x_points = [point[0] for point in points]
y_points = [point[1] for point in points]
x_pgon, y_pgon = pgon.exterior.xy
plt.plot(x_pgon, y_pgon, color='blue', linewidth=2, label="cell")
plt.scatter(0, 0, color='green',label="central BS")
plt.scatter(x_points, y_points, color='red', label="mobile device")
plt.xlabel('X-axis(m)')
plt.ylabel('Y-axis(m)')
plt.title('random distributed mobile devices in the central cell')
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()


#2-2
dlist = []
gaindb = []
for i,j in zip(x_points,y_points):
    d= (i**2+j**2)**0.5
    dlist += [d]
    gaindb += [10 * np.log10(P_m*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4))]

#Pr = P_t*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4)
plt.scatter(dlist, gaindb, color='blue')
plt.xlabel("Distance (m)")
plt.ylabel("Received Power of the central BS (dB)")
plt.title("Received Power of the central BS (Only consider path loss)vs Distance")
plt.show()


#2-3


intfere=[]
SINRP = []
gainp = [10**(e/10) for e in gaindb]
sumgainp = sum(gainp)
for i in range(len(x_points)):
    intfere+=[10*np.log10(sumgainp-gainp[i]+thermal_noise)]
    SINRP+=[gaindb[i]-intfere[i]]
    
    
plt.scatter(dlist, SINRP, color='blue')
plt.xlabel("Distance (m)")
plt.ylabel("Received Power of the central BS (dB)")
plt.title("SINR of the central BS vs Distance")
plt.show()




#bonus
isd = 500
pos= [(0, 0),(0, isd),(0, -isd),(isd * np.sqrt(3) / 2, isd / 2),(-isd * np.sqrt(3) / 2, -isd / 2),(-isd * np.sqrt(3) / 2, isd / 2),(isd * np.sqrt(3) / 2, -isd / 2),(isd * np.sqrt(3), 0),(-isd * np.sqrt(3), 0),(isd * np.sqrt(3), isd),(-isd * np.sqrt(3), isd),(isd * np.sqrt(3), -isd),(-isd * np.sqrt(3), -isd),(isd * np.sqrt(3) / 2, 3 * isd / 2),(-isd * np.sqrt(3) / 2, 3 * isd / 2),(isd * np.sqrt(3) / 2, -3 * isd / 2),(-isd * np.sqrt(3) / 2, -3 * isd / 2),(0, 2 * isd),(0, -2 * isd)]
BSx = 0
BSy = 0

central_bs_label = True
cell_label = True
mobile_device_label = True
xbonus = []
ybonus = []
for i in range(19):
    BSx = pos[i][0]
    BSy = pos[i][1]
    coords = [[BSx+a,BSy+b],[BSx-a,BSy+b],[BSx-2*a,BSy],[BSx-a,BSy-b],[BSx+a,BSy-b],[BSx+2*a,BSy],]
    pgon = Polygon(coords)
    points = pointpats.random.poisson(pgon, size=50)
    x_points = [point[0] for point in points]
    y_points = [point[1] for point in points]
    xbonus += [x_points]
    ybonus += [y_points]
    x_pgon, y_pgon = pgon.exterior.xy
    plt.plot(x_pgon, y_pgon, color='blue', linewidth=2, label="cell" if cell_label else "")
    cell_label = False
    plt.scatter(BSx, BSy, color='green', label="central BS" if central_bs_label else "" , s =10)
    central_bs_label = False
    plt.scatter(x_points, y_points, color='red', label="mobile device" if mobile_device_label else "", s= 5)
    mobile_device_label = False

plt.xlabel('X-axis(m)')
plt.ylabel('Y-axis(m)')
plt.title('random distributed mobile devices in an urban area')
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig('figure1.png')
plt.show()



#bonus2

bonusdlist = []
bonusgainp = []
#bonusRP = []
for k in range(len(pos)):
    for i in range(len(pos)):
     #   bonusRP += [[]]
        for j in range(50):
            d= ((xbonus[i][j]-pos[k][0])**2+(ybonus[i][j]-pos[k][1])**2)**0.5
            bonusdlist += [d]
            bonusgainp += [10 * np.log10(P_m*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4))]
        #    bonusRP[i] += [10 * np.log10(P_m*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4))]
    plt.scatter(bonusdlist[950*k:950*(k+1)], bonusgainp[950*k:950*(k+1)], color='blue', label = f"[BS{pos[k]}]")
    plt.xlabel("Distance (m)")
    plt.ylabel("Received Power (dB)")
    plt.title(f"Received Power (Only consider path loss)vs Distance")
    plt.legend()
    plt.savefig(f"figure{k+2}.png")
    plt.show()



#bonus3
dlistb3 = []
bonusintfere=[]
bonusSINRP = []
gainp = [10**(e/10) for e in gaindb]
sumgainp = sum(gainp)
for i in range(len(pos)):
    dlistb3 = []
    bonusintfere=[]
    bonusSINRP += [[]]
    for j in range(len(pos)):
        for k in range(50):
            d= ((xbonus[j][k]-pos[i][0])**2+(ybonus[j][k]-pos[i][1])**2)**0.5
            dlistb3 += [d]
            bonusintfere += [(P_m*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4))+thermal_noise]
    
    intf = sum(bonusintfere)
    
    for w in range(950):
        #print(intf, 10**(bonusgainp[19*i+z]/10) )
            bonusSINRP[i]+=[bonusgainp[950*i+w]- 10*np.log10(intf-10**(bonusgainp[950*i+w]/10))]
   # print(bonusSINRP[i])
    rgb = (np.random.random(), np.random.random(), np.random.random())
  #  print(len(bonusdlist[19*i:19*i+50]),intf)
    plt.scatter(bonusdlist[950*i:950*(i+1)], bonusSINRP[i],
                c='green', label=f"BS{pos[i]}", s = 50)
    plt.xlabel("Distance(m)")
    plt.ylabel("SINR of the BS(dB)")
    plt.title("SINR of the BS vs Distance")
  #  plt.savefig(f"figure{i+21}.png")
    plt.legend()
    plt.savefig(f"figure{i+21}.png")
    plt.show()
