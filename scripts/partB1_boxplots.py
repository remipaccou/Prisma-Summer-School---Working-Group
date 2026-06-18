"""
Part B.1 — Which observables carry the signal? (box-plot separation, methodology §4.2)
For each of the 6 variables we box-plot the per-scenario hindcast error (normalised MAE over
2010-2025), split by NZ2070 vs non-NZ. Variables where the two groups separate are the ones to
filter on in Part C. Result: coal and solar PV (and CO2) discriminate; wind/nuclear/GDP do not.
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI_DATA = Path.home() / "PhD" / "4. Modeling" / "Prisma School" / "Scenario_Compass_Initiative_Data"
SCI_FILE = SCI_DATA / "SCI-2025_v1.0_pathways_ensemble_global.xlsx"
FIG_DIR = Path(__file__).parent.parent / "figures"; FIG_DIR.mkdir(exist_ok=True)
YEARS = ["2010", "2015", "2020", "2025"]

VARIABLES = {
    "Emissions|CO2|Energy and Industrial Processes": ("CO₂", {"2010":33400,"2015":35400,"2020":34800,"2025":38100}),
    "Primary Energy|Coal":           ("Coal",     {"2010":148,"2015":155,"2020":152,"2025":164}),
    "Capacity|Electricity|Solar|PV": ("Solar PV", {"2010":40,"2015":227,"2020":714,"2025":2392}),
    "Capacity|Electricity|Wind":     ("Wind",     {"2010":198,"2015":433,"2020":733,"2025":1291}),
    "Capacity|Electricity|Nuclear":  ("Nuclear",  {"2010":375,"2015":383,"2020":393,"2025":377}),
    "GDP|PPP":                       ("GDP",      {"2010":87774,"2015":100690,"2020":107100,"2025":122000}),
}
df = pd.read_excel(SCI_FILE, sheet_name="data")
meta = pd.read_excel(SCI_FILE, sheet_name="meta")
meta["key"] = meta["Model"] + "|||" + meta["Scenario"]
nz = meta.set_index("key")["Emissions Diagnostics|Year of Net Zero|CO2"].le(2070)

def nmae(var, obs):
    s = df[df["Variable"] == var].copy(); s["key"] = s["Model"] + "|||" + s["Scenario"]
    eps = np.column_stack([obs[y] - s[y].values for y in YEARS])
    out = pd.Series(np.nanmean(np.abs(eps), axis=1) / np.mean(list(obs.values())), index=s["key"].values)
    return out

fig, axes = plt.subplots(1, 6, figsize=(16, 5), sharey=False)
fig.suptitle("Part B.1 — Which observables separate net-zero scenarios? (normalised hindcast error 2010–2025)",
             fontsize=13, fontweight="bold")
sep = {}
for ax, (var, (lab, obs)) in zip(axes, VARIABLES.items()):
    e = nmae(var, obs); g = nz.reindex(e.index)
    a = e[g == True].dropna().values; b = e[g == False].dropna().values
    bp = ax.boxplot([b, a], labels=["non-NZ", "NZ"], widths=0.6, patch_artist=True, showfliers=False)
    for patch, c in zip(bp["boxes"], ["#378ADD", "#D85A30"]): patch.set_facecolor(c); patch.set_alpha(0.65)
    for med in bp["medians"]: med.set_color("black")
    # separation = (median_NZ - median_nonNZ) / pooled IQR  (signed effect size)
    iqr = (np.nanpercentile(np.r_[a, b], 75) - np.nanpercentile(np.r_[a, b], 25)) or 1
    d = (np.median(a) - np.median(b)) / iqr; sep[lab] = d
    ax.set_title(f"{lab}\nsep = {d:+.2f}", fontsize=10,
                 fontweight="bold", color="#C0392B" if abs(d) > 0.3 else "#888")
    ax.set_ylabel("normalised MAE" if ax is axes[0] else "")
    ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="y", alpha=0.15)
fig.text(0.5, 0.01, "sep = (median_NZ − median_nonNZ) / pooled IQR.  |sep|>0.3 (red) = discriminating variable.  "
         "→ Coal & Solar (and CO₂) carry the signal; filter on these (multivariate) in Part C.",
         ha="center", fontsize=9, style="italic")
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(FIG_DIR / "partB1_boxplots.png", dpi=150, bbox_inches="tight")
print("Separation by variable (|sep|>0.5 = discriminating):")
for k, v in sorted(sep.items(), key=lambda kv: -abs(kv[1])): print(f"  {k:<9} {v:+.2f}")
print("Saved: figures/partB1_boxplots.png")
