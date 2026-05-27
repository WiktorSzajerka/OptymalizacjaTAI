import pandas as pd
import matplotlib.pyplot as plt



plot_cfg = [
    ("RS",   r"tsp\results\rs_best_value.csv",   "blue",  "o"),
    ("SA",   r"tsp\results\sa_best_value.csv",   "red",   "s"),
    ("LBSA", r"tsp\results\lbsa_best_value.csv", "green", "^"),
]

fig, ax = plt.subplots(figsize=(10, 5))
for label, csv_file, color, marker in plot_cfg:
    df = pd.read_csv(csv_file, index_col="n_cities")
    means = df["mean"]
    stds  = df["std"]
    x     = df.index.values
    ax.plot(x[:18], means[:18], label=label, color=color,
            marker=marker, markersize=6, linewidth=1.5)
    ax.fill_between(x[:18], means[:18] - stds[:18], means[:18] + stds[:18], alpha=0.15, color=color)



ax.set_xlabel("Liczba miast (n_cities)")
ax.set_ylabel("Długość ścieżki (best value)")
ax.set_title("Porównanie algorytmów, średnia ± odchylenie std (10 uruchomień)")
ax.legend()
plt.tight_layout()
plt.savefig("comparison_best_value_small.png", dpi=150)
plt.show()
print("Saved comparison_best_value.png")


fig, ax = plt.subplots(figsize=(10, 5))
for label, csv_file, color, marker in plot_cfg:
    df = pd.read_csv(csv_file, index_col="n_cities")
    means = df["mean"]
    stds  = df["std"]
    x     = df.index.values
    ax.plot(x, means, label=label, color=color,
            marker=marker, markersize=6, linewidth=1.5)
    ax.fill_between(x, means - stds, means + stds, alpha=0.15, color=color)



ax.set_xlabel("Liczba miast (n_cities)")
ax.set_ylabel("Długość ścieżki (best value)")
ax.set_title("Porównanie algorytmów, średnia ± odchylenie std (10 uruchomień)")
ax.legend()
plt.tight_layout()
plt.savefig("comparison_best_value1.png", dpi=150)
plt.show()
print("Saved comparison_best_value.png")

# ── Plot 2: number of iterations vs n_cities (read from CSV, with markers) ───
iter_cfg = [
    ("RS",   r"tsp\results\rs_iterations.csv",   "blue",  "o"),
    ("SA",   r"tsp\results\sa_iterations.csv",   "red",   "s"),
    ("LBSA", r"tsp\results\lbsa_iterations.csv", "green", "^"),
]

fig, ax = plt.subplots(figsize=(10, 5))
for label, csv_file, color, marker in iter_cfg:
    df = pd.read_csv(csv_file, index_col="n_cities")
    means = df["mean"]
    stds  = df["std"]
    x     = df.index.values
    ax.plot(x, means, label=label, color=color,
            marker=marker, markersize=6, linewidth=1.5)
    ax.fill_between(x, means - stds, means + stds, alpha=0.15, color=color)

ax.set_xlabel("Liczba miast (n_cities)")
ax.set_ylabel("Liczba iteracji")
ax.set_title("Liczba iteracji, średnia ± odchylenie std (10 uruchomień)")
ax.legend()
plt.tight_layout()
plt.savefig("comparison_iterations.png", dpi=150)
plt.show()
print("Saved comparison_iterations.png")


fig, ax = plt.subplots(figsize=(10, 5))
for label, csv_file, color, marker in iter_cfg:
    df = pd.read_csv(csv_file, index_col="n_cities")
    means = df["mean"]
    stds  = df["std"]
    x     = df.index.values
    ax.plot(x[:18], means[:18], label=label, color=color,
            marker=marker, markersize=6, linewidth=1.5)
    ax.fill_between(x[:18], means[:18] - stds[:18], means[:18] + stds[:18], alpha=0.15, color=color)

ax.set_xlabel("Liczba miast (n_cities)")
ax.set_ylabel("Liczba iteracji")
ax.set_title("Liczba iteracji, średnia ± odchylenie std (10 uruchomień)")
ax.legend()
plt.tight_layout()
plt.savefig("comparison_iterations_small.png", dpi=150)
plt.show()
print("Saved comparison_iterations.png")