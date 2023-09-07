import datetime
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv

# Função para calcular as coordenadas x, y, z
def calcular_coordenadas(tle_line1, tle_line2):
    # Converter as linhas TLE em um objeto satélite
    satellite = twoline2rv(tle_line1, tle_line2, wgs72)

    # Obter a data e hora atual
    data_hora_atual = datetime.datetime.now()

    # Calcular as coordenadas do objeto espacial na data e hora atual
    posicao, _ = satellite.propagate(
        data_hora_atual.year, data_hora_atual.month, data_hora_atual.day,
        data_hora_atual.hour, data_hora_atual.minute, data_hora_atual.second
    )

    # As coordenadas são retornadas em kilômetros
    x, y, z = posicao

    return x, y, z

# Exemplo de uso
tle_line1 = '1 25544U 98067A   03124.78853147  .00021906  00000-0  28403-3 0  8652'
tle_line2 = '2 25544  51.6361  13.7980 0004256  35.6671  59.2566 15.58778559250029'

x, y, z = calcular_coordenadas(tle_line1, tle_line2)

print('Coordenadas:')
print('x:', x, 'km')
print('y:', y, 'km')
print('z:', z, 'km')
