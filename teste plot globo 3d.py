import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# criação de uma figura em 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# carregamento dos dados de latitude e longitude
lat, lon = np.loadtxt('lat_lon.txt', unpack=True)

# conversão de graus para radianos
lat_rad = np.radians(lat)
lon_rad = np.radians(lon)

# cálculo das coordenadas cartesianas
R = 6371  # raio da Terra em km
x = R * np.cos(lat_rad) * np.cos(lon_rad)
y = R * np.cos(lat_rad) * np.sin(lon_rad)
z = R * np.sin(lat_rad)

# plotagem do globo
ax.scatter(x, y, z, c=z, cmap='Blues_r')

# ajuste dos limites do eixo z
ax.set_zlim(-R, R)

# exibição do gráfico
plt.show()
