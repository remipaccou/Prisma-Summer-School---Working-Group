"""
Step 3 — Net-zero scenarios are biased low (not more imprecise).
Distribution of the per-scenario CO2 mean error (obs - proj, 2010-2025), NZ2070 vs non-NZ.
NZ is shifted toward positive (under-projection); both have similar magnitude (MAE_j ~5-6%).
All numbers family-weighted (1/n_family).
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
OBS = {'2010':33400,'2015':35400,'2020':34800,'2025':38100}
_F = ['MESSAGE','REMIND','IMACLIM','IMAGE','WITCH','POLES','GCAM','AIM','COFFEE','TIAM','GEM-E3','PROMETHEUS','EPPA','C-ROADS','MERGE','CGEM','MINES']
df = pd.read_excel(SCI, sheet_name='data'); meta = pd.read_excel(SCI, sheet_name='meta')
meta['key'] = meta['Model']+'|||'+meta['Scenario']
nz = meta.set_index('key')['Emissions Diagnostics|Year of Net Zero|CO2'].le(2070)
s = df[df['Variable']=='Emissions|CO2|Energy and Industrial Processes'].copy()
s['key'] = s['Model']+'|||'+s['Scenario']; s['Family'] = s['Model'].map(lambda m: next((f for f in _F if f in str(m).upper()), str(m)))
E = np.column_stack([OBS[y]-s[y].values for y in OBS])
s['ME_j'] = np.nanmean(E, axis=1); s['MAE_j'] = np.nanmean(np.abs(E), axis=1)
s['w'] = 1.0/s.groupby('Family')['Family'].transform('size'); s['nz'] = s['key'].map(nz)
A = s[s.nz==True].dropna(subset=['ME_j']); B = s[s.nz==False].dropna(subset=['ME_j'])
def wm(d, c): return np.average(d[c], weights=d['w'])
meA, meB = wm(A,'ME_j'), wm(B,'ME_j'); maA, maB = wm(A,'MAE_j'), wm(B,'MAE_j')

fig, ax = plt.subplots(figsize=(10, 5.6))
bins = np.arange(-6000, 6001, 500)
ax.hist(B['ME_j'], bins=bins, density=True, alpha=0.55, color='#378ADD', label=f'non-NZ (n={len(B)})', edgecolor='white', lw=0.3)
ax.hist(A['ME_j'], bins=bins, density=True, alpha=0.55, color='#D85A30', label=f'NZ2070 (n={len(A)})', edgecolor='white', lw=0.3)
ax.axvline(0, color='black', lw=1.2)
ax.axvline(meB, color='#1f5c99', lw=2, ls='--'); ax.axvline(meA, color='#a8431f', lw=2, ls='--')
top = ax.get_ylim()[1]
ax.text(meA+120, top*0.92, f'NZ mean +{meA:.0f}', color='#a8431f', fontsize=9, fontweight='bold')
ax.text(meB-120, top*0.80, f'non-NZ mean +{meB:.0f}', color='#1f5c99', fontsize=9, fontweight='bold', ha='right')
ax.text(0, -top*0.10, 'perfect (0)', ha='center', fontsize=8, color='0.4')
ax.annotate('biased LOW\n(under-project CO₂)', (2600, top*0.5), (3600, top*0.72),
            fontsize=9, color='#a8431f', ha='center', arrowprops=dict(arrowstyle='->', color='#a8431f'))
ax.set_xlabel('Per-scenario CO₂ error (obs − proj), mean over 2010–2025  (Mt)', fontsize=10)
ax.set_ylabel('density'); ax.set_xlim(-6000, 6000)
ax.set_title('Step 3 — Net-zero scenarios are biased low, not more imprecise\n'
             f'NZ clearly under-projects (+{meA:.0f}) vs non-NZ far less so (+{meB:.0f}); '
             f'MAE similar ({maA/354:.0f}% vs {maB/354:.0f}% of ~35 Gt) → a bias gap, not a precision gap',
             fontsize=10.5, fontweight='bold')
ax.legend(fontsize=9, loc='upper left'); ax.spines[['top','right']].set_visible(False); ax.grid(axis='y', alpha=0.15)
plt.tight_layout(); plt.savefig('nz_bias.png', dpi=150, bbox_inches='tight')
print(f'ME_j(fam): NZ +{meA:.0f} | non-NZ +{meB:.0f}    MAE_j(fam): NZ {maA:.0f} | non-NZ {maB:.0f}')
print('Saved: nz_bias.png')
