"""
Who correctly projected 2025, and why? -> it's the assumed AMBITION, not the model.
Monotonic gradient of the 2025 ME by AR6 climate category (C1 = 1.5°C ... C8 = >4°C).
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
df = pd.read_excel(SCI, sheet_name='data'); meta = pd.read_excel(SCI, sheet_name='meta')
meta['key'] = meta['Model']+'|||'+meta['Scenario']
cat = meta.set_index('key')['Climate Category|AR6 [Name]']
s = df[df['Variable'] == 'Emissions|CO2|Energy and Industrial Processes'].copy()
s['key'] = s['Model']+'|||'+s['Scenario']; s['cat'] = s['key'].map(cat)
s = s.dropna(subset=['cat', '2025']).copy()
s['Cnum'] = s['cat'].str[:2]                      # C1..C8
s['e25'] = 38100 - s['2025']

g = s.groupby('Cnum')['e25'].agg(['mean', 'count']).reindex([f'C{i}' for i in range(1, 9)]).dropna()
LAB = {'C1':'C1\n1.5°C','C2':'C2\n1.5°C\n(overshoot)','C3':'C3\n<2°C\n(likely)','C4':'C4\n<2°C',
       'C5':'C5\n<2.5°C','C6':'C6\n<3°C','C7':'C7\n<4°C','C8':'C8\n>4°C'}

fig, ax = plt.subplots(figsize=(13, 6))
colors = ['#C0392B' if v > 0 else '#2471A3' for v in g['mean']]
bars = ax.bar(range(len(g)), g['mean'], color=colors, width=0.72)
ax.axhline(0, color='black', lw=1)
for i, (idx, r) in enumerate(g.iterrows()):
    ax.text(i, r['mean'] + (250 if r['mean'] >= 0 else -250), f"{r['mean']:+,.0f}",
            ha='center', va='bottom' if r['mean'] >= 0 else 'top', fontsize=10, fontweight='bold')
    ax.text(i, -7600, f"n={int(r['count'])}", ha='center', fontsize=8, color='0.4')
ax.set_xticks(range(len(g))); ax.set_xticklabels([LAB[i] for i in g.index], fontsize=9)
ax.set_ylabel('2025 Error = reality − projection  (Mt CO₂)', fontsize=10)
ax.set_ylim(-8200, 9500)
ax.set_title("Who correctly projected 2025? — those who assumed LITTLE climate action\n"
             "The 2025 error is an almost perfect gradient of ambition: C1 (1.5°C) under-projects by +8 Gt, "
             "C8 (baseline) over-projects by −6 Gt", fontsize=11.5, fontweight='bold')
# "reality" zone
ax.axhspan(-700, 700, color='#1D9E75', alpha=0.12)
ax.text(len(g)-0.5, 700, '2025 reality ≈ here\n(« <3-4°C » world,\nweak action)',
        ha='right', va='bottom', fontsize=9, color='#1D7a52', fontweight='bold')
ax.text(2.4, 7600, 'too OPTIMISTIC (assumed decarbonization absent)', fontsize=9.5, color='#C0392B', ha='center')
ax.text(6.5, -7600, 'too PESSIMISTIC (baselines)', fontsize=9.5, color='#2471A3', ha='center')
ax.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('co2_2025_ambition.png', dpi=150, bbox_inches='tight')
print('Saved: co2_2025_ambition.png')
print(g.round(0).to_string())
