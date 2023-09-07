import datetime
from sgp4.api import Satrec
from sgp4.api import jday

def calcular_data_juliana(data):
    data_referencia = datetime.datetime(1, 1, 1)
    delta = data - data_referencia
    segundos_totais = delta.total_seconds()
    data_juliana = 1721425.5 + segundos_totais / 86400.0
    return data_juliana

# Exemplo de uso:
data = datetime.datetime(2023, 1, 1, 7, 49, 40, 40)
deltaTempo = datetime.timedelta(minutes=1)
tempoFinal = data + (5 * deltaTempo)
while data <= tempoFinal:
    data_juliana = calcular_data_juliana(data)
    print("Data Juliana:", data_juliana)
    s = '1 44713U 19074A   23001.33310695  .00000538  00000+0  55037-4 0  9995'
    t = '2 44713  53.0541   9.1431 0002180  39.3908 320.7239 15.06389052173400'
    satellite = Satrec.twoline2rv(s, t)

    jd, fr = data_juliana, 0.362605
    e, r, v = satellite.sgp4(jd, fr)
    # print(satellite.sgp4_array(jd = jd, fr = fr))
    print(r, type(r))  # True Equator Mean Equinox position (km)
    print(v)  # True Equator Mean Equinox velocity (km/s)
    data += deltaTempo




