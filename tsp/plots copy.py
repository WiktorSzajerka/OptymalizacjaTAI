import pandas as pd
import matplotlib.pyplot as plt



# ── Plot 2: number of iterations vs n_cities (read from CSV, with markers) ───
iter_cfg = [
    ("SA",   r"tsp\results\sa_best_iter.csv",   "red",   "s"),
    ("LBSA", r"tsp\results\lbsa_best_iter.csv", "green", "^"),
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
ax.set_title("Liczba iteracji po których nie było poprawy najlepszej wartości")
ax.legend()
plt.tight_layout()
plt.savefig("comparison_best_iter.png", dpi=150)
plt.show()
print("Saved comparison_iterations.png")

