"""
L1 — Is the SCI ensemble a calibrated probabilistic forecast?  (Lafond, slides 5 & 29)
For each variable we locate where the OBSERVED value falls inside the ensemble distribution
(its percentile / PIT). A calibrated forecast would put reality near the median (~50th) about
half the time. Instead reality sits in the TAILS -> the ensemble is biased and over-confident.
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
VARS = {  # variable : (label, observed values 2010/2015/2020/2025)
    'Emissions|CO2|Energy and Industrial Processes': ('CO₂', {'2010':33400,'2015':35400,'2020':34800,'2025':38100}),
    'Primary Energy|Coal':           ('Coal',    {'2010':148,'2015':155,'2020':152,'2025':164}),
    'Capacity|Electricity|Solar|PV': ('Solar PV',{'2010':40,'2015':227,'2020':714,'2025':2392}),
    'Capacity|Electricity|Wind':     ('Wind',    {'2010':198,'2015':433,'2020':733,'2025':1291}),
    'Capacity|Electricity|Nuclear':  ('Nuclear', {'2010':375,'2015':383,'2020':393,'2025':377}),
    'GDP|PPP':                       ('GDP',     {'2010':87774,'2015':100690,'2020':107100,'2025':122000}),
}
df = pd.read_excel(SCI, sheet_name='data')
def pctile(var, year, obs):
    x = df[df['Variable']==var][year].dropna().values
    return 100*np.mean(x < obs)
rows = []
for v, (lab, obs) in VARS.items():
    rows.append({'var': lab, **{f'p{y}': pctile(v, y, obs[y]) for y in ['2015','2020','2025']}})
R = pd.DataFrame(rows).set_index('var').loc[['GDP','Nuclear','Wind','CO₂','Coal','Solar PV']]  # order low->high p2025

fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={'width_ratios':[1, 1]})
fig.suptitle('L1 — The SCI ensemble is not a calibrated forecast: reality sits in the tails, not the centre',
             fontsize=12.5, fontweight='bold')

# ── Left: 2025 PIT lollipop ──
y = np.arange(len(R))
axL.axvspan(25, 75, color='#1D9E75', alpha=0.10)
axL.axvline(50, color='#1D9E75', lw=1.4, ls='--')
axL.text(50, len(R)-0.3, 'calibrated\n(median)', ha='center', va='bottom', fontsize=8, color='#1D7a52')
for i, (name, r) in enumerate(R.iterrows()):
    p = r['p2025']; col = '#C0392B' if (p>75 or p<25) else '#888'
    axL.plot([50, p], [i, i], color=col, lw=2, zorder=2)
    axL.scatter(p, i, s=90, color=col, zorder=3)
    axL.text(p + (3 if p<50 else -3), i, f'{p:.0f}', va='center', ha='left' if p<50 else 'right', fontsize=9, fontweight='bold')
axL.set_yticks(y); axL.set_yticklabels(R.index)
axL.set_xlim(0, 100); axL.set_xlabel('Percentile of observed 2025 in the ensemble (PIT)')
axL.text(2, -0.9, 'ensemble too HIGH', fontsize=8, color='#2471A3')
axL.text(98, -0.9, 'ensemble too LOW', fontsize=8, color='#C0392B', ha='right')
axL.set_title('Where does reality 2025 fall in the cloud?', loc='left', fontsize=10, fontweight='bold')
axL.spines[['top','right']].set_visible(False)

# ── Right: drift 2015 -> 2025 (calibration degrades with horizon) ──
axR.axhspan(25, 75, color='#1D9E75', alpha=0.10); axR.axhline(50, color='#1D9E75', lw=1.2, ls='--')
for i, (name, r) in enumerate(R.iterrows()):
    axR.annotate('', (1, r['p2025']), (0, r['p2015']), arrowprops=dict(arrowstyle='->', color='#534AB7', lw=1.6))
    axR.text(-0.04, r['p2015'], name, ha='right', va='center', fontsize=8.5)
    axR.text(1.04, r['p2025'], f"{r['p2025']:.0f}", ha='left', va='center', fontsize=8.5, fontweight='bold')
axR.set_xlim(-0.45, 1.3); axR.set_ylim(0, 100); axR.set_xticks([0,1]); axR.set_xticklabels(['2015','2025'])
axR.set_ylabel('Percentile of observed (PIT)')
axR.set_title('Calibration degrades with horizon\n(reality drifts from centre to tails)', loc='left', fontsize=10, fontweight='bold')
axR.spines[['top','right']].set_visible(False)

plt.tight_layout(); plt.savefig('calibration_pit.png', dpi=150, bbox_inches='tight')
print(R.round(0).to_string()); print('Saved: calibration_pit.png')
