import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skyfield.api import Topos, load
import numpy as np
from datetime import datetime, timedelta
from pyorbital.orbital import Orbital

# Função para processar as informações do TLE e obter as coordenadas orbitais
def processar_tle(line1, line2):
    ts = load.timescale()
    t = ts.utc(2023, 1, range(1, 366))

    orb = Orbital(satellite_names[0], line1=line1, line2=line2)
    print(orb.tle)
    posLatLongAlt = orb.get_lonlatalt("2023-01-01 07:49:40")
    lat = posLatLongAlt[0]
    lon = posLatLongAlt[1]
    alt = posLatLongAlt[2]

    return lon, lat, alt

# Abrir o arquivo TLE
with open('tle.txt', 'r') as file:
    lines = file.readlines()

# Listas para armazenar os dados
satellite_names = []
line1s = []
line2s = []
xCords = []
yCords = []
zCords = []

# Percorrer as linhas do arquivo e extrair as informações relevantes
for i in range(0, len(lines), 3):
    satellite_names.append(lines[i].strip())
    line1s.append(lines[i + 1].strip())
    line2s.append(lines[i + 2].strip())

# Configuração do gráfico
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-8000, 8000])
ax.set_ylim([-8000, 8000])
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Altitude (km)')

# Plotar o globo terrestre
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 6371 * np.outer(np.cos(u), np.sin(v))
y = 6371 * np.outer(np.sin(u), np.sin(v))
z = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, color='b', alpha=0.3)

# Plotar a trajetória de cada satélite
for i in range(len(satellite_names)):
    line1 = line1s[i]
    line2 = line2s[i]

    subpoint_longitude, subpoint_latitude, altitude = processar_tle(line1, line2)
    altitude += 6371

    xCords.append(subpoint_longitude)
    yCords.append(subpoint_latitude)
    zCords.append(altitude)

ax.plot(xCords, yCords, zCords, color='r', alpha=1)
ax.set_title('Órbita do Satélite')

# Exibir o gráfico
plt.show()
