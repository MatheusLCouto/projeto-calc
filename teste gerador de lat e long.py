import numpy as np

# número de pontos a serem gerados
n = 1000

# geração de latitude e longitude aleatórias
lat = np.random.uniform(low=-90, high=90, size=n)
lon = np.random.uniform(low=-180, high=180, size=n)

# salvando os dados em um arquivo de texto
np.savetxt('lat_lon.txt', np.column_stack((lat, lon)))