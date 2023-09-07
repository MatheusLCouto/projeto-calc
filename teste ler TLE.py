"""from skyfield.api import load
import tkinter
from tkinter import filedialog
#import orbital
from datetime import datetime

# Carrega o arquivo TLE
tle_way = filedialog.askopenfilename(title="Selecione o arquivo TLE", filetypes=(("TXT files", "*.txt"), ("all files", "*.*")))
tle_file = load.tle_file(tle_way)

# Lista para armazenar as informações do TLE
tle_list = []
i: int = 0
# Loop através de cada linha do arquivo TLE
for line in tle_file:

    # Armazena as informações do TLE em uma lista
    tle_list.append(line)
    satellite = tle_file[i]

    # Obtém as informações orbitais completas do satélite
    ts = load.timescale()
    t = ts.now()
    position, velocity = satellite.at(t).position.km, satellite.at(t).velocity.km_per_s

    # Imprime as informações orbitais do satélite
    print("Satelite no momento {i}".format(i = i))
    print("Posição: ", position)
    print("Velocidade: ", velocity, "\n")
    i+=1
"""
# Imprime a lista de informações do TLE
"""print(tle_list)
line_list = tle_list[0]
print(line_list)
"""


from datetime import datetime, timedelta
from pyorbital.orbital import Orbital
#from orbital import plot

# TLE do Starlink-1007
tle = ['1 44713U 19074A   23001.33310695  .00000538  00000+0  55037-4 0  9995',
       '2 44713  53.0541   9.1431 0002180  39.3908 320.7239 15.06389052173400']

# Criar objeto Orbital a partir do TLE
orb = Orbital("STARLINK-1007", line1=tle[0], line2=tle[1])
#print(orb)

teste = orb.orbit_elements.epoch
print(teste, type(teste))

text = orb.tle
print(text)

startTime = datetime.utcnow()
endTime = startTime + timedelta(hours=12)

print(f"Horario de agora: {startTime}", type(startTime))
# Calcular a posição e velocidade no momento atual
pos, vel = orb.get_position(teste)



# Obtém informações orbitais do satélite
posLatLongAlt = orb.get_lonlatalt(teste)
lat = posLatLongAlt[1]
long = posLatLongAlt[0]
alt = posLatLongAlt[2]
#teste = orb.get_next_passes(datetime.utcnow(), length = 200, alt = alt, lat = lat, lon = long)
#print(teste)
inclination = orb.orbit_elements.inclination
eccentricity = orb.orbit_elements.excentricity
raan = orb.orbit_elements.right_ascension
arg_perigee = orb.orbit_elements.arg_perigee
mean_anomaly = orb.orbit_elements.mean_anomaly
mean_motion = orb.orbit_elements.mean_motion
eixo = orb.orbit_elements.semi_major_axis
print(orb.tle.id_launch_year)
# Imprime informações orbitais
print(f"Latitude: {lat}")
print(f"Longitude: {long}")
print(f"Altitude: {alt}")
print(f"Inclinação: {inclination} e {text.inclination}")
print(f"Eccentricidade: {eccentricity} e {text.excentricity}")
print(f"RAAN: {raan} e {text.right_ascension}")
print(f"Argumento do perigeu: {arg_perigee} e {text.arg_perigee}")
print(f"Anomalia média: {mean_anomaly} e {text.mean_anomaly}")
print(f"Movimento médio: {mean_motion} e {text.mean_motion}")
print(f"Posição: {pos}")
print(f"Velocidade: {vel}")
print(f"Eixo semi: {eixo}")