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
        for i in range(len(genotipo) - 1):
            if genotipo[i] < 5:
                value += horas[genotipo[i]]
                if value > 800:
                    return 0
        return value
    else:
        return 0


def verifica_restricoes(array):
    '''
    Verifica se alguma restrição de quantidade de individuos foi desobedecida em um array

    retorna True caso as restrições sejam bem obedecidas, retorna False caso alguma delas seja quebrada
    '''
    if count_ind(0, array) > 5 or count_ind(0, array) < 1 or count_ind(1, array) > 4 or count_ind(1, array) < 1 or count_ind(2, array) > 3 or count_ind(2, array) < 1 or count_ind(3, array) > 2 or count_ind(3, array) < 1:
        return False
    return True

def count_ind(id, array):
    '''
    Verifica a quantidade de individuos com um (id) em um determinado array de individuos

    retorna a quantidade
    '''
    qntd = 0
    for i in range(len(array)):
        if array[i] == id:
            qntd += 1

    return qntd

# Tipos de individuos, ID's dos mesmos e horas mensais.
ind_type = ['Aluno_IC', 'Aluno_mestrado', 'Aluno_doutorado', 'Prof_orientador']
ind_id = [0, 1, 2, 3]
horas = [160, 96, 64, 40]

# Restrições
horas_max = 800
max_IC = 5 # id 0
max_Mest = 4 # id 1
max_Dout = 3 # id 2
max_Prof = 2 # id 3
min_of_each = 1 
max_inds = max_IC + max_Mest + max_Dout + max_Prof

# Definição dos parâmetros
taxa_mutacao = 0.05
tamanho_populacao = 10
fitness_ideal = horas_max # vou estimar como 95% das horas máximas pq sim, sei lá, se der errado eu mudo dps foda-se
geracao_limite = 10000

# Gerar populações iniciais de cada um dos tipos de indivíduos
populacao = []
for i in range(tamanho_populacao):

    length = random.randint(min_of_each, max_IC)
    IC_array = [0] * length
    length = random.randint(min_of_each, max_Mest)
    mest_array = [1] * length
    length = random.randint(min_of_each, max_Dout)
    dout_array = [2] * length
    length = random.randint(min_of_each, max_Prof)
    prof_array = [3] * length

    individuo = IC_array + mest_array + dout_array + prof_array
    length = max_inds - len(individuo)
    void_array = [4521557] * length # preencher o array do individuo pra poder criar a populacao sem problemas com relação à tamanhos diferentes de array
    individuo += void_array
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

    for i in range(tamanho_populacao):
        vetor_fitness.append(fitness(populacao[i]))
    
    # Encontra melhor fitness
    melhor_fitness = max(vetor_fitness)
    melhor_idx = vetor_fitness.index(max(vetor_fitness))

    melhor_genotipo = populacao[melhor_idx]
    
    # Verifica condição de parada
    if melhor_fitness >= fitness_ideal:
        geracao = gen+1
        break

    # Parents definition
    size = (tamanho_populacao, max_inds)
    pais = np.zeros(size, dtype=int)

    # Pais definidos por quem tem a melhor fitness
    for j in range(tamanho_populacao):
        index_pai_1 = np.random.randint(tamanho_populacao)
        index_pai_2 = np.random.randint(tamanho_populacao)
        if vetor_fitness[index_pai_1] > vetor_fitness[index_pai_2]:
            pais[j] = populacao[index_pai_1]
        else:
            pais[j] = populacao[index_pai_2]

    # Crossover e elitismo
    offspring = np.zeros(size, dtype=int)
    offspring[0] = melhor_genotipo

    for k in range(1, tamanho_populacao):
        # Random crossover gene point
        ponto_de_crossover = np.random.randint(max_inds)
        index_pai_1 = np.random.randint(tamanho_populacao)
        index_pai_2 = np.random.randint(tamanho_populacao)
        pai_1 = pais[index_pai_1]
        pai_2 = pais[index_pai_2]

        # Apply crossover
        offspring[k, :ponto_de_crossover] = pai_1[:ponto_de_crossover]
        offspring[k, ponto_de_crossover:] = pai_2[ponto_de_crossover:]

    # Mutation
    for l in range(1, tamanho_populacao):
        for m in range(max_inds):
            if np.random.rand() < taxa_mutacao:
                offspring[l][m] = np.random.randint(4)

    # Update population
    populacao = offspring
    geracao = gen+1

final = time.time()

vetor_fitness_final = []
for i in range(tamanho_populacao):
        vetor_fitness_final.append(fitness(populacao[i]))

# Best genotype
melhor_idx = vetor_fitness_final.index(max(vetor_fitness_final))

Individuos_finais = []
for i in range(len(populacao[melhor_idx])):
    if populacao[melhor_idx][i] < 4:
        Individuos_finais.append(ind_type[populacao[melhor_idx][i]])

melhor_fitness_final = fitness(populacao[melhor_idx])
print("Individuos escolhidos:", Individuos_finais)
print("geração:", geracao)
print("fitness ideal:", fitness_ideal)
print("melhor fitness inicial:", melhor_fitnes_inicial)
print("melhor fitness encontrado", melhor_fitness_final)
print("tempo de execução:", final - inicio)
    