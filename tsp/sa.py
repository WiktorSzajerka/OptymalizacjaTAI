from RandomNumberGenerator import RandomNumberGenerator
import numpy as np
from copy import copy
import matplotlib.pyplot as plt

rng = RandomNumberGenerator(seedVaule=1)

u = 0.99
T = 100


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
    i = np.random.randint(low=1, high=len(solution))
    j = np.random.randint(low=1, high=len(solution))
    if i == j:
        j = j - np.random.randint(low=1, high=len(solution) - 1)
    new_sol[i], new_sol[j] = new_sol[j], new_sol[i]
    return new_sol

def accept_solution(cur_value, new_value, T):
    e = new_value - cur_value
    p = np.exp(-(e/T))
    rng_uni = np.random.uniform()
    if p > rng_uni:
        return True
    else:
        return False
            

def simulated_anealing(n_cities, u, T): # u = wsp. chłodzeia, T = temperatura

    dist_values = generator(n_cities)
    n_iter = 100000
    val_arr = np.zeros(n_iter)
    best_val_arr = np.zeros(n_iter)
    t_arr = np.zeros(n_iter)
    #print("dane wejściowe", dist_values)

    # generowanie pierwszego rozwiązania
    solution = []
    for i in range(n_cities):
        solution.append(i)

    np.random.shuffle(solution)


    cnt = 0
    i = 0
    cur_value = objective_fun(dist_values, solution)
    best_value = copy(cur_value)
    val_arr[i] = cur_value
    best_val_arr[i] = best_value
    t_arr[i] = T
    while T > 0.01 and i < n_iter - 1:
        new_solution = next_solution(solution)
        new_value = objective_fun(dist_values, solution)
        if new_value < cur_value:
            solution = new_solution
            cur_value = new_value
            cnt = 0
            if cur_value < best_value:
                best_value = copy(cur_value)
                
        else:
            accept = accept_solution(cur_value, new_value, T)
            if accept == True:
                solution = new_solution
                cur_value = new_value
                cnt = 0
            else:
                cnt += 1
        
        T *= u
        i += 1
        val_arr[i] = cur_value
        best_val_arr[i] = best_value
        t_arr[i] = T


    i += 1
    return solution, best_value, val_arr, best_val_arr, t_arr, i
    

# analiza pojedynczego uruchomienia
"""
solution, best_value, val_arr, best_val_arr, t_arr, i = simulated_anealing(50, 0.99, 540)

fig, ax = plt.subplots()
ax.plot(np.linspace(1, i, i), best_val_arr[:i], color='blue', label="najlepsze rozwiązanie")
ax.plot(np.linspace(1, i, i), val_arr[:i], color='red', label="aktualne rozwiązanie")
ax.legend()
plt.xlabel("liczba iteracji")
plt.ylabel("długość ścieżki")
plt.show()


fig, ax = plt.subplots()
ax.plot(np.linspace(1, i, i), t_arr[:i], color='blue', label="najlepsze rozwiązanie")
plt.xlabel("liczba iteracji")
plt.ylabel("temperatura")
plt.show()
"""
