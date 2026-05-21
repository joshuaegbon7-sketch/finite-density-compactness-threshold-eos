import matplotlib
matplotlib.use("Agg")

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

G = 6.67430e-11
c = 2.99792458e8
M_sun = 1.98847e30

DATA_DIR = "data"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_compose_mr(eos_name, folder):

    path = os.path.join(folder, "eos.mr")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing eos.mr file: {path}")

    data = np.loadtxt(path, comments="#")

    R_km = data[:, 0]
    M_Msun = data[:, 1]

    R_m = R_km * 1000.0
    M_kg = M_Msun * M_sun

    compactness = G * M_kg / (R_m * c**2)

    return pd.DataFrame({
        "EOS": eos_name,
        "R_km": R_km,
        "M_Msun": M_Msun,
        "compactness": compactness,
    })

def tidal_lambda_from_compactness(C, k2):
    return (2.0 / 3.0) * k2 * C**(-5)

eos_paths = {}

for eos_name in ["APR", "SLY4", "DD2"]:

    folder = os.path.join(DATA_DIR, eos_name)

    if os.path.exists(os.path.join(folder, "eos.mr")):
        eos_paths[eos_name] = folder
    else:
        print(f"Warning: missing {eos_name}/eos.mr")

all_mr = []

for eos_name, folder in eos_paths.items():

    df = load_compose_mr(eos_name, folder)

    for k2 in [0.05, 0.08, 0.10, 0.12]:

        df[f"Lambda_k2_{k2:.2f}"] = (
            tidal_lambda_from_compactness(
                df["compactness"],
                k2
            )
        )

    all_mr.append(df)

if not all_mr:
    raise RuntimeError("No EOS data found. Run 01_download_compose_eos.py first.")

summary_rows = []

for df in all_mr:

    eos_name = df["EOS"].iloc[0]

    idx_14 = (df["M_Msun"] - 1.4).abs().idxmin()
    row14 = df.loc[idx_14]

    idx_max = df["M_Msun"].idxmax()
    rowmax = df.loc[idx_max]

    summary_rows.append({
        "EOS": eos_name,
        "M_near_1p4_Msun": row14["M_Msun"],
        "R_near_1p4_km": row14["R_km"],
        "C_near_1p4": row14["compactness"],
        "Lambda_1p4_k2_0p05": row14["Lambda_k2_0.05"],
        "Lambda_1p4_k2_0p08": row14["Lambda_k2_0.08"],
        "Lambda_1p4_k2_0p10": row14["Lambda_k2_0.10"],
        "Lambda_1p4_k2_0p12": row14["Lambda_k2_0.12"],
        "Mmax_Msun": rowmax["M_Msun"],
        "Rmax_km": rowmax["R_km"],
        "Cmax": rowmax["compactness"],
        "Lambda_Mmax_k2_0p08": rowmax["Lambda_k2_0.08"],
    })

summary = pd.DataFrame(summary_rows)

print(summary)

summary.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "approx_tidal_deformability_summary.csv"
    ),
    index=False
)

############################################################
# Full tidal deformability curves
############################################################

plt.figure(figsize=(8, 6))

for df in all_mr:

    eos_name = df["EOS"].iloc[0]

    plt.plot(
        df["M_Msun"],
        df["Lambda_k2_0.08"],
        linewidth=2.8,
        label=f"{eos_name}"
    )

plt.yscale("log")

plt.xlabel("Mass M ($M_\odot$)")
plt.ylabel("Approximate $\Lambda$")

plt.title("Approximate Tidal Deformability")

plt.legend(fontsize=11)
plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "approx_lambda_vs_mass.png"
    ),
    dpi=400,
    bbox_inches="tight"
)

plt.close()

############################################################
# Neutron-star mass range
############################################################

plt.figure(figsize=(8, 6))

for df in all_mr:

    eos_name = df["EOS"].iloc[0]

    mask = (
        (df["M_Msun"] >= 1.0)
        &
        (df["M_Msun"] <= 2.2)
    )

    plt.plot(
        df.loc[mask, "M_Msun"],
        df.loc[mask, "Lambda_k2_0.08"],
        linewidth=2.8,
        label=f"{eos_name}"
    )

plt.yscale("log")

plt.xlabel("Mass M ($M_\odot$)")
plt.ylabel("Approximate $\Lambda$")

plt.title(
    "Approximate Tidal Deformability "
    "in Neutron-Star Mass Range"
)

plt.xlim(1.0, 2.25)
plt.ylim(10, 3000)

plt.legend(fontsize=11)
plt.grid(True)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "approx_lambda_ns_range.png"
    ),
    dpi=400,
    bbox_inches="tight"
)

plt.close()

print("Saved:")
print("outputs/approx_tidal_deformability_summary.csv")
print("outputs/approx_lambda_vs_mass.png")
print("outputs/approx_lambda_ns_range.png")
