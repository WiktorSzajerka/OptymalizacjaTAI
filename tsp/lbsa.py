from RandomNumberGenerator import RandomNumberGenerator
import numpy as np
from copy import copy
import matplotlib.pyplot as plt

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
    i = np.random.randint(low=1, high=len(solution))
    j = np.random.randint(low=1, high=len(solution))
    if i == j:
        j = j - np.random.randint(low=1, high=len(solution) - 1)
    new_sol[i], new_sol[j] = new_sol[j], new_sol[i]
    return new_sol

def accept_solution(cur_value, new_value, T):
    if T <= 0:
        return False, None
    e = new_value - cur_value
    p = np.exp(-(e/T))
    r = np.random.uniform()
    if p > r:
        new_temp = (T - (new_value - cur_value))/r
        return True, new_temp
    else:
        return False, None
    
           

def simulated_anealing(n_cities, init_prob, temp_list_len): # u = wsp. chłodzeia, T = temperatura

    dist_values = generator(n_cities)
    n_iter = 500
    val_arr = np.zeros(n_iter*n_cities+1)
    best_val_arr = np.zeros(n_iter*n_cities+1)
    print("dane wejściowe", dist_values)

    # generowanie pierwszego rozwiązania
    solution = []
    for i in range(n_cities):
        solution.append(i)

    np.random.shuffle(solution)
 
    i = 0
    temp_list = []
    cur_value = objective_fun(dist_values, solution)
    best_value = copy(cur_value)
    # tworzenie listy temperatur
    for i in range(temp_list_len):
        new_solution = next_solution(solution)
        new_value = objective_fun(dist_values, new_solution)
        if new_value < best_value:
            best_value = copy(new_value)
        temp = (-np.abs(new_value - best_value))/np.log2(init_prob)
        temp_list.append(temp)

    val_arr[0] = best_value
    best_val_arr[0] = best_value
        
    i = 0
    ind = 0

    while i < n_iter:
        cnt = 0
        t = max(temp_list)
        new_temps = []
        while cnt < n_cities:
            new_temps = []
            new_solution = next_solution(solution)
            new_value = objective_fun(dist_values, solution)
            if new_value < cur_value:
                solution = new_solution
                cur_value = new_value
                if cur_value < best_value:
                    best_value = copy(cur_value)
                    
            else:
                accept, temp = accept_solution(cur_value, new_value, t)
                if accept == True:
                    solution = new_solution
                    cur_value = new_value
                    new_temps.append(temp)

            
            cnt += 1
            ind += 1
            val_arr[ind] = cur_value
            best_val_arr[ind] = best_value

        if new_temps:
            temp_list[temp_list.index(t)] = np.mean(new_temps)
        i += 1

    print("rozwiązanie ", solution)
    print("długość ścieżki: ", best_value)
    print(i)
    return solution, best_value, val_arr, best_val_arr
    


solution, best_value, val_arr, best_val_arr =simulated_anealing(500, 0.1, 20)


fig, ax = plt.subplots()
ax.plot(np.linspace(1, best_val_arr.size, best_val_arr.size), best_val_arr, color='blue', label="najlepsze rozwiązanie")
ax.plot(np.linspace(1, val_arr.size, val_arr.size), val_arr, color='red', label="aktualne rozwiązanie")
ax.legend()
plt.show()

