import ephem

def calcular_desvio_rota_satelite(tle_line1, tle_line2, altitude_satelite, velocidade_orbital):
    # Criar objeto TLE
    tle = ephem.readtle("STARLINK-1007", tle_line1, tle_line2)

    # Configurar a localização do observador (no caso, a superfície da Terra)
    observador = ephem.Observer()
    observador.lat = 0  # Latitude 0 graus (equador)
    observador.lon = 0  # Longitude 0 graus (meridiano de Greenwich)
    observador.elev = 0   # Altitude 0 metros (nível do mar)

    # Definir a data e hora para o cálculo
    observador.date = ephem.now()

    # Obter a posição do satélite
    posicao_satelite = ephem.degrees(tle.compute(observador))

    # Calcular o desvio de rota
    desvio_rota = (posicao_satelite - observador.lon) * altitude_satelite / velocidade_orbital

    return desvio_rota

# Exemplo de uso
tle_line1 = "1 44713U 19074A   23001.33310695  .00000538  00000+0  55037-4 0  9995"
tle_line2 = "2 44713  53.0541   9.1431 0002180  39.3908 320.7239 15.06389052173400"
altitude_satelite = 545  # Altitude do satélite em quilômetros
velocidade_orbital = 7.67  # Velocidade orbital do satélite em quilômetros por segundo

desvio = calcular_desvio_rota_satelite(tle_line1, tle_line2, altitude_satelite, velocidade_orbital)
print(f"O desvio de rota do satélite é de aproximadamente {desvio} graus.")
