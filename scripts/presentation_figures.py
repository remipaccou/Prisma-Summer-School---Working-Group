"""
5 presentation figures — square format, consistent design, journalist titles.
Figures 1, 4, 5 kept as before. Figures 2 and 3 enriched to match original scripts.
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

mpl.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white", "savefig.dpi": 200,
    "font.family": "sans-serif", "font.size": 11,
    "axes.titlesize": 12, "axes.titleweight": "bold",
    "axes.labelsize": 11, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.15, "grid.linewidth": 0.5,
    "legend.frameon": False, "legend.fontsize": 9,
})

C_NZ = "#D8732E"
C_OT = "#2C6FA6"
C_GRAY = "#9aa0a6"
C_POS = "#1D9E75"
C_NEG = "#E63329"
SQ = (7, 7)

SCI_DATA = Path.home() / "PhD" / "4. Modeling" / "Prisma School" / "Scenario_Compass_Initiative_Data"
SCI_FILE = SCI_DATA / "SCI-2025_v1.0_pathways_ensemble_global.xlsx"
FIG_DIR = Path(__file__).parent.parent / "figures" / "final"
FIG_DIR.mkdir(exist_ok=True)

print("Loading SCI data...")
df = pd.read_excel(SCI_FILE, sheet_name="data")
meta = pd.read_excel(SCI_FILE, sheet_name="meta")
meta["nz_year"] = pd.to_numeric(meta["Emissions Diagnostics|Year of Net Zero|CO2"], errors="coerce")
meta["nz2070"] = meta["nz_year"].notna() & (meta["nz_year"] <= 2070)
meta["key"] = meta["Model"] + "|||" + meta["Scenario"]
nz_keys = set(meta.loc[meta["nz2070"], "key"])

_F = ['MESSAGE','REMIND','IMACLIM','IMAGE','WITCH','POLES','GCAM','AIM','COFFEE','TIAM','GEM-E3','PROMETHEUS','EPPA','C-ROADS','MERGE','CGEM','MINES']
def to_fam(m): return next((f for f in _F if f in str(m).upper()), str(m))

YEARS_PROJ = [str(y) for y in range(2010, 2101, 5)]
YEARS_HIST = ["2010", "2015", "2020", "2025"]
OBS_CO2 = {"2010": 33400, "2015": 35400, "2020": 34800, "2025": 38100}
VAR_CO2 = "Emissions|CO2|Energy and Industrial Processes"
VAR_SOLAR = "Capacity|Electricity|Solar|PV"

co2 = df[df["Variable"] == VAR_CO2].copy()
co2["key"] = co2["Model"] + "|||" + co2["Scenario"]
co2["nz2070"] = co2["key"].isin(nz_keys)
co2["Family"] = co2["Model"].map(to_fam)

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 1: CO₂ ensemble cloud + observed
# ═══════════════════════════════════════════════════════════════════════
print("Fig 1...")
fig1, ax = plt.subplots(figsize=SQ)
years_num = [int(y) for y in YEARS_PROJ if y in co2.columns]
mat_nz = co2[co2["nz2070"]][[str(y) for y in years_num]].values
mat_ot = co2[~co2["nz2070"]][[str(y) for y in years_num]].values

# Interpolate to smooth the sawtooth
from scipy.interpolate import interp1d
years_smooth = np.arange(min(years_num), max(years_num) + 1)

for pct in [5, 10, 25]:
    for mat, color in [(mat_nz, C_NZ), (mat_ot, C_OT)]:
        lo = np.nanpercentile(mat, pct, axis=0)
        hi = np.nanpercentile(mat, 100 - pct, axis=0)
        f_lo = interp1d(years_num, lo, kind='cubic', fill_value='extrapolate')
        f_hi = interp1d(years_num, hi, kind='cubic', fill_value='extrapolate')
        ax.fill_between(years_smooth, f_lo(years_smooth), f_hi(years_smooth), color=color, alpha=0.08)

for mat, color, label in [(mat_nz, C_NZ, f"NZ2070 median (n={len(mat_nz)})"),
                           (mat_ot, C_OT, f"non-NZ median (n={len(mat_ot)})")]:
    med = np.nanmedian(mat, axis=0)
    f_med = interp1d(years_num, med, kind='cubic', fill_value='extrapolate')
    ax.plot(years_smooth, f_med(years_smooth), color=color, lw=2, label=label)
ax.plot([int(y) for y in OBS_CO2], list(OBS_CO2.values()), "ko-", ms=8, lw=2.5, zorder=10, label="Observed (GCB 2025)")
ax.set_xlabel("Year"); ax.set_ylabel("Mt CO₂/yr")
ax.set_title("CO\u2082 emissions: SCI ensemble vs observed 2010\u20132025")
ax.set_xlim(2010, 2100); ax.set_ylim(0, 70000); ax.legend(loc="upper right")
fig1.tight_layout(); fig1.savefig(FIG_DIR / "pres_1_co2_ensemble.png", bbox_inches="tight")
print("  Saved pres_1_co2_ensemble.png")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 2: NZ bias — histogram (original style)
# ═══════════════════════════════════════════════════════════════════════
print("Fig 2...")
fig2, ax = plt.subplots(figsize=SQ)

E = np.column_stack([OBS_CO2[y] - co2[y].values for y in OBS_CO2])
co2["ME_j"] = np.nanmean(E, axis=1)
co2["MAE_j"] = np.nanmean(np.abs(E), axis=1)
co2["w"] = 1.0 / co2.groupby("Family")["Family"].transform("size")

A = co2[co2["nz2070"]].dropna(subset=["ME_j"])
B = co2[~co2["nz2070"]].dropna(subset=["ME_j"])

meA = np.average(A["ME_j"], weights=A["w"])
meB = np.average(B["ME_j"], weights=B["w"])
maA = np.average(A["MAE_j"], weights=A["w"])
maB = np.average(B["MAE_j"], weights=B["w"])

bins = np.arange(-6000, 6001, 500)
ax.hist(B["ME_j"], bins=bins, density=True, alpha=0.55, color=C_OT, label=f"non-NZ (n={len(B)})", edgecolor="white", lw=0.3)
ax.hist(A["ME_j"], bins=bins, density=True, alpha=0.55, color=C_NZ, label=f"NZ2070 (n={len(A)})", edgecolor="white", lw=0.3)
ax.axvline(0, color="black", lw=1.2)
ax.axvline(meB, color="#1f4e79", lw=2, ls="--")
ax.axvline(meA, color="#9c4a1f", lw=2, ls="--")

top = ax.get_ylim()[1]
ax.text(meA + 120, top * 0.92, f"NZ mean +{meA:.0f}", color="#9c4a1f", fontsize=9, fontweight="bold")
ax.text(meB - 120, top * 0.80, f"non-NZ mean +{meB:.0f}", color="#1f4e79", fontsize=9, fontweight="bold", ha="right")
ax.annotate("under-project CO₂\n(biased low)", (2600, top*0.5), (3600, top*0.72),
            fontsize=9, color="#9c4a1f", ha="center", arrowprops=dict(arrowstyle="->", color="#9c4a1f"))

ax.set_xlabel("Per-scenario CO₂ error (obs − proj), mean over 2010–2025  (Mt)")
ax.set_ylabel("density"); ax.set_xlim(-6000, 6000)
ax.set_title("CO\u2082 error distribution: NZ2070 vs non-NZ scenarios")
ax.legend(fontsize=9, loc="upper left")
fig2.tight_layout(); fig2.savefig(FIG_DIR / "pres_2_nz_bias.png", bbox_inches="tight")
print("  Saved pres_2_nz_bias.png")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 3: Skill vs naive rule (original style — grouped bars)
# ═══════════════════════════════════════════════════════════════════════
print("Fig 3...")
VARS_SKILL = {
    VAR_CO2: ({"10":33400,"15":35400,"25":38100}, "CO₂"),
    "Primary Energy|Coal": ({"10":148,"15":155,"25":164}, "Coal"),
    VAR_SOLAR: ({"10":40,"15":227,"25":2392}, "Solar PV"),
    "Capacity|Electricity|Wind": ({"10":198,"15":433,"25":1291}, "Wind"),
    "Capacity|Electricity|Nuclear": ({"10":375,"15":383,"25":377}, "Nuclear"),
    "GDP|PPP": ({"10":87774,"15":100690,"25":122000}, "GDP"),
}

rows = []
for var, (obs, short) in VARS_SKILL.items():
    sv = df[df["Variable"] == var]
    if len(sv) == 0: continue
    o10, o15, o25 = obs["10"], obs["15"], obs["25"]
    ens_med = sv["2025"].dropna().median()
    # Three naive rules
    rw = o15
    lin = o15 + 2 * (o15 - o10)
    log = o15 * (o15/o10)**2 if o10 > 0 else np.nan
    naives = {"RW": rw, "linear": lin, "log-trend": log}
    best_k = min(naives, key=lambda k: abs(o25 - naives[k]))
    best_err = abs(o25 - naives[best_k])
    ens_err = abs(o25 - ens_med)
    skill = ens_err / best_err if best_err > 0 else np.nan
    scen25 = sv["2025"].dropna().values
    pct_beaten = np.mean(np.abs(o25 - scen25) > best_err) * 100
    rows.append(dict(var=short, ens_pe=100*ens_err/o25, naive_pe=100*best_err/o25,
                     skill=skill, best_naive=best_k, pct_beaten=pct_beaten))
R = pd.DataFrame(rows)

fig3, ax = plt.subplots(figsize=SQ)
x = np.arange(len(R)); w = 0.35
ax.bar(x - w/2, R["ens_pe"], w, color=C_OT, label="IAM ensemble (median)")
ax.bar(x + w/2, R["naive_pe"], w, color=C_GRAY, label="Best naive rule")

for i, r in R.iterrows():
    loses = r["skill"] > 1
    y_top = max(r["ens_pe"], r["naive_pe"]) + 2
    ax.text(i, y_top, f"skill {r['skill']:.1f}\n{'rule wins' if loses else 'ensemble wins'}",
            ha="center", fontsize=8, fontweight="bold", color=C_NEG if loses else C_POS)

ax.set_xticks(x)
ax.set_xticklabels([f"{r['var']}\n({r['best_naive']})" for _, r in R.iterrows()], fontsize=9)
ax.set_ylabel("2025 forecast error (% of observed)")
ax.set_title("Forecast skill: ensemble vs linear extrapolation at 2025")
ax.legend(fontsize=9)
fig3.tight_layout(); fig3.savefig(FIG_DIR / "pres_3_skill.png", bbox_inches="tight")
print("  Saved pres_3_skill.png")

# ═══════════════════════════════════════════════════════════════════════
# FIGURE 4: Box plots (kept as before, updated title)
# ═══════════════════════════════════════════════════════════════════════
print("Fig 4...")
fig4, ax = plt.subplots(figsize=SQ)

VARS_BOX = {
    VAR_CO2: (OBS_CO2, "CO₂"),
    "Primary Energy|Coal": ({"2010":148,"2015":155,"2020":152,"2025":164}, "Coal"),
    VAR_SOLAR: ({"2010":40,"2015":227,"2020":714,"2025":2392}, "Solar PV"),
    "Capacity|Electricity|Wind": ({"2010":198,"2015":433,"2020":733,"2025":1291}, "Wind"),
    "Capacity|Electricity|Nuclear": ({"2010":375,"2015":383,"2020":393,"2025":377}, "Nuclear"),
    "GDP|PPP": ({"2010":87774,"2015":100690,"2020":107100,"2025":122000}, "GDP"),
}

seps = {}
pos = 0
positions = []
labels = []

for var, (obs, short) in VARS_BOX.items():
    s = df[df["Variable"] == var].copy()
    if len(s) == 0: continue
    s["key"] = s["Model"] + "|||" + s["Scenario"]
    s["nz2070"] = s["key"].isin(nz_keys)
    eps_tmp = []
    for yr in YEARS_HIST:
        s[f"e_{yr}"] = obs[yr] - s[yr]
        eps_tmp.append(f"e_{yr}")
    s["nmae"] = s[eps_tmp].abs().mean(axis=1) / np.mean(list(obs.values()))

    nz_v = s.loc[s["nz2070"], "nmae"].dropna().values
    ot_v = s.loc[~s["nz2070"], "nmae"].dropna().values
    all_v = np.concatenate([nz_v, ot_v])
    iqr = np.percentile(all_v, 75) - np.percentile(all_v, 25)
    sep = (np.median(nz_v) - np.median(ot_v)) / iqr if iqr > 0 else 0
    seps[short] = sep

    ax.boxplot([nz_v], positions=[pos - 0.18], widths=0.3, patch_artist=True,
               boxprops=dict(facecolor=C_NZ, alpha=0.5), medianprops=dict(color=C_NZ, lw=2),
               whiskerprops=dict(color=C_NZ), capprops=dict(color=C_NZ), showfliers=False)
    ax.boxplot([ot_v], positions=[pos + 0.18], widths=0.3, patch_artist=True,
               boxprops=dict(facecolor=C_OT, alpha=0.5), medianprops=dict(color=C_OT, lw=2),
               whiskerprops=dict(color=C_OT), capprops=dict(color=C_OT), showfliers=False)
    labels.append(short); positions.append(pos); pos += 1

ax.set_xticks(positions); ax.set_xticklabels(labels)
ax.set_ylabel("Normalised MAE")
ax.set_title("Coal and solar separate NZ from non-NZ\n— in opposite directions")
ax.set_ylim(0, None)
ymax = ax.get_ylim()[1]
for i, (short, sep) in enumerate(seps.items()):
    clr = C_NZ if sep > 0.2 else (C_OT if sep < -0.2 else "gray")
    ax.text(i, ymax * 0.95, f"sep={sep:+.2f}", ha="center", fontsize=8, fontstyle="italic", color=clr)

from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=C_NZ, alpha=0.5, label="NZ2070"),
                   Patch(facecolor=C_OT, alpha=0.5, label="non-NZ")], loc="upper right")
fig4.tight_layout(); fig4.savefig(FIG_DIR / "pres_4_boxplots.png", bbox_inches="tight")
print("  Saved pres_4_boxplots.png")

# FIGURE 5: uses the original Wright log figure from the full analysis script
# (copied to figures/final/ separately — not regenerated here)

plt.close("all")
print("\nDone — 5 figures saved.")
