"""
Part A.1 — Hindcast error computation
6 variables, 3 metrics, family weighting, economy/energy split, vintage analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────
SCI_DATA = Path.home() / "PhD" / "4. Modeling" / "Prisma School" / "Scenario_Compass_Initiative_Data"
SCI_FILE = SCI_DATA / "SCI-2025_v1.0_pathways_ensemble_global.xlsx"
FIG_DIR = Path(__file__).parent.parent / "figures"
FIG_DIR.mkdir(exist_ok=True)

YEARS = ["2010", "2015", "2020", "2025"]

VARIABLES = {
    "Emissions|CO2|Energy and Industrial Processes": {
        "obs": {"2010": 33400, "2015": 35400, "2020": 34800, "2025": 38100},
        "unit": "Mt CO₂/yr", "short": "CO₂", "source": "GCB 2025"
    },
    "Primary Energy|Coal": {
        "obs": {"2010": 148, "2015": 155, "2020": 152, "2025": 164},
        "unit": "EJ/yr", "short": "Coal", "source": "EI StatReview"
    },
    "Capacity|Electricity|Solar|PV": {
        "obs": {"2010": 40, "2015": 227, "2020": 714, "2025": 2392},
        "unit": "GW", "short": "Solar PV", "source": "IRENA 2026"
    },
    "Capacity|Electricity|Wind": {
        "obs": {"2010": 198, "2015": 433, "2020": 733, "2025": 1291},
        "unit": "GW", "short": "Wind", "source": "IRENA 2026"
    },
    "Capacity|Electricity|Nuclear": {
        "obs": {"2010": 375, "2015": 383, "2020": 393, "2025": 377},
        "unit": "GW", "short": "Nuclear", "source": "IAEA PRIS"
    },
    "GDP|PPP": {
        "obs": {"2010": 87774, "2015": 100690, "2020": 107100, "2025": 122000},
        "unit": "B US$2010", "short": "GDP PPP", "source": "IMF/WB"
    },
}

# ── Model families ──────────────────────────────────────────────────────
_FAMILIES = ['MESSAGE', 'REMIND', 'IMACLIM', 'IMAGE', 'WITCH', 'POLES', 'GCAM',
             'AIM', 'COFFEE', 'TIAM', 'GEM-E3', 'PROMETHEUS', 'EPPA', 'C-ROADS',
             'MERGE', 'CGEM', 'MINES']

def to_family(model):
    up = str(model).upper()
    for f in _FAMILIES:
        if f in up:
            return f
    return str(model)

_CLASS = {
    'REMIND': 'economy', 'WITCH': 'economy', 'MERGE': 'economy',
    'AIM': 'economy', 'GEM-E3': 'economy', 'IMACLIM': 'economy',
    'EPPA': 'economy', 'CGEM': 'economy',
    'MESSAGE': 'energy', 'IMAGE': 'energy', 'POLES': 'energy',
    'COFFEE': 'energy', 'GCAM': 'energy', 'TIAM': 'energy', 'PROMETHEUS': 'energy',
    'C-ROADS': 'other', 'MINES': 'other',
}

# ── Vintage mapping ─────────────────────────────────────────────────────
_VINTAGE = {
    "SSP": "early", "ADVANCE [EU FP7]": "early", "EMF30": "early", "EMF33": "early",
    "CD-LINKS [Horizon 2020]": "mid", "COMMIT [Horizon 2020]": "mid",
    "SSP-2021 (IMAGE)": "mid", "INNOPATHS [Horizon 2020]": "mid",
    "SHAPE [JPI Climate]": "mid", "COVID-Shift (MESSAGEix-GLOBIOM)": "mid",
    "Deep-Mitigation (GCAM)": "mid", "RATCHET (C-ROADS)": "mid",
    "MIT-JP (EPPA)": "mid", "Paris Reinforce [Horizon 2020]": "mid",
    "SDI (AIM/Hub-Global)": "mid", "China-NZP [NSFC]": "mid",
    "DAC (MERGE-ETL)": "mid", "LED (MESSAGEix-GLOBIOM)": "mid",
}
# Everything not in _VINTAGE defaults to "late"

# ── Colors ──────────────────────────────────────────────────────────────
C_NZ, C_OT, C_ALL = "#D85A30", "#378ADD", "#534AB7"
C_POS, C_NEG = "#1D9E75", "#D85A30"
C_VINTAGE = {"early": "#E8A838", "mid": "#378ADD", "late": "#1D9E75"}
C_CLASS = {"energy": "#378ADD", "economy": "#D85A30"}

# ── Load ────────────────────────────────────────────────────────────────
print("Loading SCI data (1-2 min)...")
df = pd.read_excel(SCI_FILE, sheet_name="data")
meta = pd.read_excel(SCI_FILE, sheet_name="meta")

meta["nz_year"] = pd.to_numeric(meta["Emissions Diagnostics|Year of Net Zero|CO2"], errors="coerce")
meta["nz2070"] = meta["nz_year"].notna() & (meta["nz_year"] <= 2070)
meta["key"] = meta["Model"] + "|||" + meta["Scenario"]
meta["vintage"] = meta["Project"].map(lambda p: _VINTAGE.get(p, "late"))
nz_keys = set(meta.loc[meta["nz2070"], "key"])
vintage_map = dict(zip(meta["key"], meta["vintage"]))

# ── Compute errors per variable ─────────────────────────────────────────
results = {}

for varname, vinfo in VARIABLES.items():
    s = df[df["Variable"] == varname].copy()
    if len(s) == 0:
        print(f"  SKIP {vinfo['short']}: no data in SCI")
        continue
    s["key"] = s["Model"] + "|||" + s["Scenario"]
    s["nz2070"] = s["key"].isin(nz_keys)
    s["Family"] = s["Model"].map(to_family)
    s["Class"] = s["Family"].map(_CLASS).fillna("other")
    s["vintage"] = s["key"].map(vintage_map).fillna("late")

    # Family weights
    s["w"] = 1.0 / s.groupby("Family")["Family"].transform("size")

    obs = vinfo["obs"]
    for yr in YEARS:
        s[f"eps_{yr}"] = obs[yr] - s[yr]

    eps_cols = [f"eps_{yr}" for yr in YEARS]
    s["ME_j"] = s[eps_cols].mean(axis=1)
    s["MAE_j"] = s[eps_cols].abs().mean(axis=1)
    s["RMSE_j"] = np.sqrt((s[eps_cols] ** 2).mean(axis=1))

    results[varname] = {"s": s, "obs": obs, **vinfo,
                        "n": len(s), "n_nz": s["nz2070"].sum()}

print(f"Loaded {len(results)} variables\n")

# ── Helper ──────────────────────────────────────────────────────────────
def wmean(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float)
    m = ~np.isnan(x)
    return np.sum(w[m] * x[m]) / np.sum(w[m]) if np.sum(w[m]) > 0 else np.nan

# ═══════════════════════════════════════════════════════════════════════
# PRINT TABLES
# ═══════════════════════════════════════════════════════════════════════
for varname, r in results.items():
    s = r["s"]
    print(f"\n{'='*65}")
    print(f"  {r['short']} ({r['unit']}) — {r['source']} — n={r['n']}")
    print(f"{'='*65}")

    # View 1
    print(f"\n  View 1 (family-weighted, by year):")
    print(f"  {'Year':<6} | {'ME':>8} | {'MAE':>8} | {'RMSE':>8}")
    print(f"  {'-'*40}")
    for yr in YEARS:
        e = s[f"eps_{yr}"]
        print(f"  {yr:<6} | {wmean(e, s['w']):>+8,.0f} | {wmean(e.abs(), s['w']):>8,.0f} | {np.sqrt(wmean(e**2, s['w'])):>8,.0f}")

    # View 2 NZ vs non-NZ
    print(f"\n  NZ vs non-NZ (family-weighted MAE_j):")
    for grp, label in [(True, "NZ2070"), (False, "non-NZ")]:
        sub = s[s["nz2070"] == grp]
        w = 1.0 / sub.groupby("Family")["Family"].transform("size")
        print(f"    {label:<8}: ME_j={wmean(sub['ME_j'], w):>+8,.0f}  MAE_j={wmean(sub['MAE_j'], w):>8,.0f}  n={len(sub)}")

    # Economy vs energy
    print(f"\n  Economy vs energy (ME_j):")
    for cl in ["economy", "energy"]:
        sub = s[s["Class"] == cl]
        if len(sub) < 10: continue
        w = 1.0 / sub.groupby("Family")["Family"].transform("size")
        print(f"    {cl:<8}: ME_j={wmean(sub['ME_j'], w):>+8,.0f}  MAE_j={wmean(sub['MAE_j'], w):>8,.0f}  n={len(sub)}")

    # Vintage
    print(f"\n  By vintage (ME by year):")
    print(f"  {'Vintage':<8} | {'n':>5} | {'2010':>8} | {'2015':>8} | {'2020':>8} | {'2025':>8} | {'MAE_j':>8}")
    print(f"  {'-'*65}")
    for v in ["early", "mid", "late"]:
        sub = s[s["vintage"] == v]
        if len(sub) < 5: continue
        row = f"  {v:<8} | {len(sub):>5}"
        for yr in YEARS:
            row += f" | {sub[f'eps_{yr}'].mean():>+8,.0f}"
        row += f" | {sub['MAE_j'].mean():>8,.0f}"
        print(row)

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 1: All variables × ME/MAE/RMSE by year (6×3 grid)
# ═══════════════════════════════════════════════════════════════════════
n_vars = len(results)
fig1, axes1 = plt.subplots(n_vars, 3, figsize=(15, 3.2 * n_vars))
fig1.suptitle("Part A.1 — Hindcast by year (family-weighted)", fontsize=13, fontweight="bold", y=1.01)

for row, (varname, r) in enumerate(results.items()):
    s = r["s"]
    for col, (mname, signed) in enumerate([("ME", True), ("MAE", False), ("RMSE", False)]):
        ax = axes1[row, col] if n_vars > 1 else axes1[col]
        if mname == "ME":    vals = [wmean(s[f"eps_{yr}"], s["w"]) for yr in YEARS]
        elif mname == "MAE": vals = [wmean(s[f"eps_{yr}"].abs(), s["w"]) for yr in YEARS]
        else:                vals = [np.sqrt(wmean(s[f"eps_{yr}"]**2, s["w"])) for yr in YEARS]
        colors = [C_POS if v >= 0 else C_NEG for v in vals] if signed else [C_OT if mname == "MAE" else C_ALL] * 4
        bars = ax.bar(YEARS, vals, color=colors, width=0.55)
        if signed: ax.axhline(0, color="gray", lw=0.5, ls="--")
        for bar, v in zip(bars, vals):
            off = max(abs(v) * 0.08, 1)
            ax.text(bar.get_x() + bar.get_width() / 2, v + (off if v >= 0 or not signed else -off),
                    f"{v:+,.0f}" if signed else f"{v:,.0f}", ha="center",
                    va="bottom" if (v >= 0 or not signed) else "top", fontsize=7)
        if row == 0: ax.set_title(mname, fontsize=11, fontweight="bold")
        if col == 0: ax.set_ylabel(f"{r['short']}\n({r['unit']})", fontsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.15)

plt.tight_layout()
fig1.savefig(FIG_DIR / "partA1_fig1_by_year.png", dpi=150, bbox_inches="tight")
print("Saved: partA1_fig1_by_year.png")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 2: MAE histograms NZ vs non-NZ (6 panels)
# ═══════════════════════════════════════════════════════════════════════
fig2, axes2 = plt.subplots(2, 3, figsize=(15, 8))
fig2.suptitle("Part A.1 — MAE distribution: NZ2070 vs non-NZ (density)", fontsize=13, fontweight="bold")
axes2_flat = axes2.flatten()

for idx, (varname, r) in enumerate(results.items()):
    ax = axes2_flat[idx]
    s = r["s"]
    v_nz = s.loc[s["nz2070"], "MAE_j"].dropna().values
    v_ot = s.loc[~s["nz2070"], "MAE_j"].dropna().values
    lo, hi = min(v_nz.min(), v_ot.min()), max(v_nz.max(), v_ot.max())
    bins = np.arange(lo, hi + (hi - lo) / 30, (hi - lo) / 30)
    ax.hist(v_ot, bins=bins, density=True, alpha=0.55, color=C_OT, label=f"non-NZ ({len(v_ot)})", edgecolor="white", lw=0.3)
    ax.hist(v_nz, bins=bins, density=True, alpha=0.55, color=C_NZ, label=f"NZ ({len(v_nz)})", edgecolor="white", lw=0.3)
    ax.axvline(np.mean(v_ot), color=C_OT, lw=1.8, ls="--")
    ax.axvline(np.mean(v_nz), color=C_NZ, lw=1.8, ls="--")
    ax.legend(fontsize=7)
    ax.set_title(r["short"], fontsize=10, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)

for idx in range(len(results), len(axes2_flat)):
    axes2_flat[idx].set_visible(False)

plt.tight_layout()
fig2.savefig(FIG_DIR / "partA1_fig2_mae_nz.png", dpi=150, bbox_inches="tight")
print("Saved: partA1_fig2_mae_nz.png")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 3: Dashboard — MAE_j across all cuts, all variables
# Rows = variables, Cols = NZ/non-NZ | economy/energy | early/mid/late
# ═══════════════════════════════════════════════════════════════════════
var_names = [r["short"] for r in results.values()]
n_v = len(var_names)

fig3, axes3 = plt.subplots(1, 3, figsize=(16, 5))
fig3.suptitle("Part A.1 — MAE summary across all variables and analysis dimensions",
              fontsize=13, fontweight="bold")

x = np.arange(n_v)
bw = 0.35

# Panel 1: NZ vs non-NZ
ax = axes3[0]
for k, (nz, label, color) in enumerate([(True, "NZ2070", C_NZ), (False, "non-NZ", C_OT)]):
    vals = []
    for r in results.values():
        sub = r["s"][r["s"]["nz2070"] == nz]
        vals.append(sub["MAE_j"].mean())
    ax.barh(x + (k - 0.5) * bw, vals, bw, label=label, color=color)
ax.set_yticks(x); ax.set_yticklabels(var_names, fontsize=9)
ax.set_xlabel("MAE_j"); ax.set_title("NZ vs non-NZ", fontweight="bold")
ax.legend(fontsize=8); ax.spines[["top", "right"]].set_visible(False)
ax.invert_yaxis()

# Panel 2: economy vs energy
ax = axes3[1]
for k, (cl, color) in enumerate([("economy", C_CLASS["economy"]), ("energy", C_CLASS["energy"])]):
    vals = []
    for r in results.values():
        sub = r["s"][r["s"]["Class"] == cl]
        vals.append(sub["MAE_j"].mean() if len(sub) > 10 else 0)
    ax.barh(x + (k - 0.5) * bw, vals, bw, label=cl, color=color)
ax.set_yticks(x); ax.set_yticklabels(var_names, fontsize=9)
ax.set_xlabel("MAE_j"); ax.set_title("Economy vs Energy", fontweight="bold")
ax.legend(fontsize=8); ax.spines[["top", "right"]].set_visible(False)
ax.invert_yaxis()

# Panel 3: vintage
ax = axes3[2]
bw3 = 0.25
for k, (v, color) in enumerate([("early", C_VINTAGE["early"]), ("mid", C_VINTAGE["mid"]), ("late", C_VINTAGE["late"])]):
    vals = []
    for r in results.values():
        sub = r["s"][r["s"]["vintage"] == v]
        vals.append(sub["MAE_j"].mean() if len(sub) > 5 else 0)
    ax.barh(x + (k - 1) * bw3, vals, bw3, label=v, color=color)
ax.set_yticks(x); ax.set_yticklabels(var_names, fontsize=9)
ax.set_xlabel("MAE_j"); ax.set_title("By vintage", fontweight="bold")
ax.legend(fontsize=8); ax.spines[["top", "right"]].set_visible(False)
ax.invert_yaxis()

plt.tight_layout()
fig3.savefig(FIG_DIR / "partA1_fig3_dashboard.png", dpi=150, bbox_inches="tight")
print("Saved: partA1_fig3_dashboard.png")

print("\nDone — 3 figures generated.")
