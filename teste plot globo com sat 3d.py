import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

R = 8000 # raio da órbita em km
# função que retorna as coordenadas cartesianas da Terra
def get_earth_coordinates():
    lat, lon = np.mgrid[-90:91:0.5, -180:181:0.5]
    R = 6371  # raio da Terra em km
    x = R * np.cos(np.radians(lat)) * np.cos(np.radians(lon))
    y = R * np.cos(np.radians(lat)) * np.sin(np.radians(lon))
    z = R * np.sin(np.radians(lat))
    print("1º R: ", R)
    #print(x, y, z)
    return x, y, z

# função que simula a trajetória de um satélite em órbita
def simulate_satellite_orbit(theta):
    raioOrb = R + 545
    print("2º R: ", R)
    T = 2 * np.pi * np.sqrt(raioOrb**3 / (G * M))  # período da órbita em segundos
    x = (raioOrb-1000) * np.cos(theta)
    y = (raioOrb-500) * np.sin(theta)
    z = 0
    vx = 20
    vy = np.sqrt(G * M / raioOrb)
    vz = 170
    dt = 60  # intervalo de tempo em segundos
    for t in range(int(T/dt)):
        r = np.sqrt(x**2 + y**2 + z**2)
        ax = -G * M * x / r**3
        ay = -G * M * y / r**3
        az = -G * M * z / r**3
        vx += ax * dt
        vy += ay * dt
        vz += az * dt
        x += vx * dt
        y += vy * dt
        z += vz * dt

    print("x = ", x, "\n\ny = ", y, "\n\nz = ", z)
    return x, y, z

"""def simulate_satellite_orbit_2(theta):
    R = 7000
    print("3º R: ", R)
    T = 2 * np.pi * np.sqrt(R**3 / (G * M))  # período da órbita em segundos
    x = (R+1000) * np.cos(theta)
    y = (R+500) * np.sin(theta)
    z = 2500
    vx = 20
    vy = np.sqrt(G * M / R)
    vz = 170
    dt = 60  # intervalo de tempo em segundos
    for t in range(int(T/dt)):
        r = np.sqrt(x**2 + y**2 + z**2)
        ax = -G * M * x / r**3
        ay = -G * M * y / r**3
        az = -G * M * z / r**3
        vx += ax * dt
        vy += ay * dt
        vz += az * dt
        x += vx * dt
        y += vy * dt
        z += vz * dt
    return x, y, z

def simulate_satellite_orbit_3(theta):
    R = 7000
    print("4º R: ", R)
    T = 2 * np.pi * np.sqrt(R**3 / (G * M))  # período da órbita em segundos
    x = (R) * np.cos(theta)
    y = (R) * np.sin(theta)
    z = 0
    vx = 20
    vy = np.sqrt(G * M / R)
    vz = 170
    dt = 60  # intervalo de tempo em segundos
    for t in range(int(T/dt)):
        r = np.sqrt(x**2 + y**2 + z**2)
        ax = -G * M * x / r**3
        ay = -G * M * y / r**3
        az = -G * M * z / r**3
        vx += ax * dt
        vy += ay * dt
        vz += az * dt
        x += vx * dt
        y += vy * dt
        z += vz * dt
    return x, y, z
"""
# constantes físicas
G = 6.674e-11  # constante gravitacional em m^3/kg/s^2
M = 5.97e24  # massa da Terra em kg

# criação da figura em 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# plotagem do globo terrestre
x, y, z = get_earth_coordinates()
ax.plot_surface(x, y, z, cmap='Blues')

# simulação da trajetória do  primeiro satélite
theta = np.linspace(0, 2*np.pi, 1000)
x_sat, y_sat, z_sat = simulate_satellite_orbit(theta)
#print(x_sat, "\n\n", y_sat, "\n\n", z_sat)
ax.plot(x_sat, y_sat, z_sat, color='r')
"""
# simulação da trajetória do segundo satélite
x_sat_2, y_sat_2, z_sat_2 = simulate_satellite_orbit_2(theta)
# plotagem da trajetória do segundo satélite
ax.plot(x_sat_2, y_sat_2, z_sat_2, color='g')

# simulação da trajetória do terceiro satélite
x_sat_3, y_sat_3, z_sat_3 = simulate_satellite_orbit_3(theta)

# plotagem da trajetória do terceiro satélite
ax.plot(x_sat_3, y_sat_3, z_sat_3, color='y')
"""
# plotagem da trajetória do satélite


#R = 8000000
# ajuste dos limites do eixo z
ax.set_xlim(-100 * R, 100 * R)
ax.set_ylim(-100 * R, 100 * R)
ax.set_zlim(-900 * R, 900 * R)
plt.autoscale()
# exibição do gráfico
plt.show()
