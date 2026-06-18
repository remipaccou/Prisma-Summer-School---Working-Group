"""
Part C (honest) — the net-zero SHARE is not even directionally robust to the credibility variable.
Filter on CO2 -> NZ share DOWN (~20%); filter on solar -> UP (~45%); balanced -> ~25%.
Reason: reality vindicated NZ on solar (the boom) but refuted it on CO2/coal (the addition signature).
=> Lafond slide 3 proven: you cannot extract an unconditional probability from conditional forecasts.
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
HIND = ['2010','2015','2020','2025']
VARS = {'Emissions|CO2|Energy and Industrial Processes': {'2010':33400,'2015':35400,'2020':34800,'2025':38100},
        'Primary Energy|Coal':           {'2010':148,'2015':155,'2020':152,'2025':164},
        'Capacity|Electricity|Solar|PV': {'2010':40,'2015':227,'2020':714,'2025':2392}}
df = pd.read_excel(SCI, sheet_name='data'); meta = pd.read_excel(SCI, sheet_name='meta')
meta['key'] = meta['Model']+'|||'+meta['Scenario']; nzy = meta.set_index('key')['Emissions Diagnostics|Year of Net Zero|CO2']
def nmae(var, obs):
    s = df[df['Variable']==var].copy(); s['key'] = s['Model']+'|||'+s['Scenario']
    eps = np.column_stack([obs[y]-s[y].values for y in HIND])
    return pd.Series(np.nanmean(np.abs(eps),axis=1)/np.mean(list(obs.values())), index=s['key'].values)
M = pd.DataFrame({'CO2':nmae('Emissions|CO2|Energy and Industrial Processes',VARS['Emissions|CO2|Energy and Industrial Processes']),
                  'Coal':nmae('Primary Energy|Coal',VARS['Primary Energy|Coal']),
                  'Solar':nmae('Capacity|Electricity|Solar|PV',VARS['Capacity|Electricity|Solar|PV'])})
M['nz'] = pd.Series(nzy.le(2070)).reindex(M.index); M = M.dropna()
for c in ['CO2','Coal','Solar']: M[c+'_r'] = M[c].rank(pct=True)
M['bal'] = M[['CO2_r','Coal_r','Solar_r']].mean(axis=1)
naive = M['nz'].mean()*100

def curve(score):
    o = M.sort_values(score); fr = np.linspace(0.05,1.0,40)
    return fr*100, np.array([o.iloc[:max(int(q*len(o)),1)]['nz'].mean()*100 for q in fr])

fig, ax = plt.subplots(figsize=(11, 6))
for score, col, lab in [('Solar_r','#D85A30','SOLAR filter → NZ UP (they predicted the boom)'),
                        ('bal','#7E57C2','BALANCED filter (CO₂+coal+solar, ranks)'),
                        ('CO2_r','#378ADD','CO₂ filter → NZ DOWN (no decarbonisation)')]:
    x, y = curve(score); ax.plot(x, y, '-o', color=col, lw=2.2, ms=3.5, label=lab)
ax.axhline(naive, color='gray', ls=':', lw=1.5); ax.text(101, naive, f'naive {naive:.0f}%', va='center', fontsize=9, color='gray')
ax.annotate('← stricter', (12, curve('CO2_r')[1][1]), (24, 8), fontsize=9, arrowprops=dict(arrowstyle='->'))
ax.set_xlabel("% of scenarios kept (most credible first)", fontsize=10)
ax.set_ylabel('net-zero 2070 scenario SHARE  (%)', fontsize=10)
ax.set_title("Part C — the « corrected NZ share » is not robust: 20%→48% depending on the variable\n"
             "Lafond slide 3: you cannot extract an unconditional probability from conditional forecasts",
             fontsize=11, fontweight='bold')
ax.set_xlim(0, 108); ax.set_ylim(0, 52)
ax.legend(fontsize=8.5, loc='upper right'); ax.spines[['top','right']].set_visible(False); ax.grid(alpha=0.15)
plt.tight_layout(); plt.savefig('partC_sensitivity.png', dpi=150, bbox_inches='tight')
print(f"naive {naive:.0f}% (n={len(M)})")
for q in [0.25,0.5]:
    print(f"  keep {int(q*100)}%: solar {curve('Solar_r')[1][np.argmin(abs(np.linspace(.05,1,40)-q))]:.0f}% | "
          f"balanced {curve('bal')[1][np.argmin(abs(np.linspace(.05,1,40)-q))]:.0f}% | "
          f"CO2 {curve('CO2_r')[1][np.argmin(abs(np.linspace(.05,1,40)-q))]:.0f}%")
print('Saved: partC_sensitivity.png')
