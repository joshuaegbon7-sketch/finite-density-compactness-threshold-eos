import matplotlib
matplotlib.use("Agg")

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

G = 6.67430e-11
c = 2.99792458e8
M_sun = 1.98847e30

r0 = 1.25e-15
m_n = 1.6749275e-27

DATA_DIR = "data"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def Mcrit_scaling(lam):
    return np.sqrt(
        (lam**3 * r0**3 * c**6)
        /
        (G**3 * m_n)
    )

def load_compose_mr(eos_name, folder):

    path = os.path.join(folder, "eos.mr")

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing eos.mr file: {path}"
        )

    data = np.loadtxt(path, comments="#")

    R_km = data[:, 0]
    M_Msun = data[:, 1]

    R_m = R_km * 1000.0
    M_kg = M_Msun * M_sun

    compactness = (
        G * M_kg
        /
        (R_m * c**2)
    )

    return pd.DataFrame({
        "EOS": eos_name,
        "R_km": R_km,
        "M_Msun": M_Msun,
        "compactness": compactness,
    })

############################################################
# Locate EOS folders
############################################################

eos_paths = {}

for eos_name in ["APR", "SLY4", "DD2"]:

    folder = os.path.join(DATA_DIR, eos_name)

    if os.path.exists(os.path.join(folder, "eos.mr")):
        eos_paths[eos_name] = folder
    else:
        print(f"Warning: missing {eos_name}/eos.mr")

############################################################
# Load EOS sequences
############################################################

all_mr = []
summary_rows = []

for eos_name, folder in eos_paths.items():

    df = load_compose_mr(eos_name, folder)

    all_mr.append(df)

    idx = df["M_Msun"].idxmax()
    row = df.loc[idx]

    summary_rows.append({
        "EOS": eos_name,
        "Mmax_TOV_Msun": row["M_Msun"],
        "Rmax_km": row["R_km"],
        "Cmax": row["compactness"],
    })

if not summary_rows:
    raise RuntimeError(
        "No EOS data found. "
        "Run 01_download_compose_eos.py first."
    )

summary = pd.DataFrame(summary_rows)

############################################################
# Add scaling-threshold comparisons
############################################################

for lam in [0.18, 0.20, 0.22]:

    Mcrit = Mcrit_scaling(lam) / M_sun

    summary[f"Mcrit_lambda_{lam:.2f}"] = Mcrit

    summary[f"Delta_lambda_{lam:.2f}"] = (
        Mcrit
        -
        summary["Mmax_TOV_Msun"]
    )

summary = summary.sort_values("Mmax_TOV_Msun")

print(summary)

summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "compose_mr_scaling_comparison_all.csv"
    ),
    index=False
)

############################################################
# Mass-radius figure
############################################################

plt.figure(figsize=(8, 6))

for df in all_mr:

    plt.plot(
        df["R_km"],
        df["M_Msun"],
        linewidth=2.8,
        label=df["EOS"].iloc[0]
    )

for lam in [0.18, 0.20, 0.22]:

    plt.axhline(
        Mcrit_scaling(lam) / M_sun,
        linestyle="--",
        linewidth=2.0,
        label=f"Scaling λ={lam:.2f}"
    )

plt.xlabel("Radius R (km)")
plt.ylabel("Mass M ($M_\odot$)")

plt.title(
    "CompOSE Mass-Radius Curves "
    "vs Scaling Thresholds"
)

plt.xlim(8, 16)
plt.ylim(1.0, 2.6)

plt.legend(fontsize=11)

plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "compose_mr_scaling_thresholds_all.png"
    ),
    dpi=400,
    bbox_inches="tight"
)

plt.close()

############################################################
# Compactness figure
############################################################

plt.figure(figsize=(8, 6))

for df in all_mr:

    plt.plot(
        df["M_Msun"],
        df["compactness"],
        linewidth=2.8,
        label=df["EOS"].iloc[0]
    )

plt.xlabel("Mass M ($M_\odot$)")
plt.ylabel("Compactness GM/(Rc$^2$)")

plt.title(
    "Compactness Along "
    "CompOSE Mass-Radius Curves"
)

plt.xlim(1.0, 2.5)
plt.ylim(0.10, 0.34)

plt.legend(fontsize=11)

plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "compose_compactness_curves_all.png"
    ),
    dpi=400,
    bbox_inches="tight"
)

plt.close()

############################################################
# Done
############################################################

print("Saved:")
print("outputs/compose_mr_scaling_comparison_all.csv")
print("outputs/compose_mr_scaling_thresholds_all.png")
print("outputs/compose_compactness_curves_all.png")
