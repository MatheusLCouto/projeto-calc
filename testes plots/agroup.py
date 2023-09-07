import matplotlib.pyplot as plt

# Cria a figura principal e os subplots
fig, axs = plt.subplots(1, 3)

# Plota nos subplots
axs[0].plot([1, 2, 3], [4, 5, 6])
axs[1].scatter([1, 2, 3], [4, 5, 6])
axs[2].bar([1, 2, 3], [4, 5, 6])

# Ajusta o layout dos subplots
plt.tight_layout()

# Exibe a janela com as figuras
plt.show()
