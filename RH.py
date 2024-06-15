import numpy as np
import time
import random

def fitness(genotipo):
    '''
    Calcula o valor da função fitness para o individuo

    Retorna valor da fitness caso as restrições sejam obedecidas, caso contrário retorna 0
    ''' 
    value = 0
    if verifica_restricoes(genotipo):
        for i in range(len(genotipo)):
            value = value + horas[i] * genotipo[i]
            if value > horas_max:
                return 0
        return value
    else:
        return 0


def verifica_restricoes(array):
    '''
    Verifica se alguma restrição de quantidade de individuos foi desobedecida em um array

    retorna True caso as restrições sejam bem obedecidas, retorna False caso alguma delas seja quebrada
    '''
    for i in range(len(array)):
        if array[i] > max_qntd[i] or array[i] < 1:
            return False
    return True


# Restrições
horas = [160, 96, 64, 40]
horas_max = 800
max_qntd = [5, 4, 3, 2]
len_gen = len(max_qntd)
max_IC = 5 
max_Mest = 4 
max_Dout = 3 
max_Prof = 2 
min_of_each = 1 

# Definição dos parâmetros
taxa_mutacao = 0.05
tamanho_populacao = 100
fitness_ideal = horas_max * 0.98 # vou estimar como 95% das horas máximas pq sim, sei lá, se der errado eu mudo dps foda-se
geracao_limite = 1000

# Gerar populações iniciais de cada um dos tipos de indivíduos
populacao = []
for i in range(tamanho_populacao - 1):

    IC = random.randint(min_of_each, max_qntd[0])
    mest = random.randint(min_of_each, max_qntd[1])
    dout = random.randint(min_of_each, max_qntd[2])
    prof = random.randint(min_of_each, max_qntd[3])

    individuo = [IC, mest, dout, prof]
    populacao.append(individuo)


vetor_fitness_inicial = []
for i in range(tamanho_populacao - 1):
    vetor_fitness_inicial.append(fitness(populacao[i]))

# Melhor genotipo inicial
melhor_fitnes_inicial = max(vetor_fitness_inicial)

inicio = time.time()
# Loop de evolução
geracao = 0
for gen in range(0, geracao_limite):
    vetor_fitness = []

    for i in range(tamanho_populacao - 1):
        vetor_fitness.append(fitness(populacao[i]))
    
    # Encontra melhor fitness
    melhor_fitness = max(vetor_fitness)
    melhor_idx = vetor_fitness.index(max(vetor_fitness))

    melhor_genotipo = populacao[melhor_idx]
    
    # Verifica condição de parada
    if melhor_fitness >= fitness_ideal:
        geracao = gen+1
        break

    # Definição dos pais
    size = (tamanho_populacao, len_gen)
    pais = np.zeros(size, dtype=int)

    # Pais definidos por quem tem a melhor fitness
    for j in range(tamanho_populacao - 1):
        index_pai_1 = np.random.randint(tamanho_populacao - 1) # primeiro indexador aleatorio
        index_pai_2 = np.random.randint(tamanho_populacao - 1) # segundo indexador aleatorio
        if vetor_fitness[index_pai_1] > vetor_fitness[index_pai_2]:
            pais[j] = populacao[index_pai_1]
        else:
            pais[j] = populacao[index_pai_2]

    # Crossover e elitismo
    offspring = np.zeros(size, dtype=int)
    offspring[0] = melhor_genotipo

    for k in range(1, tamanho_populacao):
        # Random crossover gene point
        ponto_de_crossover = np.random.randint(len_gen)
        index_pai_1 = np.random.randint(tamanho_populacao)
        index_pai_2 = np.random.randint(tamanho_populacao)
        pai_1 = pais[index_pai_1]
        pai_2 = pais[index_pai_2]

        # Apply crossover
        offspring[k, :ponto_de_crossover] = pai_1[:ponto_de_crossover]
        offspring[k, ponto_de_crossover:] = pai_2[ponto_de_crossover:]

    # Mutation
    for l in range(1, tamanho_populacao):
        for m in range(len_gen):
            if np.random.rand() < taxa_mutacao:
                offspring[l][m] = np.random.randint(4) 

    # Update population
    populacao = offspring
    geracao = gen+1

final = time.time()

vetor_fitness_final = []
for i in range(tamanho_populacao - 1):
        vetor_fitness_final.append(fitness(populacao[i]))

# Best genotype
melhor_idx = vetor_fitness_final.index(max(vetor_fitness_final))


melhor_fitness_final = fitness(populacao[melhor_idx])
print("Individuos escolhidos: ", populacao[melhor_idx][0], "Alunos de IC, ",populacao[melhor_idx][1], "Mestrandos, ",populacao[melhor_idx][2], "Doutorandos", populacao[melhor_idx][3], "Professores orientadores",)
print("geração:", geracao)
print("fitness ideal:", fitness_ideal)
print("melhor fitness inicial:", melhor_fitnes_inicial)
print("melhor fitness encontrado", melhor_fitness_final)
print("tempo de execução:", final - inicio)
    