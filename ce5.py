import numpy as np

def generate_binary_combinations(n):
    # Calculate the total number of combinations (2^n)
    num_combinations = 2**n
    
    # Initialize a 2D array to store combinations
    combinations = np.zeros((num_combinations, n), dtype=int)
    
    # Fill the array with binary combinations
    for i in range(num_combinations):
        binary_repr = f"{i:0{n}b}"  # Convert the index 'i' to binary with 'n' digits
        combinations[i] = [int(bit) for bit in binary_repr]  # Store as integers in the array
    
    return combinations

def filter_combinations(combinations, max_itens):
    # Count the number of ones in each row
    num_ones = np.sum(combinations, axis=1)
    
    # Filter combinations based on the number of ones
    filtered_combinations = combinations[num_ones <= max_itens]
    
    return filtered_combinations

def calcula_fitness_mochila(genotipo, peso_objetos, valor_objetos, peso_maximo_mochila):

    peso_total_mochila = sum(genotipo*peso_objetos)
    valor_total_objetos = sum(genotipo*valor_objetos)
    if (peso_total_mochila > peso_maximo_mochila):
        fitness = 0
    else:
        fitness = valor_total_objetos
    return fitness

# Problem parameters definitions
peso_objetos = [160, 350, 192, 2200, 333]
valor_objetos = [150, 60, 30, 500, 40]
item_name = ['Headphone', 'Coffee mug','Water bottle','Laptop','Notepad']
peso_maximo_mochila = 3000
max_itens_allowed = 3
tamanho_genoma = len(peso_objetos)

# Generate all possible combinations
binary_combinations = generate_binary_combinations(len(peso_objetos))

possibilidades = filter_combinations(binary_combinations, max_itens_allowed)

fitness_valor_objetos = []
for i in range(len(possibilidades)):
    fitness_valor_objetos.append(calcula_fitness_mochila(possibilidades[i], peso_objetos, valor_objetos, peso_maximo_mochila))

print(fitness_valor_objetos)

melhor_fitness = max(fitness_valor_objetos)
melhor_idx = fitness_valor_objetos.index(max(fitness_valor_objetos))

itens_escolhidos = []
for i in range(tamanho_genoma):
    if(possibilidades[melhor_idx][i]) == 1:
        itens_escolhidos.append(item_name[i])

print("melhor genotipo:", possibilidades[melhor_idx])
print("Itens escolhidos:", itens_escolhidos)
print("melhor fitness encontrado:", melhor_fitness)
    