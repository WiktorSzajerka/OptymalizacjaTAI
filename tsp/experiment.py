from rs import random_search
from sa import simulated_anealing
from lbsa import list_based_simulated_anealing
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

small_n_cities = list(np.linspace(5, 90, 18, dtype=int))
large_n_cities = list(np.linspace(100, 1000, 10, dtype=int))
all_n_cities = small_n_cities + large_n_cities
n_sizes = len(all_n_cities)
n_runs = 10

# lista najlepszych wartości
rs_list_val       = np.zeros((n_sizes, n_runs))
sa_list_val       = np.zeros((n_sizes, n_runs))
lbsa_list_val     = np.zeros((n_sizes, n_runs))

# lista liczby iteracji
rs_list_iter      = np.zeros((n_sizes, n_runs))
sa_list_iter      = np.zeros((n_sizes, n_runs))
lbsa_list_iter    = np.zeros((n_sizes, n_runs))

# lista liczby iteracji po których nie było poprawy najlepszego rozwiązania
rs_list_best_iter   = np.zeros((n_sizes, n_runs))
sa_list_best_iter   = np.zeros((n_sizes, n_runs))
lbsa_list_best_iter = np.zeros((n_sizes, n_runs))

# SA hyperparameters
u1 = 0.99
u2 = 0.999
T = 540

# LBSA hyperparameters
init_prob     = 0.3
temp_list_len2 = 30
temp_list_len1 = 15

for i, n_cities in enumerate(all_n_cities):
    print(f"[{i+1}/{n_sizes}] n_cities={n_cities}")
    if n_cities < 100:
        u = u1
        temp_list_len = temp_list_len1

    else:
        u = u2
        temp_list_len = temp_list_len2
    for j in range(n_runs):

        # --- Random Search ---
        _, best_val, iter_rs = random_search(n_cities)
        rs_list_val[i, j]       = best_val
        rs_list_iter[i, j]      = iter_rs
        rs_list_best_iter[i, j] = iter_rs - n_cities * 2   # iters without improvement

        # --- Simulated Annealing ---
        _, best_val, _, best_val_arr, _, iter_sa = simulated_anealing(n_cities, u, T)
        sa_list_val[i, j]       = best_val
        sa_list_iter[i, j]      = iter_sa
        best_iter_sa = np.argmin(best_val_arr) + 1
        sa_list_best_iter[i, j] = best_iter_sa  # SA stops at T<0.01, last improvement tracked inside

        # --- List-Based Simulated Annealing ---
        _, best_val, val_arr, best_val_arr, _ = list_based_simulated_anealing(
            n_cities, init_prob, temp_list_len
        )
        lbsa_list_val[i, j]       = best_val
        lbsa_list_iter[i, j]      = best_val_arr.size
        # first iteration where best value was last achieved
        best_iter_lbsa = np.argmin(best_val_arr) + 1
        lbsa_list_best_iter[i, j] = best_iter_lbsa


# ── helper: build a tidy DataFrame from a (n_sizes × n_runs) array ──────────
def to_df(arr, metric_name):
    df = pd.DataFrame(arr, index=all_n_cities,
                      columns=[f"run_{j+1}" for j in range(n_runs)])
    df.index.name = "n_cities"
    df["mean"]   = df.mean(axis=1)
    df["std"]    = df.std(axis=1)
    df["min"]    = df.min(axis=1)
    df["max"]    = df.max(axis=1)
    df["metric"] = metric_name
    return df


# ── save per-metric CSVs ─────────────────────────────────────────────────────
datasets = {
    "rs_best_value":       rs_list_val,
    "rs_iterations":       rs_list_iter,
    "rs_best_iter":        rs_list_best_iter,
    "sa_best_value":       sa_list_val,
    "sa_iterations":       sa_list_iter,
    "sa_best_iter":        sa_list_best_iter,
    "lbsa_best_value":     lbsa_list_val,
    "lbsa_iterations":     lbsa_list_iter,
    "lbsa_best_iter":      lbsa_list_best_iter,
}

for name, arr in datasets.items():
    df = to_df(arr, name)
    df.to_csv(f"{name}.csv")
    print(f"Saved {name}.csv")


# ── save a single summary CSV (mean ± std for every algorithm × metric) ─────
summary_rows = []
for name, arr in datasets.items():
    algo, metric = name.split("_", 1)
    mean_vals = arr.mean(axis=1)
    std_vals  = arr.std(axis=1)
    for n, m, s in zip(all_n_cities, mean_vals, std_vals):
        summary_rows.append({
            "algorithm": algo.upper(),
            "metric":    metric,
            "n_cities":  n,
            "mean":      m,
            "std":       s,
        })

summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv("experiment_summary.csv", index=False)
print("Saved experiment_summary.csv")


# ── quick comparison plot (best value vs n_cities) ───────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
for label, arr, color in [
    ("RS",   rs_list_val,   "blue"),
    ("SA",   sa_list_val,   "red"),
    ("LBSA", lbsa_list_val, "green"),
]:
    means = arr.mean(axis=1)
    stds  = arr.std(axis=1)
    ax.plot(all_n_cities, means, label=label, color=color)
    ax.fill_between(all_n_cities, means - stds, means + stds, alpha=0.15, color=color)

ax.set_xlabel("Liczba miast (n_cities)")
ax.set_ylabel("Długość ścieżki (best value)")
ax.set_title("Porównanie algorytmów średnia ± odchylenie std (10 uruchomień)")
ax.legend()
plt.tight_layout()
plt.savefig("comparison_best_value.png", dpi=150)
plt.show()
print("Saved comparison_best_value.png")



