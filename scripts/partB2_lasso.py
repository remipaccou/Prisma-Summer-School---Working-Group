"""
Part B.2 — LASSO variable selection (methodology §4.3).
L1-penalized logistic regression predicting NZ2070 membership from each scenario's normalised
hindcast error (MAE 2010-2025) on the 6 variables. Non-zero coefficients = informative variables.
Confirms Part B.1 (box plots): coal, CO2, solar carry the signal; wind/nuclear/GDP are dropped to ~0.
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

SCI_DATA = Path.home() / "PhD" / "4. Modeling" / "Prisma School" / "Scenario_Compass_Initiative_Data"
SCI_FILE = SCI_DATA / "SCI-2025_v1.0_pathways_ensemble_global.xlsx"
FIG_DIR = Path(__file__).parent.parent / "figures"; FIG_DIR.mkdir(exist_ok=True)
YEARS = ["2010", "2015", "2020", "2025"]
VARIABLES = {
    "Emissions|CO2|Energy and Industrial Processes": ("CO₂", {"2010":33400,"2015":35400,"2020":34800,"2025":38100}),
    "Primary Energy|Coal":           ("Coal",     {"2010":148,"2015":155,"2020":152,"2025":164}),
    "Capacity|Electricity|Solar|PV": ("Solar",    {"2010":40,"2015":227,"2020":714,"2025":2392}),
    "Capacity|Electricity|Wind":     ("Wind",     {"2010":198,"2015":433,"2020":733,"2025":1291}),
    "Capacity|Electricity|Nuclear":  ("Nuclear",  {"2010":375,"2015":383,"2020":393,"2025":377}),
    "GDP|PPP":                       ("GDP",      {"2010":87774,"2015":100690,"2020":107100,"2025":122000}),
}
df = pd.read_excel(SCI_FILE, sheet_name="data")
meta = pd.read_excel(SCI_FILE, sheet_name="meta"); meta["key"] = meta["Model"] + "|||" + meta["Scenario"]
nz = meta.set_index("key")["Emissions Diagnostics|Year of Net Zero|CO2"].le(2070)

def nmae(var, obs):
    s = df[df["Variable"] == var].copy(); s["key"] = s["Model"] + "|||" + s["Scenario"]
    eps = np.column_stack([obs[y] - s[y].values for y in YEARS])
    return pd.Series(np.nanmean(np.abs(eps), axis=1) / np.mean(list(obs.values())), index=s["key"].values)

labels = [lab for _, (lab, _) in VARIABLES.items()]
M = pd.DataFrame({lab: nmae(var, obs) for var, (lab, obs) in VARIABLES.items()})
M["nz"] = nz.reindex(M.index); M = M.dropna()
X = StandardScaler().fit_transform(M[labels].values); y = M["nz"].astype(int).values

# L1 logistic regression at a few regularisation strengths -> sparsity path
print(f"n = {len(M)} scenarios with all 6 variables; NZ share {y.mean():.0%}")
for C in [0.05, 0.1, 0.3]:
    clf = LogisticRegression(penalty="l1", solver="liblinear", C=C).fit(X, y)
    kept = [f"{labels[i]} {clf.coef_[0][i]:+.2f}" for i in range(len(labels)) if abs(clf.coef_[0][i]) > 1e-6]
    print(f"  C={C:<4} kept: {kept}")

clf = LogisticRegression(penalty="l1", solver="liblinear", C=0.1).fit(X, y)
coef = clf.coef_[0]
order = np.argsort(coef)
fig, ax = plt.subplots(figsize=(9, 5))
cols = ["#C0392B" if abs(c) > 1e-6 else "#cccccc" for c in coef[order]]
ax.barh([labels[i] for i in order], coef[order], color=cols)
ax.axvline(0, color="black", lw=1)
for i, idx in enumerate(order):
    if abs(coef[idx]) > 1e-6:
        ax.text(coef[idx] + (0.03 if coef[idx] > 0 else -0.03), i, f"{coef[idx]:+.2f}",
                va="center", ha="left" if coef[idx] > 0 else "right", fontsize=9, fontweight="bold")
ax.set_xlabel("L1-logistic coefficient (standardised) — predicting NZ2070 membership")
ax.set_title("Part B.2 — LASSO confirms Part B.1: coal, CO₂, solar carry the signal\n"
             "(+ = higher error ⇒ more likely NZ; − = lower error ⇒ more likely NZ). Wind/Nuclear/GDP → 0.",
             fontsize=10.5, fontweight="bold")
ax.set_xlim(-0.33, 0.45)
ax.spines[["top", "right"]].set_visible(False); ax.grid(axis="x", alpha=0.15)
plt.tight_layout(); plt.savefig(FIG_DIR / "partB2_lasso.png", dpi=150, bbox_inches="tight")
print("Saved: figures/partB2_lasso.png")
