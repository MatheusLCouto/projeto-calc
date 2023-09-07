"""
Importando as bibliotecas necessárias para o programa
"""

import math
import datetime
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pyorbital.orbital import Orbital
from skyfield.api import Topos, load
from sgp4.api import Satrec, jday
from scipy.interpolate import interp1d
import matplotlib.animation as animation
import warnings

"""
constantes
"""

radEarth = 6378.137 # raio da terra

fig = plt.figure(figsize=(14, 10)) # figura para plot

pertRaan = 0.0

# Função para separar as linhas do 3LE (nome, linha1, linha2)
def separateToLines(tle_file):
    with open(tle_file, 'r') as file:
        lines = file.readlines()

    nameSat = []
    line1 = []
    line2 = []

    i = 0
    for _ in lines:
        if i % 3 == 0:
            nameSat.append(lines[i].replace("\n", ""))
            line1.append(lines[i+1].replace("\n", ""))
            line2.append(lines[i+2].replace("\n", ""))
        i += 1

    return nameSat, line1, line2

def satelliteData(nameSat, line1, line2):
    satelitte = {}

    # Criando objeto Orbital a partir do TLE
    orb = Orbital(nameSat, line1=line1, line2=line2)

    # Criando TLE a partir do objeto orb
    tleSat = orb.tle

    # Extração dos dados necessários
    satelitte['epoch'] = tleSat.epoch.astype(datetime) # data do momento do TLE
    posLatLongAlt = orb.get_lonlatalt(tleSat.epoch)
    satelitte['latitude'] = posLatLongAlt[1] # latitude
    satelitte['longitude'] = posLatLongAlt[0] # longitude
    satelitte['altitude'] = posLatLongAlt[2] # altitude
    satelitte['inclination'] = tleSat.inclination
    satelitte['excentricity'] = tleSat.excentricity
    satelitte['perigee'] = tleSat.arg_perigee
    satelitte['RAAN'] = tleSat.right_ascension
    satelitte['mean-anomaly'] = tleSat.mean_anomaly
    satelitte['mean-motion'] = tleSat.mean_motion
    satelitte['semi-major'] = orb.orbit_elements.semi_major_axis * 6371

    return satelitte

# Função para calcular a anomalia excêntrica usando o método de Newton
def calculateEccentricAnomaly(average_meanAnomaly, excentricity):
    # Inicializa a anomalia excêntrica como a anomalia média
    if excentricity < 0.8:
        excentricityAnomaly = average_meanAnomaly
    else:
        excentrincityAnomaly = math.pi

    max_iter = 15  # Número máximo de iterações
    delta = 1e-11  # Critério de convergência

    f = excentricityAnomaly - excentricity * math.sin(excentricityAnomaly) - average_meanAnomaly
    # Método de Newton
    for _ in range(max_iter):
        f_prime = excentricityAnomaly - f / (1 * excentricity * math.cos(excentricityAnomaly))
        f = excentricityAnomaly - excentricity * math.sin(excentricityAnomaly) - average_meanAnomaly
        delta_E = f / f_prime
        excentricityAnomaly -= delta_E

        if abs(delta_E) < delta:
            break

    return excentricityAnomaly

# Função para calcular a posição do satélite em relação ao tempo atual
def calculatePositionSat(tleSat, currentTime):
    global pertRaan

    inclination = math.radians(tleSat['inclination'])
    RAAN = math.radians(tleSat['RAAN'])
    excentricity = tleSat['excentricity']
    perigee = math.radians(tleSat['perigee'])
    meanAnomaly = math.radians(tleSat['mean-anomaly'])
    meanMotion = tleSat['mean-motion'] * 2 * math.pi / 86400.0
    pastTime = (currentTime - tleSat['epoch']).total_seconds()

    # Determina a rotação da órbita
    if pastTime != 0:
        pertRaan += 5e-5
        RAAN += pertRaan

    average_meanAnomaly = meanAnomaly + meanMotion * pastTime
    excentricityAnomaly = calculateEccentricAnomaly(average_meanAnomaly, excentricity)
    trueAnomaly = math.atan2(math.sqrt(1 - excentricity ** 2) * math.sin(excentricityAnomaly),
                             math.cos(excentricityAnomaly) - excentricity)

    radius = ((tleSat['semi-major']) * (1 - excentricity ** 2)) / (
            1 + excentricity * math.cos(trueAnomaly))
    # Conversão de coordenadas polares no sistema orbital para coordenadas cartesianas
    Xw = radius * math.cos(trueAnomaly)
    Yw = radius * math.sin(trueAnomaly)

    """Cálculo de vetores de transformação que auxiliam na conversão do 
    sistema Orbital para o sistema Earth-Fixed (Terra - Fixa)"""

    Px = math.cos(perigee) * math.cos(RAAN) - math.sin(perigee) * math.sin(
        RAAN) * math.cos(inclination)
    Py = math.cos(perigee) * math.sin(RAAN) + math.sin(perigee) * math.cos(
        RAAN) * math.cos(inclination)
    Pz = math.sin(perigee) * math.sin(inclination)
    Qx = -math.sin(perigee) * math.cos(RAAN) - math.cos(perigee) * math.sin(
        RAAN) * math.cos(inclination)
    Qy = -math.sin(perigee) * math.sin(RAAN) + math.cos(perigee) * math.cos(
        RAAN) * math.cos(inclination)
    Qz = math.cos(perigee) * math.sin(inclination)

    # Equações em relação à teoria de Keppler
    x = Px * Xw + Qx * Yw
    y = Py * Xw + Qy * Yw
    z = Pz * Xw + Qz * Yw

    """
    Referência: 
        Methods of Orbit Determination
        Pedro Ramon Escobal
        páginas 401 e 402 
    """
    return -x, -y, -z

# Função para calcular a trajetória do satélite por previsão
def calculateOrbit(tleSat, initTime, endTime, deltaTime):
    times, positions, heights, speeds = [], [], [], []

    currentTime = initTime

    while currentTime <= endTime:
        x, y, z = calculatePositionSat(tleSat, currentTime)
        r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        v = math.sqrt(tleSat['semi-major']) * math.sqrt(1 - tleSat['excentricity'] ** 2) / r
        altitude = r - radEarth     # Altitude em relação à superfície da Terra
        times.append(currentTime)
        positions.append((x, y, z))
        heights.append(altitude)
        speeds.append(v)
        currentTime += deltaTime

    return times, positions, heights, speeds

# Função para calcular as médias orbitais (periodos e velocidades)
def calculateMeanOrbitTime(meanMotion, altitude):

    # Conversão de revoluções por dia para radianos por segundo
    numRevolutions = (meanMotion * 2 * math.pi) / (24 * 60 * 60)

    # Cálculo do período orbital em segundos
    periodOrbitalS = (2 * math.pi) / numRevolutions

    # Cálculo da velocidade média em metros por segundo
    velSatMs = 2 * math.pi * ((radEarth + altitude) * 10 ** 3) / periodOrbitalS

    # Conversão para km/h, horas e minutos
    periodOrbitalM = (periodOrbitalS / 60)
    periodOrbitalH = periodOrbitalM / 60
    velSatH = velSatMs * 3.6
    numOrbitsPerDay = 24 * 60 * 60 / periodOrbitalS

    return periodOrbitalS, periodOrbitalM, periodOrbitalH, velSatMs, velSatH, numOrbitsPerDay

# Função para calcular as cordenadas do satélite real
def calculateCoordinates(nameSat, line1, line2, initTime, endTime, deltaTime):
    lat, lon, alt, ht = [], [], [], []
    i = 0
    currentTime = initTime
    orb = Orbital(nameSat, line1 = line1, line2 = line2)

    while currentTime <= endTime:
        posLatLonAlt = orb.get_lonlatalt(currentTime)
        lon.append(posLatLonAlt[0])
        lat.append(posLatLonAlt[1])
        alt.append(posLatLonAlt[2])
        ht.append(alt[i] + radEarth)
        currentTime += deltaTime
        i+=1

    return lat, lon, alt, ht

# Função para calcular data em formato juliano
def calculateJulianDate(date):
    refDate = datetime(1, 1, 1)
    delta = date - refDate
    totalSeconds = delta.total_seconds()
    julianDate = 1721425.5 + totalSeconds / 86400.0

    return julianDate


# Função para calcular a órbita real do satélite
def calculateRealOrbit(line1, line2, initTime, endTime, deltaTime):
    xReal, yReal, zReal = [], [], []
    satellite = Satrec.twoline2rv(line1, line2)

    while initTime <= endTime:
        julianDate = calculateJulianDate(initTime)
        jd, fr = julianDate, 0.362605
        error, pos, vel = satellite.sgp4(jd, fr)
        xReal.append(pos[0])
        yReal.append(pos[1])
        zReal.append(pos[2])
        initTime += deltaTime

    return xReal, yReal, zReal

# Função para criar 3 arrays (x, y, z) para guardar os valores do globo terrestre
def getEarthCoordinates():
    lat, lon = np.mgrid[-90:91:0.5, -180:181:0.5]
    x = radEarth * np.cos(np.radians(lat)) * np.cos(np.radians(lon))
    y = radEarth * np.cos(np.radians(lat)) * np.sin(np.radians(lon))
    z = radEarth * np.sin(np.radians(lat))

    return x, y, z

#função que atualiza os frames do plot em função do tempo
def updateFrame(frame, x, y, z, point, line):
    # Atualiza a posição do ponto

    point.set_data(x[frame], y[frame])
    point.set_3d_properties(z[frame])
    line.set_data(x[:frame + 1], y[:frame + 1])
    line.set_3d_properties(z[:frame + 1])

    return point, line

# Função para criar a órbita do satélite em órbita da terra
def createFigOrb(x, y, z, typeOrb, id):
    ax = fig.add_subplot(id, projection='3d')

    ax.plot(x, y, z, color ='r')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Órbita do Satélite {typeOrb}')

    xEarth, yEarth, zEarth = getEarthCoordinates()
    ax.plot_surface(xEarth, yEarth, zEarth, cmap='Blues', alpha = 0.4)
    ax.set_xlim(-7200, 7200)
    ax.set_ylim(-7200, 7200)
    ax.set_zlim(-7200, 7200)

    return ax

# Função para criar as tabelas de posição dos satélites
def createTablePos(x, y, z, time, title, id):

    ax = fig.add_subplot(id)
    firstDate = time[0].strftime('%Y-%m-%d %H:%M:%S')
    lastDate = time[-1].strftime('%Y-%m-%d %H:%M:%S')
    ax.plot(time, x)
    ax.plot(time, y)
    ax.plot(time, z)
    ax.legend(['X', 'Y', 'Z'])
    ax.set_xlabel(f'Tempo Inicial {firstDate} e Tempo Final {lastDate}')
    ax.set_xticklabels('')
    ax.set_ylabel('Posição')
    ax.set_title(f'Posições do Satélite {title}')

    return ax

# Função para agrupar as órbitas e as posições dos satélites (Previsão e Real)
def plotOrb(fig1, fig2, fig3, fig4):

    fig1.set_aspect('equal')
    fig2.set_aspect('equal')
    fig1.grid(True)
    fig2.grid(True)
    fig3.grid(True)
    fig4.grid(True)
    fig1.axis('off')
    fig2.axis('off')
    plt.tight_layout()

# Função para calcular a interpolação linear de 2 retas
def interpPM(x, y1, y2):
    # Interpola os valores y1 e y2 no mesmo grid de x
    interp_y1 = np.interp(x, x, y1)
    interp_y2 = np.interp(x, x, y2)

    # Calcula o ponto médio entre os valores interpolados
    medPoint = (interp_y1 + interp_y2) / 2.0

    return medPoint


def plotInterpPos(xPrev, yPrev, zPrev, xReal, yReal, zReal, altPrev, altReal):
    fig2 = plt.figure(figsize=(14, 10))
    ax1 = fig2.add_subplot(221)
    ax2 = fig2.add_subplot(222)
    ax3 = fig2.add_subplot(223)
    ax4 = fig2.add_subplot(224)

    interv = [i for i in range(len(xPrev))]
    interpX = interpPM(interv, xReal, xPrev)
    interpY = interpPM(interv, yReal, yPrev)
    interpZ = interpPM(interv, zReal, zPrev)
    interpAlt = interpPM(interv, altReal, altPrev)

    ax1.plot(interv, xReal)
    ax1.plot(interv, xPrev)
    ax1.plot(interv, interpX)
    ax1.legend(['X real', 'X prev', 'X interp'])
    ax1.set_xlabel('Tempo')
    ax1.set_ylabel('Posição')
    ax1.set_title('Interpolação X')

    ax2.plot(interv, yReal)
    ax2.plot(interv, yPrev)
    ax2.plot(interv, interpY)
    ax2.legend(['Y real', 'Y prev', 'Y interp'])
    ax2.set_xlabel('Tempo')
    ax2.set_ylabel('Posição')
    ax2.set_title('Interpolação Y')

    ax3.plot(interv, zReal)
    ax3.plot(interv, zPrev)
    ax3.plot(interv, interpZ)
    ax3.legend(['Z real', 'Z prev', 'Z interp'])
    ax3.set_xlabel('Tempo')
    ax3.set_ylabel('Posição')
    ax3.set_title('Interpolação Z')

    ax4.plot(interv, altReal)
    ax4.plot(interv, altPrev)
    ax4.plot(interv, interpAlt)
    ax4.legend(['Alt real', 'Alt prev', 'Alt interp'])
    ax4.set_xlabel('Tempo')
    ax4.set_ylabel('Altitude')
    ax4.set_title('Interpolação Altitude')

    plt.tight_layout()

# Função para plotar os erros em porcentagem
def plotErros(xPrev, yPrev, zPrev, xReal, yReal, zReal, altPrev, altReal):

    size = len(xPrev)
    interv = [i for i in range(size)]
    labelsX = ["" for i in range(size)]
    labelsY = ["" for i in range(size)]
    labelsZ = ["" for i in range(size)]
    labelsAlt = ["" for i in range(size)]

    errorAbsX = [abs(xReal[i] - xPrev[i]) for i in range(size)]
    errorAbsY = [abs(yReal[i] - yPrev[i]) for i in range(size)]
    errorAbsZ = [abs(zReal[i] - zPrev[i]) for i in range(size)]
    errorAbsAlt = [abs(altReal[i] - altPrev[i]) for i in range(size)]

    errorRelX = [abs(errorAbsX[i] / xReal[i]) for i in range(size)]
    errorRelY = [abs(errorAbsY[i] / yReal[i]) for i in range(size)]
    errorRelZ = [abs(errorAbsZ[i] / zReal[i]) for i in range(size)]
    errorRelAlt = [abs(errorAbsAlt[i] / altReal[i]) for i in range(size)]

    errorPerX = [errorRelX[i] * 100 for i in range(size)]
    errorPerY = [errorRelY[i] * 100 for i in range(size)]
    errorPerZ = [errorRelZ[i] * 100 for i in range(size)]
    errorPerAlt = [errorRelAlt[i] * 100 for i in range(size)]

    plt.figure(3, figsize=(14, 10))
    plt.subplot(221)
    plt.bar(interv, errorPerX)
    for i, error in enumerate(errorPerX):
        plt.text(i, error, '', ha='center', va='bottom')

    plt.xticks(interv, labels=labelsX)
    plt.xlabel('Erros dos pontos X')
    plt.ylabel('Porcentagem')
    plt.ylim(0, 100)

    plt.figure(3)
    plt.subplot(222)
    plt.bar(interv, errorPerY)
    for i, error in enumerate(errorPerY):
        plt.text(i, error, '', ha='center', va='bottom')

    plt.xticks(interv, labels=labelsY)
    plt.xlabel('Erros dos pontos Y')
    plt.ylabel('Porcentagem')
    plt.ylim(0, 100)

    plt.figure(3)
    plt.subplot(223)
    plt.bar(interv, errorPerZ)
    for i, error in enumerate(errorPerZ):
        plt.text(i, error, '', ha='center', va='bottom')

    plt.xticks(interv, labels=labelsZ)
    plt.xlabel('Erros dos pontos Z')
    plt.ylabel('Porcentagem')
    plt.ylim(0, 100)

    plt.figure(3)
    plt.subplot(224)
    plt.bar(interv, errorPerAlt)
    for i, error in enumerate(errorPerAlt):
        plt.text(i, error, '', ha='center', va='bottom')

    plt.xticks(interv, labels=labelsAlt)
    plt.xlabel('Erros das altitudes')
    plt.ylabel('Porcentagem')
    plt.ylim(0, 100)

    plt.tight_layout()
    plt.show()


def main():
    name_TLE = "tle.txt" # nome do arquivo (TLE)
    nameSat, line1, line2 = separateToLines(name_TLE) # separando os nomes dos satélites e dividindo por linhas
    selection = int(input(f"DIGITE UM NÚMERO PARA SELECIONAR UM SATÉLITE (1 a {len(nameSat)}): "))
    while (selection > len(nameSat)) | (selection < 1):
        print("DIGITOU UM NÚMERO INVÁLIDO")
        selection = int(input(f"DIGITE UM NÚMERO PARA SELECIONAR UM SATÉLITE (1 a {len(nameSat)}): "))

    selection -= 1
    print(F"FOI SELECIONADO O SATÉLITE: {nameSat[selection]}")

    # Obtendo as informações necessárias do satélite e atribuindo em um dicionário
    satelliteSelect = satelliteData(nameSat[selection],
                                    line1[selection],
                                    line2[selection]) # recebendo as informações necessárias

    periodOrbitalS, \
        periodOrbitalM, \
        periodOrbitalH, velSatMs, \
        velSatH, \
        numOrbitsPerDay = calculateMeanOrbitTime(satelliteSelect['mean-motion'],
                                         satelliteSelect['altitude'])
    # leitura dos minutos totais da trajetória
    minutes = float(input(f"DIGITE UM NÚMERO DE MINUTOS (5 a {5 * round(periodOrbitalM * numOrbitsPerDay)}): "))
    while (minutes > round(5 * numOrbitsPerDay * periodOrbitalM)) | (minutes < 5):
        print("DIGITOU UM NÚMERO INVÁLIDO")
        minutes = float(input(f"DIGITE UM NÚMERO DE MINUTOS (5 a {5 * round(periodOrbitalM * numOrbitsPerDay)}): "))

    # criação de parâmetros de tempo
    deltaHours = timedelta(minutes=minutes)
    deltaTime = timedelta(milliseconds=60000)  # 1 minuto de intervalo para cada ponto no espaço
    endTime = satelliteSelect['epoch'] + deltaHours
    timesSat, \
        positionsSat, \
        heigthsPrevSat, \
        velocitiesSat = calculateOrbit(satelliteSelect,
                                       satelliteSelect['epoch'],
                                       endTime,
                                       deltaTime)
    # Obter e guardas os pontos (x, y e z) reais do satélite
    xRealSat, \
        yRealSat, \
        zRealSat = calculateRealOrbit(line1[selection],
                                      line2[selection],
                                      satelliteSelect['epoch'],
                                      endTime,
                                      deltaTime)

    latReal, lonReal, altReal, heigthsRealSat = calculateCoordinates(nameSat[selection],
                                                                     line1[selection],
                                                                     line2[selection],
                                                                     satelliteSelect['epoch'],
                                                                     endTime,
                                                                     deltaTime)

    # Distribue cada indice para os respectivos pontos x y z
    xPrevSat = [positionSat[0] for positionSat in positionsSat]
    yPrevSat = [positionSat[1] for positionSat in positionsSat]
    zPrevSat = [positionSat[2] for positionSat in positionsSat]

    # cria objeto para plotar a trajetoria em relação ao globo terrestre
    figPrev = createFigOrb(xPrevSat,
                           yPrevSat,
                           zPrevSat,
                           f"Previsão - {nameSat[selection]}",
                           221)
    figReal = createFigOrb(xRealSat,
                           yRealSat,
                           zRealSat,
                           f"Real - {nameSat[selection]}",
                           222)

    # cria objeto para tabelas
    tabPosPrev = createTablePos(xPrevSat,
                                yPrevSat,
                                zPrevSat,
                                timesSat,
                                f"da Previsão - {nameSat[selection]}",
                                223)
    tabPosReal = createTablePos(xRealSat,
                                yRealSat,
                                zRealSat,
                                timesSat,
                                f"Real - {nameSat[selection]}",
                                224)

    plotOrb(figPrev, figReal, tabPosPrev, tabPosReal)

    # criar tabelas de comparações
    plotInterpPos(xPrevSat, yPrevSat, zPrevSat,
                  xRealSat, yRealSat, zRealSat,
                  heigthsPrevSat, altReal)

    plotErros(xPrevSat, yPrevSat, zPrevSat,
                  xRealSat, yRealSat, zRealSat,
                  heigthsPrevSat, altReal)

if __name__ == "__main__":
    warnings.simplefilter("ignore")
    main()
