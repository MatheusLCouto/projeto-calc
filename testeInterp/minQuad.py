"""import numpy as np

def estimar_diferenca_entre_retas(x, y1, y2):
    # Cria uma matriz A com as colunas [x, 1]
    A = np.vstack([x, np.ones_like(x)]).T

    # Calcula os coeficientes a e b para a reta que melhor se ajusta aos pontos y1
    a1, b1 = np.linalg.lstsq(A, y1, rcond=None)[0]

    # Calcula os coeficientes a e b para a reta que melhor se ajusta aos pontos y2
    a2, b2 = np.linalg.lstsq(A, y2, rcond=None)[0]

    # Calcula a diferença entre as duas retas
    diferenca = a1 - a2

    return diferenca

# Exemplo de uso
x = np.array([0, 1, 2, 3, 4])
y1 = np.array([1, 3, 5, 7, 9])
y2 = np.array([0, 2, 4, 6, 8])

diferenca = estimar_diferenca_entre_retas(x, y1, y2)
print("Diferença entre as retas:", diferenca)"""
import numpy as np
from scipy.interpolate import interp1d
"""
def estimar_pontos_medios(x, y1, y2, num_pontos):
    # Define a função de interpolação para y1 e y2 usando spline cúbica
    f1 = interp1d(x, y1, kind='cubic')
    f2 = interp1d(x, y2, kind='cubic')

    # Define os pontos de interpolação com base no número desejado de pontos
    x_interp = np.linspace(x.min(), x.max(), num_pontos)

    # Calcula os pontos médios entre as duas curvas interpoladas
    pontos_medios = (f1(x_interp) + f2(x_interp)) / 2.0

    return pontos_medios

# Exemplo de uso
x = np.array([0, 1, 2, 3, 4])
y1 = np.array([1, 3, 5, 7, 9])
y2 = np.array([0, 2, 4, 6, 8])
num_pontos = 1

pontos_medios = estimar_pontos_medios(x, y1, y2, num_pontos)
print("Pontos Médios:", pontos_medios)


"""

def interpolar_ponto_medio(x, y1, y2):
    # Interpola os valores y1 e y2 no mesmo grid de x
    interp_y1 = np.interp(x, x, y1)
    interp_y2 = np.interp(x, x, y2)

    # Calcula o ponto médio entre os valores interpolados
    ponto_medio = (interp_y1 + interp_y2) / 2.0

    return ponto_medio

# Exemplo de uso
x = np.array([0, 1, 2, 3, 4])
y1 = np.array([-3847.431793214774, -3644.733254596415, -3426.2738022859685, -3193.0002624095123, -2945.9236503875895])
y2 = np.array([-2944.17735835099, -2944.17735835099, -2425.07793615101, 2149.2421469751325, -1864.1229836547448])

ponto_medio = interpolar_ponto_medio(x, y1, y2)
print("Ponto Médio:", ponto_medio)
