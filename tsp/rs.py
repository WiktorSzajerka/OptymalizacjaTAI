from RandomNumberGenerator import RandomNumberGenerator
import numpy as np

rng = RandomNumberGenerator(seedVaule=1)

def generator(matrix_size):
    dist_values = np.zeros((matrix_size, matrix_size))
    for i in range(matrix_size):
        for j in range(matrix_size):
            if i != j:
                dist_values[i, j] = rng.nextInt(low=1, high=30)
    
    return dist_values

def objective_fun(dist_matrix, solution):   # funkcja celu
    value = 0
    for i in range(len(solution)):
        value += dist_matrix[solution[i-1], solution[i]]

    return value

def next_solution(solution):    # generowanie kolejnego rozwiązania z pośród sąsiadów
    new_sol = solution[:]
    i = np.random.randint(low=0, high=len(solution))
    j = np.random.randint(low=0, high=len(solution))
    if i == j:
        j = j - np.random.randint(low=1, high=len(solution) - 1)
    new_sol[i], new_sol[j] = new_sol[j], new_sol[i]
    return new_sol



def random_search(n_cities):
    dist_values = generator(n_cities)
    #print("dane wejściowe", dist_values)

    # generowanie pierwszego rozwiązania
    solution = []
    for i in range(n_cities):
        solution.append(i)

    np.random.shuffle(solution)

    # random search
    cnt = 0
    i = 0
    best_value = objective_fun(dist_values, solution)
    while cnt <= len(solution)*2:
        i += 1
        new_solution = next_solution(solution)
        new_value = objective_fun(dist_values, solution)
        if new_value < best_value:
            solution = new_solution
            best_value = new_value
            cnt = 0
        else:
            cnt += 1

    return solution, best_value, i



# analiza pojedynczego uruchomienia
"""
solution, best_value, iter = random_search(50)


print("rozwiązanie ", solution)
print("długość ścieżki: ", best_value)
"""




