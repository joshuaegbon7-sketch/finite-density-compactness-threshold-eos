import os
import numpy as np
import pandas as pd

# ============================================================
# Finite-Density Compactness Threshold Scan
# ============================================================

# Physical constants
G = 6.67430e-11
c = 2.99792458e8
M_sun = 1.98847e30

# Nuclear-scale parameters
r0 = 1.25e-15
m_n = 1.6749275e-27

# Output directory
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Critical mass scaling relation
# ============================================================

def Mcrit_scaling(lam):
    """
    Finite-density compactness-threshold scaling relation.
    Returns critical mass in kg.
    """
    return np.sqrt(
        (lam**3 * r0**3 * c**6) /
        (G**3 * m_n)
    )

# ============================================================
# Lambda scan
# ============================================================

lambda_values = np.array([
    0.15,
    0.18,
    0.20,
    0.22,
    0.25,
    0.28,
    0.30,
    0.32,
    0.35
])

rows = []

for lam in lambda_values:

    Mcrit_kg = Mcrit_scaling(lam)
    Mcrit_Msun = Mcrit_kg / M_sun

    rows.append({
        "lambda": round(lam, 3),
        "Mcrit_kg": Mcrit_kg,
        "Mcrit_Msun": round(Mcrit_Msun, 6),
    })

# ============================================================
# Create dataframe
# ============================================================

df = pd.DataFrame(rows)

# ============================================================
# Display results
# ============================================================

print("
Finite-Density Compactness Threshold Scan
")
print(df)

# ============================================================
# Save CSV
# ============================================================

csv_path = os.path.join(
    OUTPUT_DIR,
    "scaling_threshold_table.csv"
)

df.to_csv(
    csv_path,
    index=False
)

print("
Saved:")
print(csv_path)
