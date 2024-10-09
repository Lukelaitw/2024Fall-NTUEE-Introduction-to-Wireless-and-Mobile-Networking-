import numpy as np
import matplotlib.pyplot as plt


T = 300#K
bandwidth = 10**7
P_t_dbm = 33
P_t = 10**((P_t_dbm - 30) / 10)
h_bs = 51.5
h_md=1.5
G_t_db = 14
G_r_db = 14
G_t = 10**(14/10)
G_r = 10**(14/10)
k=1.38*(10**-23)

d = np.linspace(0.1, 3000, 10000)
#1-1
Pr = P_t*(G_t*G_r*(h_bs**2)*(h_md**2))/(d**4)
Pr_db = 10 * np.log10(Pr)


plt.figure(figsize=(10, 6))
plt.plot(d, Pr_db, label="Received Power (dB)")
plt.xlabel("Distance (m)")
plt.ylabel("Received Power (dB)")
plt.title("Received Power vs Distance")
plt.grid(True)
plt.legend()
plt.show()



# 1-2
thermal_noise=T*bandwidth*k
SINR = 10 * np.log10(Pr / thermal_noise)

plt.figure(figsize=(10, 6))
plt.plot(d, SINR, label="SINR (dB)", color='orange')
plt.xlabel("Distance (m)")
plt.ylabel("SINR (dB)")
plt.title("SINR vs Distance")
plt.grid(True)
plt.legend()
plt.show()



#2-1

sigma_db = 6
s = np.random.normal(0, 6, d.shape)
Pr_shadowed_db = Pr_db + s
plt.figure(figsize=(10, 6))
plt.plot(d, Pr_shadowed_db, label="Received Power with Shadowing (dB)")
plt.xlabel("Distance (m)")
plt.ylabel("Received Power (dB)")
plt.title("Received Power vs Distance")
plt.grid(True)
plt.legend()
plt.show()

#2-2

thermal_noise=T*bandwidth*k
SINR_shadowed = Pr_shadowed_db-10 * np.log10(thermal_noise)


plt.figure(figsize=(10, 6))
plt.plot(d, SINR_shadowed, label="SINR (dB)", color='orange')
plt.xlabel("Distance (m)")
plt.ylabel("SINR (dB)")
plt.title("SINR with shadowing vs Distance")
plt.grid(True)
plt.legend()
plt.show()
