import numpy as np
import time

def calcula_fitness_mochila(genotipo, peso_objetos, valor_objetos, peso_maximo_mochila):

    peso_total_mochila = sum(genotipo*peso_objetos)
    valor_total_objetos = sum(genotipo*valor_objetos)
    if (peso_total_mochila > peso_maximo_mochila):
        fitness = 0
    else:
        fitness = valor_total_objetos
    return fitness

# Problem parameters definitions
#peso_objetos = [350, 250, 160, 120, 200, 100, 120, 220, 40, 80]
#valor_objetos = [300, 400, 450, 350, 250, 300, 200, 250, 150, 400]

#peso_objetos = [350, 250, 160, 120, 200, 100, 120, 220, 40, 80, 100, 300, 180, 250, 220]
#valor_objetos = [300, 400, 450, 350, 250, 300, 200, 250, 150, 400, 350, 300, 450, 500, 350]

peso_objetos = [350, 250, 160, 120, 200, 100, 120, 220, 40, 80, 100, 300, 180, 250, 220, 150, 280, 310, 120, 160, 110, 210]
valor_objetos = [300, 400, 450, 350, 250, 300, 200, 250, 150, 400, 350, 300, 450, 500, 350, 400, 200, 300, 250, 300, 150, 200]

peso_maximo_mochila = 3000
taxa_mutacao = 0.005
tamanho_populacao = 10
tamanho_genoma = len(peso_objetos)
fitness_ideal = sum(valor_objetos) * 0.9
geracao_limite = 1000

# Generate initial random population
populacao = np.random.randint(2, size=(tamanho_populacao, tamanho_genoma))

fitness_valor_objetos_inicial = []
for i in range(tamanho_populacao):
    fitness_valor_objetos_inicial.append(calcula_fitness_mochila(populacao[i], peso_objetos, valor_objetos, peso_maximo_mochila))

# Find best genotype
melhor_fitnes_inicial = max(fitness_valor_objetos_inicial)

inicio = time.time()
# Evolution loop
geracao = 0
for gen in range(geracao_limite):
    fitness_valor_objetos = []

    for i in range(tamanho_populacao):
        fitness_valor_objetos.append(calcula_fitness_mochila(populacao[i], peso_objetos, valor_objetos, peso_maximo_mochila))
    
    # Find best genotype
    melhor_fitness = max(fitness_valor_objetos)
    melhor_idx = fitness_valor_objetos.index(max(fitness_valor_objetos))

    melhor_genotipo = populacao[melhor_idx]
    
    # Verify stop condition
    if melhor_fitness >= fitness_ideal:
        geracao = gen+1
        break

    # Parents definition
    size = (tamanho_populacao, tamanho_genoma)
    pais = np.zeros(size, dtype=int)

    for j in range(tamanho_populacao):
        index_pai_1 = np.random.randint(tamanho_populacao)
        index_pai_2 = np.random.randint(tamanho_populacao)
        if fitness_valor_objetos[index_pai_1] > fitness_valor_objetos[index_pai_2]:
            pais[j] = populacao[index_pai_1]
        else:
            pais[j] = populacao[index_pai_2]

    # Crossover
    offspring = np.zeros(size, dtype=int)

    for k in range(tamanho_populacao):
        # Random crossover gene point
        ponto_de_crossover = np.random.randint(tamanho_genoma)
        index_pai_1 = np.random.randint(tamanho_populacao)
        index_pai_2 = np.random.randint(tamanho_populacao)
        pai_1 = pais[index_pai_1]
        pai_2 = pais[index_pai_2]

        # Apply crossover
        offspring[k, :ponto_de_crossover] = pai_1[:ponto_de_crossover]
        offspring[k, ponto_de_crossover:] = pai_2[ponto_de_crossover:]

    # Mutation
    for l in range(tamanho_populacao):
        for m in range(tamanho_genoma):
            if np.random.rand() < taxa_mutacao:
                if offspring[l][m] == 0:
                    offspring[l][m] = 1
                else:
                    offspring[l][m] = 0

    # Update population
    populacao = offspring
    geracao = gen+1

final = time.time()

fitness_valor_objetos_final = []
for i in range(tamanho_populacao):
        fitness_valor_objetos_final.append(calcula_fitness_mochila(populacao[i], peso_objetos, valor_objetos, peso_maximo_mochila))

# Best genotype
melhor_idx = fitness_valor_objetos.index(max(fitness_valor_objetos))

itens_escolhidos = []
for i in range(tamanho_genoma):
    if(populacao[melhor_idx][i]) == 1:
        itens_escolhidos.append(i)

melhor_fitness_final = calcula_fitness_mochila(populacao[melhor_idx], peso_objetos, valor_objetos, peso_maximo_mochila)
print("melhor genotipo:", populacao[melhor_idx])
print("Itens escolhidos:", itens_escolhidos)
print("geração:", geracao)
print("fitness ideal:", fitness_ideal)
print("melhor fitness inicial:", melhor_fitnes_inicial)
print("melhor fitness encontrado", melhor_fitness_final)
print("tempo de execução:", final - inicio)
    