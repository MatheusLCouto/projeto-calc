"""import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.animation import FuncAnimation

# Criar a figura e o objeto de projeção do globo terrestre
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Configurar a projeção do globo terrestre
map = Basemap(ax=ax)

# Função para atualizar o plot a cada quadro da animação
def update(frame):
    ax.cla()  # Limpar o plot anterior

    # Plot do globo terrestre
    map.drawcoastlines()
    map.drawcountries()

    # Plot das órbitas dos satélites
    for satellite in satellites:
        # Calcular as coordenadas (latitude, longitude) da órbita para o tempo atual
        lat, lon = calculateCoordinates(satellite, frame)

        # Converter as coordenadas para a projeção do mapa
        x, y = map(lon, lat)

        # Plotar a órbita do satélite
        ax.plot(x, y, zs=0, linewidth=1, color='red')

    # Configurações adicionais do plot
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Altitude')
    ax.set_title('Órbitas dos Satélites')

# Função para calcular as coordenadas (latitude, longitude) da órbita para um dado tempo
def calculateCoordinates(satellite, time):
    # Implemente a lógica para calcular as coordenadas da órbita do satélite aqui
    # Use os parâmetros do satélite e o tempo fornecido para calcular as coordenadas

    # Exemplo de retorno de coordenadas aleatórias
    lat = np.random.uniform(-90, 90, 100)
    lon = np.random.uniform(-180, 180, 100)

    return lat, lon

# Lista de satélites
satellites = ['Satélite 1']  # Adicione os satélites desejados aqui

# Criar a animação
animation = FuncAnimation(fig, update, frames = 100, interval=200)

# Exibir a animação
plt.show()
"""
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import math

def plot_earth_and_satellites(n):
  
  # Create a figure and an axes object.
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  # Plot the Earth.
  earth = plt.Circle((-90.0, 90.0), radius=6371, alpha = 0.5, do_3d_animation = True)
  ax.add_artist(earth)

  # Plot the satellites.
  for i in range(n):
    satellite = plt.Circle((-170.0, 170.0), radius=100, alpha = 0.5, do_3d_animation = True)
    ax.add_artist(satellite)

  # Animate the satellites orbiting the Earth.
  def animate(i):
    for satellite in ax.get_children():
      satellite.center = (
          math.cos(i * 0.1), math.sin(i * 0.1), 0)

  ani = FuncAnimation(fig, animate, interval=1000)
  plt.show()

if __name__ == "__main__":
  # Plot 5 satellites orbiting the Earth.
  plot_earth_and_satellites(5)

"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import numpy as np
import datetime

# Função para plotar o globo terrestre
def plot_globo_terrestre():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Carregar os dados do globo terrestre
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 6371 * np.outer(np.cos(u), np.sin(v))
    y = 6371 * np.outer(np.sin(u), np.sin(v))
    z = 6371 * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plotar o globo terrestre
    ax.plot_surface(x, y, z, color='b')

    # Configurar os limites do gráfico
    ax.set_xlim([-7000, 7000])
    ax.set_ylim([-7000, 7000])
    ax.set_zlim([-7000, 7000])

    return fig, ax

# Função para plotar os satélites em uma determinada data e hora
def plotar_satelites(ax, data_hora):
    # Exemplo de coordenadas de satélite (para demonstração)
    latitudes = [0, 30, 60, -30, -60]
    longitudes = [0, 45, 90, -45, -90]

    # Converter a data e hora para um objeto datetime
    data_hora_obj = datetime.datetime.strptime(data_hora, "%Y-%m-%d %H:%M:%S")

    # Plotar cada satélite
    for lat, lon in zip(latitudes, longitudes):
        # Converter as coordenadas para coordenadas esféricas
        theta = np.deg2rad(90 - lat)
        phi = np.deg2rad(lon)

        # Converter as coordenadas esféricas para coordenadas cartesianas
        x = 6871 * np.sin(theta) * np.cos(phi)
        y = 6871 * np.sin(theta) * np.sin(phi)
        z = 6871 * np.cos(theta)

        # Plotar o satélite
        ax.plot([x], [y], [z], marker='o', markersize=5, color='r')

    return ax

# Função para criar os frames do gráfico
def criar_frames(ax, data_horas):
    frames = []
    for data_hora in data_horas:
        fig_copy, ax_copy = plot_globo_terrestre()
        ax_copy = plotar_satelites(ax_copy, data_hora)
        frames.append(fig_copy)

    return frames

# Exemplo de lista de data e horas para os frames
data_horas = [
    "2023-06-02 12:00:00",
    "2023-06-02 12:15:00",
    "2023-06-02 12:30:00",
    "2023-06-02 12:45:00",
    "2023-06-02 13:00:00"
]

# Plotar o globo terrestre inicial
fig, ax = plot_globo_terrestre()

# Criar os frames para cada data e hora
frames = criar_frames(ax, data_horas)
print(frames)

# Criar a animação
animat = FuncAnimation(fig, ax, frames, interval=200, blit=False, repeat_delay=1000)

# Exibir a animação
plt.show()
