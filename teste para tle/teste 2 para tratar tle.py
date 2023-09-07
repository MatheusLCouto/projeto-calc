from datetime import datetime, timedelta
import numpy
from pyorbital.orbital import Orbital
#from orbital import plot

alti: list = []
lati: list = []
longe: list = []

def extrair_dados(nameSat, line1, line2):
    # Criar objeto Orbital a partir do TLE
    #print(f"Nome: {nameSat}Linha 1: {line1}Linha 2: {line2}")
    orb = Orbital(nameSat, line1=line1, line2=line2)

    text = orb.tle
    #print(text)

    #print(orb.orbit_elements.epoch)

    startTime = datetime.utcnow()
    endTime = startTime + timedelta(hours=12)

    #print(f"Horario de agora: {startTime}")
    # Calcular a posição e velocidade no momento atual
    pos, vel = orb.get_position(orb.orbit_elements.epoch)

    # Obtém informações orbitais do satélite
    posLatLongAlt = orb.get_lonlatalt(orb.orbit_elements.epoch)
    lat: float = posLatLongAlt[0]
    long: float = posLatLongAlt[1]
    alt: float = posLatLongAlt[2]


    inclination = orb.orbit_elements.inclination
    eccentricity = orb.orbit_elements.excentricity
    raan = orb.orbit_elements.right_ascension
    arg_perigee = orb.orbit_elements.arg_perigee
    mean_anomaly = orb.orbit_elements.mean_anomaly
    mean_motion = orb.orbit_elements.mean_motion
    eixo = orb.orbit_elements.semi_major_axis

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
    #print(type(lat), type(long), type(alt))

    return lat, long, alt


def separar_por_indice(tle_file):
    with open(tle_file, 'r') as file:
        lines = file.readlines()

    tle_entries = []
    current_entry = []

    i, j = 0, 0
    for line in lines:
        line = line.strip()
        if line.startswith('1'):
            if current_entry:
                if i % 3 == 0:
                    nameSat = lines[i]
                    print("nome: ", nameSat)
                    line1 = lines[i+1]
                    print("linha 1: ", line1)
                    line2 = lines[i+2]
                    print("linha 2: ", line2)
                    #print(f"Nome: {nameSat}Linha 1: {line1}Linha 2: {line2}")
                    lat, long, alt = extrair_dados(nameSat, line1, line2)
                    lati.append(lat)
                    longe.append(long)
                    alti.append(alt)
                    j+=1
                i+=1
                tle_entries.append(current_entry)
                current_entry = []
        current_entry.append(line)

    if current_entry:
        tle_entries.append(current_entry)

    return tle_entries

# Exemplo de uso:
nome_arquivo = 'dados_tle.txt'
tle_entries = separar_por_indice(nome_arquivo)
print(tle_entries[1])

print(lati, "\n\n", longe, "\n\n", alti)

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
    global R
    R = R + 540
    print("2º R: ", R)
    T = 2 * np.pi * np.sqrt(R**3 / (G * M)) # período da órbita em segundos
    print(T)
    x = (R-1000) * np.cos(theta)
    y = (R-500) * np.sin(theta)
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
        print(x, y, z)

    return x, y, z

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
ax.plot(x_sat, y_sat, z_sat, color='r')

# plotagem da trajetória do satélite


#R = 8000000
# ajuste dos limites do eixo z
ax.set_xlim(-100 * R, 100 * R)
ax.set_ylim(-100 * R, 100 * R)
ax.set_zlim(-900 * R, 900 * R)
plt.autoscale()
# exibição do gráfico
plt.show()


#print(tle_entries[0][0])


"""
for i, entry in enumerate(tle_entries):
    print(f"Índice {i+1}:")
    print('\n'.join(entry))"""