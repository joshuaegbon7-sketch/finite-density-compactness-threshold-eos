# Finite-Density Compactness Threshold

Numerical EOS--TOV and tidal-deformability analysis for finite-density compactness-threshold phenomenology in neutron-star and low-mass compact-object transition regimes.

## EOS Sources

This repository uses validated neutron-star equation-of-state datasets from the CompOSE database:

- APR
- SLY4
- DD2

The EOS download script retrieves the corresponding CompOSE EOS archives and extracts the validated `eos.mr` mass-radius sequences used in the analysis.

## Scripts

### `scripts/01_download_compose_eos.py`

Downloads and extracts validated APR, SLY4, and DD2 EOS datasets from CompOSE.

### `scripts/02_scaling_threshold_scan.py`

Generates phenomenological finite-density compactness-threshold masses using

```text
Mcrit = sqrt(lambda^3 r0^3 c^6 / (G^3 mn))
```

### `scripts/03_compose_eos_tov_comparison.py`

Computes EOS mass-radius sequences, extracts terminal compact-star branches, calculates compactness, and compares maximum TOV masses with finite-density scaling thresholds.

### `scripts/04_approx_tidal_deformability.py`

Computes approximate compactness-based tidal deformability estimates using

```text
Lambda ~= (2/3) k2 C^(-5)
```

## Generated Outputs

The scripts generate CSV tables and publication-quality figures in the `outputs/` directory.

Generated figures include:

- Mass-radius EOS sequences with compactness-threshold overlays
- Compactness evolution curves
- Approximate neutron-star tidal deformability curves
- Full EOS-sequence tidal deformability curves

Key output files include:

```text
outputs/scaling_threshold_table.csv
outputs/compose_mr_scaling_comparison_all.csv
outputs/approx_tidal_deformability_summary.csv
outputs/compose_mr_scaling_thresholds_all.png
outputs/compose_compactness_curves_all.png
outputs/approx_lambda_ns_range.png
outputs/approx_lambda_vs_mass.png
```

## Installation

```bash
pip install -r requirements.txt
```

## Run Order

Run the scripts in the following order:

```bash
python scripts/01_download_compose_eos.py
python scripts/02_scaling_threshold_scan.py
python scripts/03_compose_eos_tov_comparison.py
python scripts/04_approx_tidal_deformability.py
```

## Notes

The analysis uses validated CompOSE `eos.mr` mass-radius sequences rather than reconstructing full thermo--TOV solutions directly from thermodynamic EOS tables.

The tidal-deformability estimate is an approximate compactness-based diagnostic and is not a replacement for full relativistic Love-number integration.

## Citation

If using this repository, cite the corresponding Zenodo archival release.
