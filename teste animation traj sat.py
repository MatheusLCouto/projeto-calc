import math
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Função para calcular a posição do satélite em coordenadas cartesianas
def calcular_posicao_satelite(tle, tempo_atual):
    line1 = tle['line1']
    line2 = tle['line2']

    epoch_year = int(line1[20:22].strip() or 0)
    print(epoch_year)
    epoch_day = float(line1[22:24])
    print(epoch_day)

    epoch_datetime = datetime.datetime(year=2000 + epoch_year, month=1, day=1) + datetime.timedelta(days=epoch_day)

    tempo_passado = tempo_atual - epoch_datetime

    line2 = tle['line2']
    raio = float(line2[52:63]) * 6371.0  # raio em quilômetros
    inclination = float(line2[8:16])
    raan = float(line2[17:25])
    eccentricity = float("0." + line2[26:33])
    argument_of_perigee = float(line2[34:42])
    mean_anomaly = float(line2[43:51])
    mean_motion = float(line2[52:63])

    # Cálculo dos parâmetros orbitais
    n = mean_motion * 2 * math.pi / (24 * 60 * 60)  # movimento médio
    a = (6.67430 * 10 ** -11 * 5.97219 * 10 ** 24 * (86400 / (2 * math.pi)) ** 2 / n ** 2) ** (1 / 3)  # semieixo maior
    p = a * (1 - eccentricity ** 2)  # semilatus rectum
    r = p / (1 + eccentricity * math.cos(mean_anomaly))  # distância do foco
    true_anomaly = mean_anomaly + argument_of_perigee  # anomalia verdadeira
    x_orbital = r * (math.cos(raan) * math.cos(argument_of_perigee + true_anomaly) - math.sin(raan) * math.sin(
        argument_of_perigee + true_anomaly) * math.cos(inclination))
    y_orbital = r * (math.sin(raan) * math.cos(argument_of_perigee + true_anomaly) + math.cos(raan) * math.sin(
        argument_of_perigee + true_anomaly) * math.cos(inclination))
    z_orbital = r * (math.sin(inclination) * math.sin(argument_of_perigee + true_anomaly))

    return x_orbital, y_orbital, z_orbital


# Função para prever a trajetória do satélite
def prever_trajetoria_satelite(tle, tempo_inicial, tempo_final, delta_tempo):
    tempos = []
    posicoes = []

    tempo_atual = tempo_inicial
    while tempo_atual <= tempo_final:
        tempos.append(tempo_atual)

        x, y, z = calcular_posicao_satelite(tle, tempo_atual)
        posicoes.append([x, y, z])

    return np.array(tempos), np.array(posicoes)


# Função para atualizar o gráfico a cada frame da animação
def update(frame):
    ax.clear()
    ax.plot(posicoes[:frame, 0], posicoes[:frame, 1], color='blue')
    ax.scatter(posicoes[frame, 0], posicoes[frame, 1], color='red', label='Ponto Atual')
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_title('Trajetória do Satélite')
    ax.legend()


# Dados de exemplo
tle = {
    'name': 'STARLINK-5540/2023-058Z',
    'line1': '1 1 56340C 23058Z   23146.31576389 -.00975607  00000-0 -24432-1 0  1460',
    'line2': '2 56340  97.6555 147.0752 0001806 101.7264 147.7231 15.41115726    18'
}

tempo_inicial = datetime.datetime(2023, 5, 26, 0, 0, 0)
tempo_final = datetime.datetime(2023, 5, 27, 0, 0, 0)
delta_tempo = datetime.timedelta(hours=1)

# Obter a previsão da trajetória do satélite
tempos, posicoes = prever_trajetoria_satelite(tle, tempo_inicial, tempo_final, delta_tempo)

# Criar a figura e o eixo
fig, ax = plt.subplots(figsize=(10, 10))

# Criar a animação
ani = FuncAnimation(fig, update, frames=len(tempos), interval=200, blit=False)

# Exibir a animação
plt.show()