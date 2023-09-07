import string
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Constantes
G = 6.67430e-11  # Constante gravitacional
r_earth = 6.371e6  # Raio da Terra
m_earth = 5.972e24  # Massa da Terra

# Parâmetros dos satélites
n_satellites = 3
satellites = []
colors = ["red", "blue", "green"]

# Parâmetros temporais para a simulação
t_max = 3600  # segundos
dt = 1  # segundos
t = np.arange(0, t_max + dt, dt)

for i in range(n_satellites):
    # Posição inicial aleatória em latitude e longitude
    lat = np.random.uniform(-90, 90)
    lon = np.random.uniform(-180, 180)
    r = r_earth + 1000 * np.random.uniform(200, 400)
    x = r * np.cos(np.radians(lat)) * np.cos(np.radians(lon))
    y = r * np.cos(np.radians(lat)) * np.sin(np.radians(lon))
    z = r * np.sin(np.radians(lat))

    # Velocidade inicial aleatória
    v = np.sqrt(G * m_earth / r)
    theta_v = np.random.uniform(0, 2 * np.pi)
    phi_v = np.arccos(np.random.uniform(-1, 1))
    vx = v * np.sin(phi_v) * np.cos(theta_v)
    vy = v * np.sin(phi_v) * np.sin(theta_v)
    vz = v * np.cos(phi_v)

    # Massa e área frontal
    m = np.random.uniform(1, 100)
    A = np.random.uniform(0.01, 10)

    satellites.append({
        "r": np.array([x, y, z]),  # posição
        "v": np.array([vx, vy, vz]),  # velocidade
        "m": m,  # massa
        "A": A,  # área frontal
        "color": colors[i]  # cor
    })
    print(f"satelite {i}")
    satelliteAtual = satellites[i]
    r_Satellites = satelliteAtual["r"]
    m_Satellites = satelliteAtual["m"]
    v_Satellites = satelliteAtual["A"]
    color_Satellites = satelliteAtual["color"]
    print(r_Satellites, m_Satellites, v_Satellites, color_Satellites, "\n")


"""print(satellites[1])
primeiro_satelite = satellites[0]
r_primeiro_satelite = primeiro_satelite["r"]

print(r_primeiro_satelite)"""



def gravitational_force(satellite, satellites):
    force = np.zeros(3)
    print(force)
    # Força gravitacional da Terra
    r_satellite = satellite["r"]
    print(r_satellite)
    distance_to_earth = np.linalg.norm(r_satellite)
    print(distance_to_earth)
    force += -G * m_earth * satellite["m"] / distance_to_earth ** 3 * r_satellite
    print(force)
    """# Força gravitacional dos outros satélites
    for other_satellite in satellites:
        if other_satellite is not satellite:
            r_other_satellite = other_satellite["r"]
            distance_between_satellites = np.linalg.norm(r_satellite - r_other_satellite)
            force += -G * satellite["m"] * other_satellite["m"] / distance_between_satellites ** 3 * (r_satellite - r_other_satellite)
"""
    return force

gravitational_force(satellites[0], n_satellites)

"""

def update_satellite(satellite, satellites, dt):
    r = satellite["r"]
    v = satellite["v"]
    m = satellite["m"]

    # Calcular força gravitacional
    force = gravitational_force(satellite, satellites)

    # Atualizar posição e velocidade usando o método de Newton
    r_new = r + v * dt
    v_new = v + force / m * dt

    # Atualizar satélite com nova posição e velocidade
    satellite["r"] = r_new
    satellite["v"] = v_new

# Loop para atualizar a posição e velocidade dos satélites
for t in np.arange(0, T, dt):
    # Atualiza a posição e velocidade dos satélites
    for satellite in satellites:
        # Calcula a força resultante no satélite
        f_res = np.array([0., 0., 0.])
        for other_satellite in satellites:
            if other_satellite != satellite:
                f_res += gravitational_force(satellite["m"], other_satellite["m"])

        # Atualiza a velocidade do satélite usando o método de Newton
        satellite["v"] += f_res * dt / satellite["m"]

        # Atualiza a posição do satélite usando o método de Newton
        satellite["r"] += satellite["v"] * dt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = r_earth * np.cos(u)*np.sin(v)
y = r_earth * np.sin(u)*np.sin(v)
z = r_earth * np.cos(v)
ax.plot_wireframe(x, y, z, color='gray', alpha=0.1)

for satellite in satellites:
    ax.scatter(satellite['r'][0], satellite['r'][1], satellite['r'][2], color=satellite['color'], s=10)

for t in range(n_steps):
    for i, satellite in enumerate(satellites):
        # calcular a força resultante no satélite usando o método de Newton
        F = np.zeros(3)
        for j, other_satellite in enumerate(satellites):
            if i != j:
                F += gravitational_force(satellite, other_satellite)

        # atualizar a posição e velocidade do satélite usando o método de Newton
        a = F / satellite['m']
        update_satellite(satellite["r"], satellites["r"], dt)

    # plotar a nova posição dos satélites na figura
    for satellite in satellites:
        ax.scatter(satellite['r'][0], satellite['r'][1], satellite['r'][2], color=satellite['color'], s=10)

    # atualizar a figura
    plt.draw()
    plt.pause(0.01)
    ax.clear()
    ax.set_aspect('equal')
    ax.plot_wireframe(x, y, z, color='gray', alpha=0.1)
"""