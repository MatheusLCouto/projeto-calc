import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def convert_coordinates(x, y, z):
    # Raio médio da Terra em quilômetros
    R = 6371

    # Ajustar as coordenadas para o sistema de coordenadas centrado na Terra
    y_prime = x
    z_prime = -y
    x_prime = z

    # Converter coordenadas geocêntricas para latitude, longitude e altitude
    latitude = math.degrees(math.asin(z_prime / (R + z_prime)))
    longitude = math.degrees(math.atan2(y_prime, x_prime))
    altitude = math.sqrt(x_prime ** 2 + y_prime ** 2 + z_prime ** 2) - R

    return longitude, latitude, altitude


def plot_earth(longitude, latitude, altitude):
    # Criação da figura e do subplot 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Criação da esfera que representa a Terra
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_earth = np.outer(np.cos(u), np.sin(v))
    y_earth = np.outer(np.sin(u), np.sin(v))
    z_earth = np.outer(np.ones(np.size(u)), np.cos(v))

    # Plotagem da esfera
    ax.plot_surface(x_earth, y_earth, z_earth, color='b', alpha=0.2)

    # Plotagem do ponto fornecido
    ax.scatter(longitude, latitude, altitude, color='r', label='Ponto')
    ax.text(longitude, latitude, altitude, '(%.2f, %.2f, %.2f)' % (longitude, latitude, altitude), fontsize=8)

    # Configurações adicionais do gráfico
    ax.set_xlim([-180, 180])
    ax.set_ylim([-90, 90])
    ax.set_zlim([-6371, 6371])
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Altitude')

    # Mostrar o gráfico
    plt.legend()
    plt.autoscale()
    plt.show()


# Coordenadas cartesianas do ponto
x = 0.789
y = -0.453
z = 0.312

# Conversão para coordenadas de longitude, latitude e altitude
longitude, latitude, altitude = convert_coordinates(x, y, z)

# Plotagem no gráfico de globo terrestre
plot_earth(longitude, latitude, altitude)
