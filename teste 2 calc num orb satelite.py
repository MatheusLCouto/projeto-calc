import math
import datetime
import numpy as np
import matplotlib.pyplot as plt


# Função para calcular a anomalia excêntrica usando o método de Newton
def calcular_anomalia_excentrica(M, e):
    E = M  # Inicializa a anomalia excêntrica como a anomalia média
    max_iter = 100  # Número máximo de iterações
    delta = 1e-8  # Critério de convergência

    # Iteração de Newton
    for _ in range(max_iter):
        f = E - e * math.sin(E) - M
        f_prime = 1 - e * math.cos(E)
        delta_E = f / f_prime
        E -= delta_E

        if abs(delta_E) < delta:
            break

    return E

# Função para calcular a posição do satélite
def calcular_posicao_satelite(tle, tempo):
    inclinacao = math.radians(tle['inclination'])
    RAAN = math.radians(tle['RAAN'])
    excentricidade = tle['eccentricity']
    argumento_perigeu = math.radians(tle['argument_of_perigee'])
    anomalia_media = math.radians(tle['mean_anomaly'])
    movimento_medio = tle['mean_motion'] * 2 * math.pi / 86400.0

    tempo_decorrido = (tempo - tle['epoch']).total_seconds()
    #print(f"tempo: {tempo}\ttempo TLE: {tle['epoch']}\ttempo decorrido: {tempo_decorrido}")

    anomalia_media_media = anomalia_media + movimento_medio * tempo_decorrido

    anomalia_excen = calcular_anomalia_excentrica(anomalia_media_media, excentricidade)

    anomalia_verdadeira = math.atan2(math.sqrt(1 - excentricidade ** 2) * math.sin(anomalia_excen),
                                     math.cos(anomalia_excen) - excentricidade)

    raio = ((tle['semi_major_axis'] * 6371) * (1 - excentricidade ** 2)) / (1 + excentricidade * math.cos(anomalia_verdadeira))
    #print(f"reio atual: {raio}")
    x = raio * (math.cos(anomalia_verdadeira + RAAN) * math.cos(argumento_perigeu) - math.sin(
        anomalia_verdadeira + RAAN) * math.sin(argumento_perigeu) * math.cos(inclinacao))
    y = raio * (math.cos(anomalia_verdadeira + RAAN) * math.sin(argumento_perigeu) + math.sin(
        anomalia_verdadeira + RAAN) * math.cos(argumento_perigeu) * math.cos(inclinacao))
    z = raio * (math.sin(anomalia_verdadeira + RAAN) * math.sin(inclinacao))

    #print(x, y, z)

    return x, y, z

# Função para prever a trajetória do satélite
def prever_trajetoria_satelite(tle, tempo_inicial, tempo_final, delta_tempo):
    tempos = []
    posicoes = []
    alturas = []
    velocidades = []
    tempo_atual = tempo_inicial
    #print(f"tempo: {tempo_atual}")
    i = 0
    #while por minuto (i+=1)
    while tempo_atual <= tempo_final:

        x, y, z = calcular_posicao_satelite(tle, tempo_atual)
        r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        v = math.sqrt(tle['semi_major_axis']) * math.sqrt(1 - tle['eccentricity'] ** 2) / r
        altitude = r - 6371.0  # Altitude em relação à superfície da Terra
        tempos.append(tempo_atual)
        posicoes.append((x, y, z))
        alturas.append(altitude)
        velocidades.append(v)
        """if i == 0:
            print(altitude)
        i+=1"""
        tempo_atual += delta_tempo

    return tempos, posicoes, alturas, velocidades


# Função para plotar a órbita do satélite em relação à Terra
def plotar_orbita(tle, tempo_inicial, tempo_final, delta_tempo):
    tempos, posicoes, alturas, velocidades = prever_trajetoria_satelite(tle, tempo_inicial, tempo_final, delta_tempo)
    #tempos2, posicoes2, alturas2, velocidades2 = prever_trajetoria_satelite(tle2, tempo_inicial, tempo_final, delta_tempo)
    """
    
    """

    #print(f"Tempo: {tempos}\nPosição: {posicoes}\nVelocidade: {velocidades}\nAltura: {alturas}")

    fig = plt.figure(figsize=(12, 8))

    # Plot da órbita
    ax1 = fig.add_subplot(221, projection='3d')
    #print(posicoes)
    x_coords = [posicao[0] for posicao in posicoes]
    y_coords = [posicao[1] for posicao in posicoes]
    z_coords = [posicao[2] for posicao in posicoes]
    #print(x_coords, "\n\n", y_coords, "\n\n", z_coords)
    ax1.plot(x_coords, y_coords, z_coords)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Órbita do Satélite')

    tempos, posicoes, alturas, velocidades = prever_trajetoria_satelite(tle2, tempo_inicial2, tempo_final2, delta_tempo)

    #fig = plt.figure(figsize=(12, 8))

    # Plot da órbita 2
    """ax2 = fig.add_subplot(222, projection='3d')
    x_coords = [posicao[0] for posicao in posicoes]
    y_coords = [posicao[1] for posicao in posicoes]
    z_coords = [posicao[2] for posicao in posicoes]

    #print(x_coords)
    # print(x_coords, "\n\n", y_coords, "\n\n", z_coords)
    ax2.plot(x_coords, y_coords, z_coords)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    ax2.set_title('Órbita do Satélite')
"""
    raio_terra = 6371.0
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_terra = raio_terra * np.outer(np.cos(u), np.sin(v))
    y_terra = raio_terra * np.outer(np.sin(u), np.sin(v))
    z_terra = raio_terra * np.outer(np.ones(np.size(u)), np.cos(v))
    ax1.plot_surface(x_terra, y_terra, z_terra, color='blue', alpha=0.2)
    #ax2.plot_surface(x_terra, y_terra, z_terra, color='blue', alpha=0.2)
    ax1.set_aspect('equal')
    ax1.grid(True)
    #ax2.set_aspect('equal')
    #ax2.grid(True)

    # Plot da posição
    ax3 = fig.add_subplot(222)
    ax3.plot(tempos, [posicao[0] for posicao in posicoes])
    ax3.plot(tempos, [posicao[1] for posicao in posicoes])
    ax3.plot(tempos, [posicao[2] for posicao in posicoes])
    ax3.legend(['X', 'Y', 'Z'])
    ax3.set_xlabel('Tempo')
    ax3.set_ylabel('Posição')
    ax3.set_title('Posição do Satélite')

    # Plot da altitude
    ax4 = fig.add_subplot(223)
    ax4.plot(tempos, alturas)
    ax4.set_xlabel('Tempo')
    ax4.set_ylabel('Altitude')
    ax4.set_title('Altitude do Satélite')

    ax3 = fig.add_subplot(223, projection='3d')
    x_coords = [posicao[0] for posicao in posicoes]
    y_coords = [posicao[1] for posicao in posicoes]
    z_coords = [posicao[2] for posicao in posicoes]
    # print(x_coords, "\n\n", y_coords, "\n\n", z_coords)
    ax3.plot(x_coords, y_coords, z_coords)
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    ax3.set_title('Órbita do Satélite')

    ax3.set_aspect('equal')
    ax3.grid(True)

    # Plot da velocidade
    ax5 = fig.add_subplot(224)
    ax5.plot(tempos, velocidades)
    ax5.set_xlabel('Tempo')
    ax5.set_ylabel('Velocidade')
    ax5.set_title('Velocidade do Satélite')

    plt.tight_layout()
    plt.show()


# Exemplo de uso
tle = {
    'epoch': datetime.datetime(2023, 5, 27, 16, 59, 42),
    'semi_major_axis': 1.05348,
    'eccentricity': 0.0001759,
    'inclination': 43.0014,
    'RAAN': 0.997434,
    'argument_of_perigee': 4.621979,
    'mean_anomaly': 125.1681,
    'mean_motion': 15.769319
}

tle2 = {
    'epoch': datetime.datetime(2023, 1, 1, 7, 49, 40),
    'semi_major_axis': 1.085842604698925,
    'eccentricity': 0.00021799999999999999,
    'inclination': 53.0541,
    'RAAN': 9.1431,
    'argument_of_perigee': 39.3908,
    'mean_anomaly': 320.7239,
    'mean_motion': 15.06389052
}

#print(tle)

tempo_inicial = tle['epoch']
tempo_inicial2 = tle2['epoch']
print(f"tempo inicial: {tempo_inicial} e tipo {type(tempo_inicial)}")
deltaT = datetime.timedelta(hours=1.5)
tempo_final = tempo_inicial + deltaT
tempo_final2 = tempo_inicial2 + deltaT
delta_tempo = datetime.timedelta(milliseconds=60000)

plotar_orbita(tle, tempo_inicial, tempo_final, delta_tempo)
