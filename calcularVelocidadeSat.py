import math

# Dados do TLE
mean_motion = 15.06389052  # Revoluções por dia

# Conversão de revoluções por dia para radianos por segundo
n = (mean_motion * 2 * math.pi) / (24 * 60 * 60)

# Cálculo do período orbital
T = (2 * math.pi) / n

V = 2 * 3.14 * ((6371 + 546.9578647197122) * 10 ** 3) / T
TH = (T / 60)/60

print("Período orbital:", T, "segundos")
print("Período orbital:", TH, "horas")
print(f"velocidade: {V * 3.6}")
