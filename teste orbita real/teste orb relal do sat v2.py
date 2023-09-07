"""import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Dados de latitude, longitude e altitude
lat = [126.11766477698698, 126.11766477698698, 126.09978620117651, 126.10285035065877, 126.10285035065877, 126.09678639801436, 126.09678639801436, 126.1435053159169, 126.15960394202322, 126.11505024947535, 126.13898684769777, 126.12143045457235, 126.11594903439216, 126.21696652377736, 126.08847309368366, 126.09600409303842, 126.07714582084135, 126.07714582084135]
lon = [-29.400753131099243, -29.400753131099243, -29.417184370608847, -29.415396618310716, -29.415396618310716, -29.422345096789716, -29.422345096789716, -29.37978020009753, -29.364922224699868, -29.406406028863866, -29.384940773958718, -29.402134769325748, -29.407623911148555, -29.316120410505235, -29.43395834772684, -29.42743969313072, -29.44498882509871, -29.44498882509871]
alt = [555.8062585138567, 555.8062585138567, 555.7924990768336, 555.7241067344305, 555.7241067344305, 555.6281266894632, 555.6281266894632, 555.6410701768475, 555.7375056483799, 555.7305099234856, 555.6015422497138, 555.5158203242416, 555.505330096102, 555.6817907856663, 555.4096960864695, 555.3856991676814, 555.3030124753534, 555.3030124753534]

# Criando o mapa
fig = plt.figure()
ax = fig.add_subplot(111)

# Configurando o mapa
map = Basemap(projection='ortho', lat_0=0, lon_0=0)
map.drawcoastlines()
map.fillcontinents(color='coral', lake_color='aqua')

# Convertendo latitude e longitude para coordenadas do mapa
x, y = map(lon, lat)
print(x, y)

# Plotando os pontos no mapa
map.scatter(x, y, c=alt, cmap='coolwarm', edgecolors='k', linewidths=1, alpha=0.7)

# Adicionando uma barra de cor
cbar = plt.colorbar(label='Altitude')

# Exibindo o mapa
plt.title('Orbita de Satélite')
plt.show()
"""

import math

from matplotlib import pyplot as plt
import numpy as np

"""
def convert_coordinates(latitude, longitude, altitude):
    # Raio médio da Terra em quilômetros
    R = 6371

    # Converter latitude e longitude para radianos
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # Calcular coordenadas geocêntricas
    x_prime = (R + altitude) * math.cos(lat_rad) * math.cos(lon_rad)
    y_prime = (R + altitude) * math.cos(lat_rad) * math.sin(lon_rad)
    z_prime = (R + altitude) * math.sin(lat_rad)

    # Ajustar as coordenadas para o sistema de coordenadas centrado na Terra
    x = y_prime
    y = -z_prime
    z = x_prime

    return x, y, z

# Exemplo de uso
latitude = 126.11766477698698
longitude = -29.40075313109924
altitude = 555.806258513856

xCord, yCord, zCord = [], [], []

x, y, z = convert_coordinates(latitude, longitude, altitude)
xCord.append(x)
yCord.append(y)
zCord.append(z)

print("Coordenadas cartesianas:")
print("x:", x)
print("y:", y)
print("z:", z)
"""
import datetime
from datetime import timedelta
from pyorbital.orbital import Orbital
from skyfield.api import Topos, load
#from orbital import plot

tempoInicial = datetime.datetime(2023, 1, 1, 7, 49, 40)
tempoFinal = tempoInicial + datetime.timedelta(hours=1)
delta_tempo = datetime.timedelta(minutes=5)

def processar_tle(line1, line2, tempoInicial):
    orb = Orbital("STARLINK-1007", line1=line1, line2=line2)
    #print(f"tempo atual: {tempoInicial}\nTempo TLE: {orb.orbit_elements.epoch}")
    posLatLongAlt = orb.get_lonlatalt(tempoInicial)
    lat = posLatLongAlt[1]
    lon = posLatLongAlt[0]
    alt = posLatLongAlt[2]
    print(f"lat: {lat}\tlon: {lon}\talt: {alt}")
    print(f"tempo atual: {tempoInicial}")

    return lat, lon, alt

# Listas para armazenar os dados
satellite_names = []
line1s = []
line2s = []
xCords = []
yCords = []
zCords = []
latTot, lonTot, altTot = [], [], []

# Abrir o arquivo TLE
with open('tle.txt', 'r') as file:
    lines = file.readlines()

def converterCoordenadas(lat, lon, alt):
    raioTerra = 6371.0
    altura = raioTerra + alt
    print(f"lat: {lat}\tlon: {lon}\talt: {alt}")
    # Converter latitude e longitude para radianos
    latRad = math.radians(lat)
    lonRad = math.radians(lon)
    print(f"latrad: {latRad}\tlonrad: {lonRad}")

    # Calcular coordenadas geocêntricas
    x_prime = altura * np.cos(latRad) * np.cos(lonRad)
    y_prime = altura * np.cos(latRad) * np.sin(lonRad)
    z_prime = altura * np.sin(latRad)

    # Ajustar as coordenadas para o sistema de coordenadas centrado na Terra
    a = y_prime
    b = -z_prime
    c = x_prime

    print("coordenadaX: {a}\tcoordenadaY: {b}\tcoordenadaZ: {c}".format(a=a, b=b, c=c))

    return a, b, c

# Percorrer as linhas do arquivo e extrair as informações relevantes
for i in range(0, len(lines)-820, 3):
    #sat = orbital
    satellite_names.append(lines[i].strip())
    line1s.append(lines[i + 1].strip())
    line2s.append(lines[i + 2].strip())
    print(i)
    latS, lonS, altS = processar_tle(lines[i+1], lines[i+2], tempoInicial)
    latTot.append(latS)
    lonTot.append(lonS)
    altTot.append(altS)
    aX, bY, cZ = converterCoordenadas(latS, lonS, altS)
    tempoInicial += delta_tempo
    xCords.append(aX)
    yCords.append(bY)
    zCords.append(cZ)
"""
# TLE do Starlink-1007
tle = ['1 44713U 19074A   23001.33310695  .00000538  00000+0  55037-4 0  9995',
       '2 44713  53.0541   9.1431 0002180  39.3908 320.7239 15.06389052173400']

# Criar objeto Orbital a partir do TLE
orb = Orbital("STARLINK-1007", line1=tle[0], line2=tle[1])
#print(orb)

text = orb.tle
#print(text)

print(f"Horario selecionado: {tempoInicial}", type(tempoInicial))
# Calcular a posição e velocidade no momento atual
pos, vel = orb.get_position(tempoInicial)



# Obtém informações orbitais do satélite
posLatLongAlt = orb.get_lonlatalt(tempoInicial)
lat = posLatLongAlt[0]
long = posLatLongAlt[1]
alt = posLatLongAlt[2]
#teste = orb.get_next_passes(datetime.utcnow(), length = 200, alt = alt, lat = lat, lon = long)
#print(teste)
inclination = orb.orbit_elements.inclination
eccentricity = orb.orbit_elements.excentricity
raan = orb.orbit_elements.right_ascension
arg_perigee = orb.orbit_elements.arg_perigee
mean_anomaly = orb.orbit_elements.mean_anomaly
mean_motion = orb.orbit_elements.mean_motion
eixo = orb.orbit_elements.semi_major_axis"""
# Imprime informações orbitais
"""print(f"Latitude: {lat}")
print(f"Longitude: {long}")
print(f"Altitude: {alt}")
print(f"Inclinação: {inclination}")
print(f"Eccentricidade: {eccentricity}")
print(f"RAAN: {raan}")
print(f"Argumento do perigeu: {arg_perigee}")
print(f"Anomalia média: {mean_anomaly}")
print(f"Movimento médio: {mean_motion}")
print(f"Posição: {pos}")
print(f"Velocidade: {vel}")
print(f"Eixo semi: {eixo}")"""

fig = plt.figure(figsize=(12, 10))

    # Plot da órbita
ax1 = fig.add_subplot(221, projection='3d')
print(xCords, "\n\n", yCords, "\n\n", zCords)
ax1.plot(zCords, xCords, yCords)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('Órbita do Satélite')

raio_terra = 6371.0
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x_terra = raio_terra * np.outer(np.cos(u), np.sin(v))
y_terra = raio_terra * np.outer(np.sin(u), np.sin(v))
z_terra = raio_terra * np.outer(np.ones(np.size(u)), np.cos(v))
#ax1.plot_surface(x_terra, y_terra, z_terra, color='blue', alpha=0.2)

ax1.set_aspect('equal')
#ax1.grid(True)

#plt.tight_layout()
plt.show()
