import matplotlib.pyplot as plt

# Dados de exemplo
labels = ['Categoria A', 'Categoria B', 'Categoria C', 'Categoria D']
porcentagens = [25, 30, 15, 30]

# Gerar índices para as barras
indices = range(len(porcentagens))

# Plotar o gráfico de barras
plt.bar(indices, porcentagens)

# Adicionar rótulos às barras
for i, porcentagem in enumerate(porcentagens):
    plt.text(i, porcentagem, f'{porcentagem}%', ha='center', va='bottom')

# Personalizar os eixos e rótulos
plt.xticks(indices, labels)
plt.xlabel('Categorias')
plt.ylabel('Porcentagem')

# Exibir o gráfico
plt.show()
