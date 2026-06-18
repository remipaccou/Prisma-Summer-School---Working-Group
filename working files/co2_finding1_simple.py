"""Finding 1 — version pédagogique (claire)."""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
OBS = {2010: 33400, 2015: 35400, 2020: 34800, 2025: 38100}
YEARS = [2010, 2015, 2020, 2025]; YC = [str(y) for y in YEARS]
_F = ['MESSAGE','REMIND','IMACLIM','IMAGE','WITCH','POLES','GCAM','AIM','COFFEE','TIAM','GEM-E3','PROMETHEUS','EPPA','C-ROADS','MERGE','CGEM','MINES']
df = pd.read_excel(SCI, sheet_name='data')
s = df[df['Variable'] == 'Emissions|CO2|Energy and Industrial Processes'].copy()
s['Family'] = s['Model'].map(lambda m: next((f for f in _F if f in str(m).upper()), str(m)))
w = (1.0 / s.groupby('Family')['Family'].transform('size')).values
proj = [float(np.nansum(w*s[c].values) / np.nansum(w*~np.isnan(s[c].values))) for c in YC]
cf2020 = (OBS[2015] + OBS[2025]) / 2

fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={'width_ratios': [1.4, 1]})

# ── gauche : 2 courbes ──
X = YEARS
axL.plot(X, proj, '-s', color='#333', lw=2.4, ms=8, label='Ce que les modèles prévoyaient', zorder=4)
axL.plot(X, [OBS[y] for y in X], '-o', color='#E63329', lw=2.4, ms=9, mec='black', label='Réalité observée', zorder=5)
axL.scatter([2020], [cf2020], s=130, facecolor='white', edgecolor='#E63329', lw=2, zorder=6)
axL.annotate('2020 sans COVID\n(~36 750)', (2020, cf2020), (2016.3, 37600), fontsize=9, color='#E63329',
             arrowprops=dict(arrowstyle='->', color='#E63329'))
axL.annotate('creux COVID', (2020, OBS[2020]), (2020.2, 33200), fontsize=9, color='#E63329',
             arrowprops=dict(arrowstyle='->', color='#E63329'))
# flèche du gap 2025
axL.annotate('', (2025, OBS[2025]), (2025, proj[3]), arrowprops=dict(arrowstyle='<->', color='#1D9E75', lw=2))
axL.text(2025.15, (OBS[2025]+proj[3])/2, 'écart +2 582\n(VRAI problème :\nmodèles trop\noptimistes)', fontsize=9,
         color='#1D9E75', fontweight='bold', va='center')
axL.text(2021.3, 35900, 'les modèles attendaient\nun pic puis un déclin', fontsize=8.5, color='#333', style='italic')
axL.set_xticks(YEARS); axL.set_xlim(2009, 2028.5); axL.set_ylim(32000, 39500)
axL.set_ylabel('CO₂ (Mt/an)'); axL.set_xlabel('Année'); axL.legend(loc='upper left', fontsize=9)
axL.set_title('Modèles vs réalité', loc='left', fontsize=11, fontweight='bold')
axL.spines[['top','right']].set_visible(False); axL.grid(axis='y', alpha=0.15)

# ── droite : 3 barres, langage simple ──
labels = ['2020\nbrut', '2020\nsans COVID', '2025']
vals = [OBS[2020]-proj[2], cf2020-proj[2], OBS[2025]-proj[3]]
cols = ['#D85A30', '#9ecae1', '#1D9E75']
notes = ['ON DIRAIT\ntrop haut…\nmais c’est\nle COVID', 'en fait\n≈ juste', 'VRAI problème :\ntrop bas\n(optimisme)']
b = axR.bar(labels, vals, color=cols, width=0.6)
axR.axhline(0, color='gray', lw=0.8)
for bar, v, nt in zip(b, vals, notes):
    axR.text(bar.get_x()+bar.get_width()/2, v+(130 if v>=0 else -130), f'{v:+,.0f}',
             ha='center', va='bottom' if v>=0 else 'top', fontsize=10, fontweight='bold')
    axR.text(bar.get_x()+bar.get_width()/2, 1600 if v < 0 else -600, nt, ha='center', va='center', fontsize=8)
axR.set_title('Erreur = réalité − modèles  (Mt CO₂)', loc='left', fontsize=11, fontweight='bold')
axR.set_ylim(-2200, 3100); axR.spines[['top','right']].set_visible(False)

fig.suptitle('Une fois le COVID retiré, les modèles sont trop bas AUX DEUX dates → biais constant d’optimisme',
             fontsize=12, fontweight='bold')
plt.tight_layout(); plt.savefig('co2_finding1_simple.png', dpi=150, bbox_inches='tight')
print('Saved: co2_finding1_simple.png')
