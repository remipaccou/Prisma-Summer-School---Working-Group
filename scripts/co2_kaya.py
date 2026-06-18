"""
Kaya decomposition of the 2025 CO2 hindcast error (inspired by Pretis-Roser 2017, Burgess 2021).
CO2 = GDP x (CO2/GDP). The ensemble over-projects GDP but assumes too much decarbonisation;
the carbon-intensity error dominates and flips the sign -> our miss is DECOUPLING optimism, not growth.
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
df = pd.read_excel(SCI, sheet_name='data')
_F = ['MESSAGE','REMIND','IMACLIM','IMAGE','WITCH','POLES','GCAM','AIM','COFFEE','TIAM','GEM-E3','PROMETHEUS','EPPA','C-ROADS','MERGE','CGEM','MINES']
def ens(var):
    s = df[df['Variable'] == var].copy(); s['F'] = s['Model'].map(lambda m: next((f for f in _F if f in str(m).upper()), str(m)))
    w = (1/s.groupby('F')['F'].transform('size')).values; x = s['2025'].values; m = ~np.isnan(x)
    return np.sum(w[m]*x[m]) / np.sum(w[m])

OBS_CO2, OBS_GDP = 38100, 122000
co2_e, gdp_e = ens('Emissions|CO2|Energy and Industrial Processes'), ens('GDP|PPP')
ci_o, ci_e = OBS_CO2/OBS_GDP, co2_e/gdp_e
# waterfall levels: obs -> (apply GDP factor) -> (apply CI factor) = ensemble
lvl_gdp = OBS_CO2 * (gdp_e/OBS_GDP)        # if intensity were right but GDP wrong
gdp_eff = lvl_gdp - OBS_CO2
ci_eff  = co2_e - lvl_gdp

fig, ax = plt.subplots(figsize=(10, 6))
xs = ['Observed\n2025', 'GDP effect\n(+14%)', 'decarbonisation effect\n(−18%)', 'Ensemble\n(family median)']
# bar 0 and bar 3 are absolute; 1 and 2 are floating deltas
ax.bar(0, OBS_CO2, color='#E63329', width=0.6)
ax.bar(3, co2_e, color='#534AB7', width=0.6)
ax.bar(1, gdp_eff, bottom=OBS_CO2, color='#C0392B', width=0.6)              # GDP pushes up
ax.bar(2, ci_eff, bottom=lvl_gdp, color='#2471A3', width=0.6)              # decarbonisation pushes down
# connectors
for x0, y in [(0, OBS_CO2), (1, lvl_gdp), (2, co2_e)]:
    ax.plot([x0+0.3, x0+0.7], [y, y], color='0.5', lw=1, ls='--')
# labels
ax.text(0, OBS_CO2+250, f'{OBS_CO2:,}', ha='center', fontweight='bold')
ax.text(3, co2_e+250, f'{co2_e:,.0f}', ha='center', fontweight='bold', color='#534AB7')
ax.text(1, lvl_gdp+250, f'+{gdp_eff:,.0f}', ha='center', fontweight='bold', color='#C0392B')
ax.text(2, lvl_gdp+200, f'{ci_eff:,.0f}', ha='center', va='bottom', fontweight='bold', color='#2471A3')
ax.annotate('', (3.45, OBS_CO2), (3.45, co2_e), arrowprops=dict(arrowstyle='<->', color='#1D9E75', lw=1.8))
ax.text(3.5, (OBS_CO2+co2_e)/2, f'net error\n−{OBS_CO2-co2_e:,.0f}', color='#1D9E75', fontsize=9, fontweight='bold', va='center')
ax.set_xticks(range(4)); ax.set_xticklabels(xs)
ax.set_ylabel('CO₂ 2025 (Mt)'); ax.set_ylim(30000, 45000)
ax.set_title("Kaya decomposition of the 2025 CO₂ error\n"
             "Over-projected GDP pushes CO₂ up (+5 147); the assumed decarbonisation\n"
             "crushes it (−7 729) → our bias = DECOUPLING optimism, not growth",
             fontsize=11, fontweight='bold')
ax.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('../figures/co2_kaya.png', dpi=150, bbox_inches='tight')
print(f"obs {OBS_CO2} -> +GDP {gdp_eff:+,.0f} -> +CI {ci_eff:+,.0f} -> ens {co2_e:,.0f}")
print('Saved: co2_kaya.png')
