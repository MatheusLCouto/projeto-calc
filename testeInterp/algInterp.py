"""def interpolar_linearmente(x1, y1, x2, y2, num_pontos):
    valores_interpolados = []

    # Calcula o incremento entre os pontos
    incremento = (x2 - x1) / (num_pontos - 1)

    # Realiza a interpolação linear para cada ponto no intervalo
    for i in range(num_pontos):
        ponto_interesse = x1 + (i * incremento)
        valor_interpolado = y1 + ((ponto_interesse - x1) * (y2 - y1)) / (x2 - x1)
        valores_interpolados.append(valor_interpolado)

    return valores_interpolados


# Exemplo de uso
x1 = 0.0
y1 = 0.0
x2 = 10.0
y2 = 20.0
num_pontos = 6

valores_interpolados = interpolar_linearmente(x1, y1, x2, y2, num_pontos)
print("Valores interpolados:", valores_interpolados)
"""


def interpolar_linearmente(x1, y1, x2, y2, ponto_interesse):
    # Calcula o valor interpolado usando a fórmula da interpolação linear
    valor_interpolado = y1 + ((ponto_interesse - x1) * (y2 - y1)) / (x2 - x1)

    return valor_interpolado


# Exemplo de uso
x1 = 0.0
y1 = 0.0
x2 = 10.0
y2 = 20.0
ponto_interesse = 5.0

valor_interpolado = interpolar_linearmente(x1, y1, x2, y2, ponto_interesse)
print("Valor interpolado:", valor_interpolado)
