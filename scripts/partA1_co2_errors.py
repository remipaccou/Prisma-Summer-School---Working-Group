"""
Part A.1 — Hindcast error computation (ME, MAE, RMSE)
Four variables: CO₂ emissions, Coal, Solar PV, Wind
Three views × three metrics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
        "unit": "Mt CO₂/yr", "short": "CO₂ emissions", "source": "GCB 2025"
    },
    "Primary Energy|Coal": {
        "obs": {"2010": 148, "2015": 155, "2020": 152, "2025": 164},
        "unit": "EJ/yr", "short": "Coal", "source": "EI StatReview 2025"
    },
    "Capacity|Electricity|Solar|PV": {
        "obs": {"2010": 40, "2015": 227, "2020": 714, "2025": 2392},
        "unit": "GW", "short": "Solar PV", "source": "IRENA 2026"
    },
    "Capacity|Electricity|Wind": {
        "obs": {"2010": 198, "2015": 433, "2020": 733, "2025": 1291},
        "unit": "GW", "short": "Wind", "source": "IRENA 2026"
    },
}

C_NZ, C_OT, C_ALL = "#D85A30", "#378ADD", "#534AB7"
C_POS, C_NEG = "#1D9E75", "#D85A30"

# ── Load ────────────────────────────────────────────────────────────────
print("Loading SCI data...")
df = pd.read_excel(SCI_FILE, sheet_name="data")
meta = pd.read_excel(SCI_FILE, sheet_name="meta")

meta["nz_year"] = pd.to_numeric(
    meta["Emissions Diagnostics|Year of Net Zero|CO2"], errors="coerce"
)
meta["nz2070"] = meta["nz_year"].notna() & (meta["nz_year"] <= 2070)
meta["key"] = meta["Model"] + "|||" + meta["Scenario"]
nz_keys = set(meta.loc[meta["nz2070"], "key"])

# ── Compute errors per variable ─────────────────────────────────────────
results = {}

for varname, vinfo in VARIABLES.items():
    s = df[df["Variable"] == varname].copy()
    s["key"] = s["Model"] + "|||" + s["Scenario"]
    s["nz2070"] = s["key"].isin(nz_keys)

    obs = vinfo["obs"]
    for yr in YEARS:
        s[f"eps_{yr}"] = obs[yr] - s[yr]

    eps_cols = [f"eps_{yr}" for yr in YEARS]
    eps_mat = s[eps_cols]

    s["ME_j"] = eps_mat.mean(axis=1)
    s["MAE_j"] = eps_mat.abs().mean(axis=1)
    s["RMSE_j"] = np.sqrt((eps_mat ** 2).mean(axis=1))

    results[varname] = {
        "s": s, "eps_mat": eps_mat, "obs": obs,
        "short": vinfo["short"], "unit": vinfo["unit"], "source": vinfo["source"],
        "n": len(s), "n_nz": s["nz2070"].sum(), "n_other": (~s["nz2070"]).sum(),
    }

# ── Print summary tables ────────────────────────────────────────────────
for varname, r in results.items():
    s = r["s"]
    obs = r["obs"]
    print(f"\n{'='*70}")
    print(f"  {r['short']} ({r['unit']}) — source: {r['source']}")
    print(f"  n={r['n']} scenarios, {s['Model'].nunique()} models")
    print(f"{'='*70}")

    print(f"\n  View 1: by year")
    print(f"  {'Year':<6} | {'ME':>10} | {'MAE':>10} | {'RMSE':>10} | {'±10%':>6}")
    print(f"  {'-'*50}")
    for yr in YEARS:
        e = s[f"eps_{yr}"].dropna()
        pct10 = (e.abs() / abs(obs[yr]) <= 0.10).mean() * 100
        print(f"  {yr:<6} | {e.mean():>+10,.0f} | {e.abs().mean():>10,.0f} | {np.sqrt((e**2).mean()):>10,.0f} | {pct10:>5.0f}%")

    print(f"\n  View 2: by scenario (NZ vs non-NZ)")
    print(f"  {'Group':<10} | {'ME_j':>8} | {'MAE_j':>8} | {'RMSE_j':>8} | {'n':>6}")
    print(f"  {'-'*50}")
    for grp, label in [(None, "All"), (True, "NZ2070"), (False, "non-NZ")]:
        sub = s if grp is None else s[s["nz2070"] == grp]
        print(f"  {label:<10} | {sub['ME_j'].mean():>+8,.0f} | {sub['MAE_j'].mean():>8,.0f} | {sub['RMSE_j'].mean():>8,.0f} | {len(sub):>6d}")

    all_eps = r["eps_mat"].values.flatten()
    all_eps = all_eps[~np.isnan(all_eps)]
    print(f"\n  View 3: overall")
    print(f"  ME={np.mean(all_eps):>+,.0f}  MAE={np.mean(np.abs(all_eps)):>,.0f}  RMSE={np.sqrt(np.mean(all_eps**2)):>,.0f}")

# ── Figure: 4 variables × 3 metrics (View 1 by year) ───────────────────
fig, axes = plt.subplots(len(VARIABLES), 3, figsize=(15, 4 * len(VARIABLES)))
fig.suptitle(
    "Part A.1 — Hindcast evaluation by year\n"
    r"$\varepsilon = y_{\mathrm{obs}} - \hat{y}_{\mathrm{proj}}$"
    "  |  positive = models underestimate observed",
    fontsize=13, fontweight="bold", y=1.01,
)

metric_fns = [
    ("ME", lambda e: e.mean(), True),
    ("MAE", lambda e: e.abs().mean(), False),
    ("RMSE", lambda e: np.sqrt((e**2).mean()), False),
]

for row, (varname, r) in enumerate(results.items()):
    s = r["s"]
    for col, (mname, fn, signed) in enumerate(metric_fns):
        ax = axes[row, col]
        vals = [fn(s[f"eps_{yr}"].dropna()) for yr in YEARS]
        colors = [C_POS if v >= 0 else C_NEG for v in vals] if signed else [C_OT if mname == "MAE" else C_ALL] * 4

        bars = ax.bar(YEARS, vals, color=colors, width=0.55)
        if signed:
            ax.axhline(0, color="gray", lw=0.5, ls="--")
        for bar, v in zip(bars, vals):
            off = max(abs(v) * 0.08, abs(max(vals, key=abs)) * 0.03)
            label = f"{v:+,.0f}" if signed else f"{v:,.0f}"
            ax.text(bar.get_x() + bar.get_width() / 2,
                    v + (off if v >= 0 or not signed else -off),
                    label, ha="center",
                    va="bottom" if (v >= 0 or not signed) else "top", fontsize=8)

        if row == 0:
            ax.set_title(f"{mname}", fontsize=11, fontweight="bold")
        if col == 0:
            ax.set_ylabel(f"{r['short']}\n({r['unit']})", fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=0.15)

plt.tight_layout()
out = FIG_DIR / "partA1_fig_all_by_year.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
plt.savefig(FIG_DIR / "partA1_fig_all_by_year.pdf", bbox_inches="tight")
print(f"\nSaved: {out}")

# ── Figure: 4 variables — NZ vs non-NZ histograms (MAE_j) ──────────────
fig2, axes2 = plt.subplots(2, 2, figsize=(12, 8))
fig2.suptitle(
    "Part A.1 — MAE distribution: NZ2070 vs non-NZ scenarios",
    fontsize=13, fontweight="bold",
)

for idx, (varname, r) in enumerate(results.items()):
    ax = axes2[idx // 2, idx % 2]
    s = r["s"]

    v_nz = s.loc[s["nz2070"], "MAE_j"].dropna().values
    v_ot = s.loc[~s["nz2070"], "MAE_j"].dropna().values

    lo = min(v_nz.min(), v_ot.min())
    hi = max(v_nz.max(), v_ot.max())
    step = (hi - lo) / 30
    bins = np.arange(lo, hi + step, step)

    ax.hist(v_ot, bins=bins, density=True, alpha=0.55, color=C_OT,
            label=f"non-NZ (n={len(v_ot)})", edgecolor="white", lw=0.3)
    ax.hist(v_nz, bins=bins, density=True, alpha=0.55, color=C_NZ,
            label=f"NZ2070 (n={len(v_nz)})", edgecolor="white", lw=0.3)
    ax.axvline(np.mean(v_ot), color=C_OT, lw=1.8, ls="--")
    ax.axvline(np.mean(v_nz), color=C_NZ, lw=1.8, ls="--")
    ax.legend(fontsize=8)
    ax.set_title(f"{r['short']} ({r['unit']})", fontsize=10, fontweight="bold")
    ax.set_xlabel(f"MAE_j ({r['unit']})", fontsize=9)
    ax.set_ylabel("density", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
out2 = FIG_DIR / "partA1_fig_all_mae_nz.png"
plt.savefig(out2, dpi=150, bbox_inches="tight")
plt.savefig(FIG_DIR / "partA1_fig_all_mae_nz.pdf", bbox_inches="tight")
print(f"Saved: {out2}")

# ── Figure: summary bar — View 3 overall ────────────────────────────────
fig3, axes3 = plt.subplots(1, 3, figsize=(14, 4))
fig3.suptitle("Part A.1 — Overall error (all years × all scenarios)", fontsize=13, fontweight="bold")

for col, (mname, _, signed) in enumerate(metric_fns):
    ax = axes3[col]
    labels = []
    vals_all, vals_nz, vals_ot = [], [], []

    for varname, r in results.items():
        eps_all = r["eps_mat"].values.flatten()
        eps_all = eps_all[~np.isnan(eps_all)]
        eps_nz = r["eps_mat"][r["s"]["nz2070"].values].values.flatten()
        eps_nz = eps_nz[~np.isnan(eps_nz)]
        eps_ot = r["eps_mat"][~r["s"]["nz2070"].values].values.flatten()
        eps_ot = eps_ot[~np.isnan(eps_ot)]

        if mname == "ME":
            vals_all.append(np.mean(eps_all))
            vals_nz.append(np.mean(eps_nz))
            vals_ot.append(np.mean(eps_ot))
        elif mname == "MAE":
            vals_all.append(np.mean(np.abs(eps_all)))
            vals_nz.append(np.mean(np.abs(eps_nz)))
            vals_ot.append(np.mean(np.abs(eps_ot)))
        else:
            vals_all.append(np.sqrt(np.mean(eps_all**2)))
            vals_nz.append(np.sqrt(np.mean(eps_nz**2)))
            vals_ot.append(np.sqrt(np.mean(eps_ot**2)))

        labels.append(r["short"])

    x = np.arange(len(labels))
    w = 0.25
    ax.bar(x - w, vals_nz, w, color=C_NZ, label="NZ2070")
    ax.bar(x, vals_all, w, color=C_ALL, label="All")
    ax.bar(x + w, vals_ot, w, color=C_OT, label="non-NZ")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_title(mname, fontsize=11, fontweight="bold")
    ax.legend(fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    if signed:
        ax.axhline(0, color="gray", lw=0.5, ls="--")

plt.tight_layout()
out3 = FIG_DIR / "partA1_fig_all_summary.png"
plt.savefig(out3, dpi=150, bbox_inches="tight")
plt.savefig(FIG_DIR / "partA1_fig_all_summary.pdf", bbox_inches="tight")
print(f"Saved: {out3}")

print("\nDone.")
