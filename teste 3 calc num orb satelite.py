import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import datetime
from datetime import datetime, timedelta
from pyorbital.orbital import Orbital


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

    tempo_decorrido = (tempo - tle['epoch']).total_seconds() / 60.0

    anomalia_media_media = anomalia_media + movimento_medio * tempo_decorrido

    anomalia_excen = calcular_anomalia_excentrica(anomalia_media_media, excentricidade)

    anomalia_verdadeira = math.atan2(math.sqrt(1 - excentricidade ** 2) * math.sin(anomalia_excen),
                                     math.cos(anomalia_excen) - excentricidade)

    raio = (tle['semi_major_axis'] * (1 - excentricidade ** 2)) / (1 + excentricidade * math.cos(anomalia_verdadeira))

    x = raio * (math.cos(anomalia_verdadeira + RAAN) * math.cos(argumento_perigeu) - math.sin(
        anomalia_verdadeira + RAAN) * math.sin(argumento_perigeu) * math.cos(inclinacao))
    y = raio * (math.cos(anomalia_verdadeira + RAAN) * math.sin(argumento_perigeu) + math.sin(
        anomalia_verdadeira + RAAN) * math.cos(argumento_perigeu) * math.cos(inclinacao))
    z = raio * (math.sin(anomalia_verdadeira + RAAN) * math.sin(inclinacao))

    return x, y, z


# Função para prever a trajetória do satélite
def prever_trajetoria_satelite(tle, tempo_inicial, tempo_final, delta_tempo):
    tempos = []
    posicoes = []
    alturas = []
    velocidades = []

    tempo_atual = tempo_inicial
    while tempo_atual <= tempo_final:
        x, y, z = calcular_posicao_satelite(tle, tempo_atual)
        r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        v = tle['mean_motion'] * (2 * math.pi / 86400.0) * tle['semi_major_axis'] / math.sqrt(tle['semi_major_axis'])
        h = r - 6371.0

        tempos.append(tempo_atual)
        posicoes.append((x, y, z))
        alturas.append(h)
        velocidades.append(v)

        tempo_atual += delta_tempo

    return tempos, posicoes, alturas, velocidades


# Função para plotar a trajetória do satélite e informações adicionais
def plotar_trajetoria_satelite(tle, tempo_inicial, tempo_final, delta_tempo):
    tempos, posicoes, alturas, velocidades = prever_trajetoria_satelite(tle, tempo_inicial, tempo_final, delta_tempo)

    fig = plt.figure(figsize=(12, 8))

    # Plotar trajetória
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    x_coords = [pos[0] for pos in posicoes]
    y_coords = [pos[1] for pos in posicoes]
    z_coords = [pos[2] for pos in posicoes]
    ax1.plot(x_coords, y_coords, z_coords)
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Órbita do Satélite')

    # Plotar posição ao longo do tempo
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(tempos, x_coords, label='X')
    ax2.plot(tempos, y_coords, label='Y')
    ax2.plot(tempos, z_coords, label='Z')
    ax2.legend()
    ax2.set_xlabel('Tempo')
    ax2.set_ylabel('Posição')
    ax2.set_title('Posição do Satélite ao Longo do Tempo')

    # Plotar altura ao longo do tempo
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.plot(tempos, alturas)
    ax3.set_xlabel('Tempo')
    ax3.set_ylabel('Altura')
    ax3.set_title('Altura do Satélite ao Longo do Tempo')

    # Plotar velocidade ao longo do tempo
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.plot(tempos, velocidades)
    ax4.set_xlabel('Tempo')
    ax4.set_ylabel('Velocidade')
    ax4.set_title('Velocidade do Satélite ao Longo do Tempo')

    plt.tight_layout()
    plt.show()

# Função para obter os dados do TLE a partir da entrada do usuário
def obter_dados_tle():
    print('Entre com os dados do TLE:')
    line1 = input('Linha 1: ')
    line2 = input('Linha 2: ')
    return line1, line2


# Função para processar os dados do TLE e retornar um dicionário
def processar_tle(line1, line2):
    tle = {}
    tle['epoch'] = datetime.strptime(line1[18:32], '%Y%m%d%H%M%S.%f')
    tle['semi_major_axis'] = float(line2[52:63])
    tle['eccentricity'] = float('.' + line2[26:33])
    tle['inclination'] = float(line2[8:16])
    tle['RAAN'] = float(line2[17:25])
    tle['argument_of_perigee'] = float(line2[34:42])
    tle['mean_anomaly'] = float(line2[43:51])
    tle['mean_motion'] = float(line2[52:63])
    return tle


# Função principal
def main():
    line1, line2 = obter_dados_tle()
    tle = processar_tle(line1, line2)

    tempo_inicial = tle['epoch']
    tempo_final = tempo_inicial + datetime.timedelta(hours=100)
    delta_tempo = datetime.timedelta(minutes=1)

    plotar_trajetoria_satelite(tle, tempo_inicial, tempo_final, delta_tempo)


# Executar a função principal
if __name__ == "__main__":
    main()
