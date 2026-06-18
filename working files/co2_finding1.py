"""
Finding 1, defense-grade: separate the COVID-contaminated 2020 from the structural 2025.
Left  : trajectory — models peak ~2020 & decline, reality dips (COVID) then rises on trend.
Right : ME decomposition — 2020 is COVID (robust to 2 counterfactuals), 2025 survives detrending.
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
OBS = {2010: 33400, 2015: 35400, 2020: 34800, 2025: 38100}
YEARS = list(range(2010, 2031, 5)); YC = [str(y) for y in YEARS]; X = np.array(YEARS)
_F = ['MESSAGE','REMIND','IMACLIM','IMAGE','WITCH','POLES','GCAM','AIM','COFFEE','TIAM','GEM-E3','PROMETHEUS','EPPA','C-ROADS','MERGE','CGEM','MINES']

df = pd.read_excel(SCI, sheet_name='data')
s = df[df['Variable'] == 'Emissions|CO2|Energy and Industrial Processes'].copy()
s['Family'] = s['Model'].map(lambda m: next((f for f in _F if f in str(m).upper()), str(m)))
w = (1.0 / s.groupby('Family')['Family'].transform('size')).values
def wmean(col):
    x = s[col].values; m = ~np.isnan(x); return np.sum(w[m]*x[m]) / np.sum(w[m])
proj = np.array([wmean(c) for c in YC])
p5  = np.array([np.nanpercentile(s[c], 5) for c in YC])
p95 = np.array([np.nanpercentile(s[c], 95) for c in YC])

# two COVID counterfactuals for 2020 (both avoid the dip, neither is "the" truth)
cf_interp = (OBS[2015] + OBS[2025]) / 2                 # interpolate 2015->2025 (uses future)
cf_fwd    = OBS[2015] + (OBS[2015]-OBS[2010])/5 * 5      # extrapolate 2010-2015 trend to 2020
me2020_real   = OBS[2020] - proj[2]
me2020_interp = cf_interp - proj[2]
me2020_fwd    = cf_fwd    - proj[2]
me2025        = OBS[2025] - proj[3]

fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 5.5), gridspec_kw={'width_ratios':[1.45, 1]})
fig.suptitle('Finding 1 — models assumed an emissions peak that did not happen', fontsize=13, fontweight='bold')

# ── Left: trajectories ──
axL.fill_between(X, p5, p95, color='0.8', alpha=0.5, lw=0, label='ensemble 5–95%')
axL.plot(X, proj, '-', color='#333', lw=2.2, marker='s', ms=5, label='ensemble mean (family-weighted)')
ox = list(OBS); oy = [OBS[y] for y in OBS]
axL.plot(ox, oy, '-', color='#E63329', lw=2, marker='o', ms=8, mec='black', label='observed (GCB 2025)')
axL.scatter([2020], [cf_interp], s=80, facecolor='white', edgecolor='#E63329', lw=1.6, zorder=6, label='2020 COVID-free counterfactual')
axL.annotate('reality dips (COVID)\nthen rises on trend', (2020, 34800), (2021.5, 31200), fontsize=8.5,
             color='#E63329', arrowprops=dict(arrowstyle='->', color='#E63329'))
axL.annotate('models peak ~2020\nthen decline', (2025, proj[3]), (2025.3, 39500), fontsize=8.5,
             color='#333', ha='right', arrowprops=dict(arrowstyle='->', color='#333'))
axL.annotate(f'ME 2025\n{me2025:+,.0f}', (2025, (38100+proj[3])/2), (2026.0, 36500), fontsize=9, fontweight='bold')
axL.set_xlim(2008, 2031); axL.set_ylim(28000, 42000); axL.set_xticks(YEARS)
axL.set_ylabel('CO₂ (Mt/yr)'); axL.set_xlabel('Year'); axL.legend(fontsize=8, loc='lower left')
axL.spines[['top','right']].set_visible(False); axL.grid(axis='y', alpha=0.15)

# ── Right: ME decomposition ──
bars = ['2020\n(raw)', '2020\n(interp.\ndetrend)', '2020\n(fwd-trend\ndetrend)', '2025\n(raw=detrend)']
vals = [me2020_real, me2020_interp, me2020_fwd, me2025]
cols = ['#D85A30', '#9ecae1', '#9ecae1', '#1D9E75']
b = axR.bar(bars, vals, color=cols, width=0.62)
axR.axhline(0, color='gray', lw=0.7)
for bar, v in zip(b, vals):
    axR.text(bar.get_x()+bar.get_width()/2, v + (120 if v >= 0 else -120),
             f'{v:+,.0f}', ha='center', va='bottom' if v >= 0 else 'top', fontsize=9, fontweight='bold')
axR.set_title('ME decomposition (Mt CO₂)', loc='left', fontsize=10, fontweight='bold')
axR.set_ylabel('obs − proj')
axR.text(0.5, -0.30, '2020 over-projection is COVID (flips positive under both\ncounterfactuals).  '
         '2025 under-projection is real → structural optimism.',
         transform=axR.transAxes, ha='center', fontsize=8.5, style='italic')
axR.spines[['top','right']].set_visible(False)

plt.tight_layout(); plt.savefig('co2_finding1.png', dpi=150, bbox_inches='tight')
print('Saved: co2_finding1.png')
print(f'ME 2020 raw {me2020_real:+.0f} | interp {me2020_interp:+.0f} | fwd-trend {me2020_fwd:+.0f} | 2025 {me2025:+.0f}')
