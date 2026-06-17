"""
Part A.2 — Error diagnostics
A2.1: Addition vs substitution (ME sign at 2025 for all variables)
A2.2: Cross-variable error correlation matrix
A2.3: Temporal autocorrelation of errors
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
        "short": "CO₂"
    },
    "Primary Energy|Coal": {
        "obs": {"2010": 148, "2015": 155, "2020": 152, "2025": 164},
        "short": "Coal"
    },
    "Capacity|Electricity|Solar|PV": {
        "obs": {"2010": 40, "2015": 227, "2020": 714, "2025": 2392},
        "short": "Solar PV"
    },
    "Capacity|Electricity|Wind": {
        "obs": {"2010": 198, "2015": 433, "2020": 733, "2025": 1291},
        "short": "Wind"
    },
    "Capacity|Electricity|Nuclear": {
        "obs": {"2010": 375, "2015": 383, "2020": 393, "2025": 377},
        "short": "Nuclear"
    },
    "GDP|PPP": {
        "obs": {"2010": 87774, "2015": 100690, "2020": 107100, "2025": 122000},
        "short": "GDP"
    },
}

# ── Load ────────────────────────────────────────────────────────────────
print("Loading SCI data...")
df = pd.read_excel(SCI_FILE, sheet_name="data")
meta = pd.read_excel(SCI_FILE, sheet_name="meta")

meta["nz_year"] = pd.to_numeric(meta["Emissions Diagnostics|Year of Net Zero|CO2"], errors="coerce")
meta["nz2070"] = meta["nz_year"].notna() & (meta["nz_year"] <= 2070)
meta["key"] = meta["Model"] + "|||" + meta["Scenario"]
nz_keys = set(meta.loc[meta["nz2070"], "key"])

# ── Build error matrix: one row per scenario, columns = eps per variable per year ──
print("Computing errors...")

# First pass: get all scenario keys
all_keys = set()
var_data = {}

for varname, vinfo in VARIABLES.items():
    s = df[df["Variable"] == varname].copy()
    if len(s) == 0:
        print(f"  SKIP {vinfo['short']}: no data")
        continue
    s["key"] = s["Model"] + "|||" + s["Scenario"]
    obs = vinfo["obs"]
    for yr in YEARS:
        s[f"eps_{yr}"] = obs[yr] - s[yr]
    var_data[varname] = s.set_index("key")
    all_keys.update(s["key"].values)

# Build merged error dataframe: rows = scenarios, cols = (variable, year) errors
short_names = {v: VARIABLES[v]["short"] for v in var_data}
eps_frames = {}

for varname, s in var_data.items():
    short = short_names[varname]
    for yr in YEARS:
        col = f"{short}_{yr}"
        eps_frames[col] = s[f"eps_{yr}"]

eps_df = pd.DataFrame(eps_frames)
eps_df["nz2070"] = eps_df.index.isin(nz_keys)

print(f"Error matrix: {len(eps_df)} scenarios × {len(eps_frames)} columns")
print(f"  NZ2070: {eps_df['nz2070'].sum()} | non-NZ: {(~eps_df['nz2070']).sum()}")

# ═══════════════════════════════════════════════════════════════════════
# A2.1 — ADDITION VS SUBSTITUTION
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("  A2.1 — Addition vs Substitution: ME at 2025 for all variables")
print("  Positive ME = models underestimate observed (reality > projection)")
print("  Negative ME = models overestimate observed (reality < projection)")
print("=" * 70)

print(f"\n  {'Variable':<12} | {'ME 2025':>10} | {'Obs 2025':>10} | {'Median proj':>12} | {'Interpretation'}")
print(f"  {'-'*75}")

me_2025 = {}
for varname, s in var_data.items():
    short = short_names[varname]
    col = f"eps_2025"
    e = s[col].dropna()
    me = e.mean()
    obs_val = VARIABLES[varname]["obs"]["2025"]
    median_proj = (obs_val - e).median()
    me_2025[short] = me

    if me > 0:
        interp = "UNDERESTIMATED (reality > models)"
    else:
        interp = "OVERESTIMATED (reality < models)"

    print(f"  {short:<12} | {me:>+10,.0f} | {obs_val:>10,.0f} | {median_proj:>12,.0f} | {interp}")

# Addition test
coal_sign = me_2025.get("Coal", 0) > 0
solar_sign = me_2025.get("Solar PV", 0) > 0
wind_sign = me_2025.get("Wind", 0) > 0

print(f"\n  ADDITION TEST:")
print(f"    Coal underestimated (ME > 0)?  {'YES' if coal_sign else 'NO'}")
print(f"    Solar underestimated (ME > 0)? {'YES' if solar_sign else 'NO'}")
print(f"    Wind underestimated (ME > 0)?  {'YES' if wind_sign else 'NO'}")

if coal_sign and solar_sign:
    print(f"\n  → ENERGY ADDITION: models underestimate BOTH fossil AND renewable.")
    print(f"    The real world adds renewables without retiring fossils at the expected pace.")
elif coal_sign and not solar_sign:
    print(f"\n  → SUBSTITUTION FAILURE: models expected fossil phase-out that didn't happen,")
    print(f"    but correctly anticipated (or overestimated) renewable growth.")
else:
    print(f"\n  → Check results — pattern does not match simple addition/substitution.")

# ═══════════════════════════════════════════════════════════════════════
# A2.2 — CROSS-VARIABLE ERROR CORRELATION
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("  A2.2 — Cross-variable error correlation at 2025")
print("=" * 70)

# Extract eps at 2025 for all variables
cols_2025 = [f"{short_names[v]}_2025" for v in var_data]
corr_df = eps_df[cols_2025].dropna()

# Rename columns for display
rename = {c: c.replace("_2025", "") for c in cols_2025}
corr_df = corr_df.rename(columns=rename)

corr_matrix = corr_df.corr()
print(f"\n  Correlation matrix (n={len(corr_df)} scenarios with all variables):\n")
print(corr_matrix.round(2).to_string())

# Key pairs
pairs = [("Coal", "Solar PV"), ("Coal", "CO₂"), ("Solar PV", "Wind"),
         ("Coal", "Nuclear"), ("Solar PV", "CO₂"), ("Nuclear", "GDP")]
print(f"\n  Key correlations:")
for v1, v2 in pairs:
    if v1 in corr_matrix.columns and v2 in corr_matrix.columns:
        r = corr_matrix.loc[v1, v2]
        print(f"    Corr(ε_{v1}, ε_{v2}) = {r:+.3f}", end="")
        if abs(r) > 0.5:
            print(f"  ← STRONG {'positive' if r > 0 else 'negative'}")
        elif abs(r) > 0.2:
            print(f"  ← moderate")
        else:
            print(f"  ← weak")

# Split by NZ
print(f"\n  Coal-Solar correlation by NZ status:")
for nz, label in [(True, "NZ2070"), (False, "non-NZ")]:
    sub = eps_df[eps_df["nz2070"] == nz][cols_2025].dropna().rename(columns=rename)
    if "Coal" in sub.columns and "Solar PV" in sub.columns:
        r = sub["Coal"].corr(sub["Solar PV"])
        print(f"    {label:<8}: Corr(ε_Coal, ε_Solar) = {r:+.3f} (n={len(sub)})")

# ═══════════════════════════════════════════════════════════════════════
# A2.3 — TEMPORAL AUTOCORRELATION
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("  A2.3 — Temporal autocorrelation: Corr(ε_2010, ε_t) across scenarios")
print("  High ρ = structural bias (wrong from the start)")
print("  Low ρ = random error (missed specific events)")
print("=" * 70)

print(f"\n  {'Variable':<12} | {'ρ(2010,2015)':>12} | {'ρ(2010,2020)':>12} | {'ρ(2010,2025)':>12} | {'ρ(2015,2025)':>12}")
print(f"  {'-'*68}")

for varname, s in var_data.items():
    short = short_names[varname]
    rhos = []
    for t1, t2 in [("2010", "2015"), ("2010", "2020"), ("2010", "2025"), ("2015", "2025")]:
        e1 = s[f"eps_{t1}"]
        e2 = s[f"eps_{t2}"]
        mask = e1.notna() & e2.notna()
        rho = e1[mask].corr(e2[mask])
        rhos.append(rho)
    print(f"  {short:<12} | {rhos[0]:>+12.3f} | {rhos[1]:>+12.3f} | {rhos[2]:>+12.3f} | {rhos[3]:>+12.3f}")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 1: Cross-variable correlation heatmap at 2025
# ═══════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle("Part A.2 — Error diagnostics", fontsize=13, fontweight="bold")

# Panel 1: correlation heatmap
ax = axes[0]
n = len(corr_matrix)
im = ax.imshow(corr_matrix.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax.set_xticks(range(n))
ax.set_xticklabels(corr_matrix.columns, fontsize=8, rotation=45, ha="right")
ax.set_yticks(range(n))
ax.set_yticklabels(corr_matrix.columns, fontsize=8)
for i in range(n):
    for j in range(n):
        val = corr_matrix.values[i, j]
        ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=8,
                color="white" if abs(val) > 0.5 else "black")
ax.set_title("Cross-variable ε correlation (2025)", fontsize=10, fontweight="bold")
plt.colorbar(im, ax=ax, shrink=0.8)

# Panel 2: ME at 2025 for all variables (addition test)
ax = axes[1]
names = list(me_2025.keys())
vals = list(me_2025.values())
colors = ["#1D9E75" if v > 0 else "#D85A30" for v in vals]
bars = ax.barh(names, vals, color=colors)
ax.axvline(0, color="gray", lw=0.5, ls="--")
for bar, v in zip(bars, vals):
    ax.text(v + (abs(v) * 0.05 if v >= 0 else -abs(v) * 0.05),
            bar.get_y() + bar.get_height() / 2,
            f"{v:+,.0f}", ha="left" if v >= 0 else "right", va="center", fontsize=8)
ax.set_title("ME at 2025 (addition test)", fontsize=10, fontweight="bold")
ax.set_xlabel("ε = obs − proj (positive = underestimated)")
ax.spines[["top", "right"]].set_visible(False)
ax.invert_yaxis()

# Panel 3: temporal autocorrelation
ax = axes[2]
var_shorts = [short_names[v] for v in var_data]
rho_2010_2025 = []
rho_2015_2025 = []
for varname, s in var_data.items():
    e1 = s["eps_2010"]; e2 = s["eps_2025"]
    mask = e1.notna() & e2.notna()
    rho_2010_2025.append(e1[mask].corr(e2[mask]))
    e3 = s["eps_2015"]
    mask2 = e3.notna() & e2.notna()
    rho_2015_2025.append(e3[mask2].corr(e2[mask2]))

x = np.arange(len(var_shorts))
bw = 0.35
ax.barh(x - bw/2, rho_2010_2025, bw, label="ρ(2010,2025)", color="#378ADD")
ax.barh(x + bw/2, rho_2015_2025, bw, label="ρ(2015,2025)", color="#D85A30")
ax.set_yticks(x)
ax.set_yticklabels(var_shorts, fontsize=9)
ax.axvline(0, color="gray", lw=0.5, ls="--")
ax.set_title("Temporal autocorrelation", fontsize=10, fontweight="bold")
ax.set_xlabel("ρ")
ax.legend(fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
ax.invert_yaxis()
ax.set_xlim(-1, 1)

plt.tight_layout()
fig.savefig(FIG_DIR / "partA2_fig1_diagnostics.png", dpi=150, bbox_inches="tight")
print(f"\nSaved: partA2_fig1_diagnostics.png")

print("\nDone — Part A.2 complete.")
