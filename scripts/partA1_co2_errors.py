"""
Step 1 — Hindcast evaluation: CO2 emissions
3x3 grid: ME / MAE / RMSE × View 1 (by year) / View 2 (by scenario) / View 3 (overall)
Histograms normalized to density so NZ2070 (n=497) and non-NZ (n=1094) are comparable.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────
# Each user: update SCI_DATA to your local path
SCI_DATA = Path.home() / "PhD" / "4. Modeling" / "Prisma School" / "Scenario_Compass_Initiative_Data"
SCI_FILE = SCI_DATA / "SCI-2025_v1.0_pathways_ensemble_global.xlsx"
FIG_DIR = Path(__file__).parent.parent / "figures"
FIG_DIR.mkdir(exist_ok=True)

VARIABLE = "Emissions|CO2|Energy and Industrial Processes"
EVAL_YEARS = ["2010", "2015", "2020", "2025"]
OBS = {"2010": 33400, "2015": 35400, "2020": 34800, "2025": 38100}

# Colors
C_POS, C_NEG = "#1D9E75", "#D85A30"  # green / orange
C_NZ, C_OTHER, C_ALL = "#D85A30", "#378ADD", "#534AB7"  # orange / blue / purple

# ── Load ────────────────────────────────────────────────────────────────
print("Loading SCI data (this may take 1-2 min)...")
df = pd.read_excel(SCI_FILE, sheet_name="data")
meta = pd.read_excel(SCI_FILE, sheet_name="meta")

s = df[df["Variable"] == VARIABLE].copy()
print(f"  {len(s)} scenarios, {s['Model'].nunique()} models")

# NZ2070 flag
meta["nz_year"] = pd.to_numeric(
    meta["Emissions Diagnostics|Year of Net Zero|CO2"], errors="coerce"
)
meta["nz2070"] = meta["nz_year"].notna() & (meta["nz_year"] <= 2070)
meta["key"] = meta["Model"] + "|||" + meta["Scenario"]
nz_keys = set(meta.loc[meta["nz2070"], "key"])
s["key"] = s["Model"] + "|||" + s["Scenario"]
s["nz2070"] = s["key"].isin(nz_keys)

n_nz = s["nz2070"].sum()
n_other = (~s["nz2070"]).sum()
print(f"  NZ2070: {n_nz} | non-NZ: {n_other}")

# ── Compute errors ──────────────────────────────────────────────────────
for yr in EVAL_YEARS:
    s[f"eps_{yr}"] = OBS[yr] - s[yr]

eps_cols = [f"eps_{yr}" for yr in EVAL_YEARS]
eps_mat = s[eps_cols]

s["ME_j"] = eps_mat.mean(axis=1)
s["MAE_j"] = eps_mat.abs().mean(axis=1)
s["RMSE_j"] = np.sqrt((eps_mat ** 2).mean(axis=1))

# View 3 data
all_eps = eps_mat.values.flatten()
all_eps = all_eps[~np.isnan(all_eps)]
eps_nz = eps_mat[s["nz2070"].values].values.flatten()
eps_nz = eps_nz[~np.isnan(eps_nz)]
eps_other = eps_mat[~s["nz2070"].values].values.flatten()
eps_other = eps_other[~np.isnan(eps_other)]

# ── Print summary ───────────────────────────────────────────────────────
print("\n── View 1: by year ──")
print(f"{'Year':<6} | {'ME':>8} | {'MAE':>8} | {'RMSE':>8}")
print("-" * 40)
for yr in EVAL_YEARS:
    e = s[f"eps_{yr}"].dropna()
    print(f"{yr:<6} | {e.mean():>+8,.0f} | {e.abs().mean():>8,.0f} | {np.sqrt((e**2).mean()):>8,.0f}")

print("\n── View 2: by scenario ──")
print(f"{'':>10} | {'ME_j':>8} | {'MAE_j':>8} | {'RMSE_j':>8}")
print("-" * 42)
for grp, label in [(True, "NZ2070"), (False, "non-NZ"), (None, "All")]:
    sub = s if grp is None else s[s["nz2070"] == grp]
    print(f"{label:>10} | {sub['ME_j'].mean():>+8,.0f} | {sub['MAE_j'].mean():>8,.0f} | {sub['RMSE_j'].mean():>8,.0f}")

print("\n── View 3: overall ──")
print(f"  ME  = {np.mean(all_eps):>+8,.0f} | NZ: {np.mean(eps_nz):>+8,.0f} | non-NZ: {np.mean(eps_other):>+8,.0f}")
print(f"  MAE = {np.mean(np.abs(all_eps)):>8,.0f} | NZ: {np.mean(np.abs(eps_nz)):>8,.0f} | non-NZ: {np.mean(np.abs(eps_other)):>8,.0f}")
print(f"  RMSE= {np.sqrt(np.mean(all_eps**2)):>8,.0f} | NZ: {np.sqrt(np.mean(eps_nz**2)):>8,.0f} | non-NZ: {np.sqrt(np.mean(eps_other**2)):>8,.0f}")

# ── Figure: 3×3 grid ────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 3, figsize=(15, 11))
fig.suptitle(
    f"Hindcast evaluation — {VARIABLE}\n"
    r"$\varepsilon = y_{\mathrm{observed}} - \hat{y}_{\mathrm{projected}}$"
    f"  (Mt CO₂/yr)  |  NZ2070: n={n_nz}, non-NZ: n={n_other}",
    fontsize=12, fontweight="bold", y=1.01,
)

metrics = [
    ("ME", "systematic bias", True),
    ("MAE", "typical error size", False),
    ("RMSE", "penalises large errors", False),
]

for col, (name, subtitle, signed) in enumerate(metrics):

    # ── Row 0: View 1 — by year ──
    ax = axes[0, col]
    if name == "ME":
        vals = [s[f"eps_{yr}"].dropna().mean() for yr in EVAL_YEARS]
    elif name == "MAE":
        vals = [s[f"eps_{yr}"].dropna().abs().mean() for yr in EVAL_YEARS]
    else:
        vals = [np.sqrt((s[f"eps_{yr}"].dropna() ** 2).mean()) for yr in EVAL_YEARS]

    colors = [C_POS if v >= 0 else C_NEG for v in vals] if signed else [C_OTHER if name == "MAE" else C_ALL] * 4
    bars = ax.bar(EVAL_YEARS, vals, color=colors, width=0.55, edgecolor="none", zorder=3)
    if signed:
        ax.axhline(0, color="gray", lw=0.5, ls="--", zorder=1)
    for bar, v in zip(bars, vals):
        offset = max(abs(v) * 0.06, 80)
        label = f"{v:+,.0f}" if signed else f"{v:,.0f}"
        ax.text(bar.get_x() + bar.get_width() / 2,
                v + (offset if v >= 0 or not signed else -offset),
                label, ha="center",
                va="bottom" if (v >= 0 or not signed) else "top", fontsize=9)

    ax.set_title(f"{name} — {subtitle}", fontsize=10, fontweight="bold", loc="left")
    if col == 0:
        ax.set_ylabel("View 1: by year\n(Mt CO₂)", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.15, zorder=0)

    # ── Row 1: View 2 — by scenario (histogram, normalized) ──
    ax = axes[1, col]
    metric_col = f"{name}_j"
    v_nz = s.loc[s["nz2070"], metric_col].dropna().values
    v_other = s.loc[~s["nz2070"], metric_col].dropna().values

    lo = min(v_nz.min(), v_other.min())
    hi = max(v_nz.max(), v_other.max())
    bins = np.arange(np.floor(lo / 500) * 500, np.ceil(hi / 500) * 500 + 500, 500)

    # density=True normalizes area to 1, making NZ and non-NZ comparable
    ax.hist(v_other, bins=bins, density=True, alpha=0.55, color=C_OTHER,
            label=f"non-NZ (n={len(v_other)})", edgecolor="white", lw=0.3, zorder=2)
    ax.hist(v_nz, bins=bins, density=True, alpha=0.55, color=C_NZ,
            label=f"NZ2070 (n={len(v_nz)})", edgecolor="white", lw=0.3, zorder=3)

    # Mean lines
    ax.axvline(np.mean(v_other), color=C_OTHER, lw=1.8, ls="--", zorder=4)
    ax.axvline(np.mean(v_nz), color=C_NZ, lw=1.8, ls="--", zorder=4)

    ax.legend(fontsize=8, loc="upper right")
    ax.set_xlabel(f"{name}$_j$ (Mt CO₂)", fontsize=9)
    if col == 0:
        ax.set_ylabel("View 2: by scenario\n(density)", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.15, zorder=0)

    # ── Row 2: View 3 — overall (horizontal bars) ──
    ax = axes[2, col]
    if name == "ME":
        v3 = [np.mean(all_eps), np.mean(eps_nz), np.mean(eps_other)]
    elif name == "MAE":
        v3 = [np.mean(np.abs(all_eps)), np.mean(np.abs(eps_nz)), np.mean(np.abs(eps_other))]
    else:
        v3 = [np.sqrt(np.mean(all_eps**2)), np.sqrt(np.mean(eps_nz**2)), np.sqrt(np.mean(eps_other**2))]

    labels3 = ["All", "NZ2070", "non-NZ"]
    colors3 = [C_ALL, C_NZ, C_OTHER]
    bars3 = ax.barh(labels3, v3, color=colors3, height=0.5, edgecolor="none", zorder=3)
    for bar, v in zip(bars3, v3):
        label = f"{v:+,.0f}" if signed else f"{v:,.0f}"
        ax.text(v + max(abs(v) * 0.03, 30), bar.get_y() + bar.get_height() / 2,
                label, ha="left", va="center", fontsize=9)
    if col == 0:
        ax.set_ylabel("View 3: overall\n", fontsize=9)
    ax.set_xlabel(f"{name} (Mt CO₂)", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.15, zorder=0)
    xmax = max(abs(v) for v in v3) * 1.25
    if signed:
        ax.set_xlim(-xmax, xmax)
    else:
        ax.set_xlim(0, xmax)

plt.tight_layout()
out_png = FIG_DIR / "partA1_fig_co2_3x3.png"
out_pdf = FIG_DIR / "partA1_fig_co2_3x3.pdf"
plt.savefig(out_png, dpi=150, bbox_inches="tight")
plt.savefig(out_pdf, bbox_inches="tight")
print(f"\nSaved: {out_png}")
print(f"       {out_pdf}")
plt.show()
