"""
Naive-benchmark test (Lafond/Farmer style): does the IAM ensemble beat a trivial rule
at predicting 2025?  Train on 2010+2015 (pre-COVID), forecast 2025 (10-yr-ahead).
Benchmarks: random walk (persistence), linear trend, log-linear (geometric) trend.
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
VARS = {
    'Emissions|CO2|Energy and Industrial Processes': dict(obs={10:33400,15:35400,25:38100}, short='CO₂'),
    'Primary Energy|Coal':           dict(obs={10:148,15:155,25:164}, short='Coal'),
    'Capacity|Electricity|Solar|PV': dict(obs={10:40,15:227,25:2392}, short='Solar PV'),
    'Capacity|Electricity|Wind':     dict(obs={10:198,15:433,25:1291}, short='Wind'),
    'Capacity|Electricity|Nuclear':  dict(obs={10:375,15:383,25:377}, short='Nuclear'),
    'GDP|PPP':                       dict(obs={10:87774,15:100690,25:122000}, short='GDP'),
}
df = pd.read_excel(SCI, sheet_name='data')

def naives(o10, o15):
    rw  = o15                                   # persistence
    lin = o15 + 2*(o15 - o10)                    # linear trend (slope from 2010-15, *10yr)
    log = o15 * (o15/o10)**2 if o10 > 0 else np.nan   # geometric/exponential trend
    return {'RW': rw, 'linear': lin, 'log-trend': log}

rows = []
for v, d in VARS.items():
    o10, o15, o25 = d['obs'][10], d['obs'][15], d['obs'][25]
    sv = df[df['Variable'] == v]
    scen25 = sv['2025'].dropna().values
    ens_med = np.median(scen25)
    nv = naives(o10, o15)
    nv_err = {k: abs(o25 - val) for k, val in nv.items()}
    best_k = min(nv_err, key=nv_err.get); best_err = nv_err[best_k]; best_val = nv[best_k]
    ens_err = abs(o25 - ens_med)
    skill = ens_err / best_err
    # fraction of scenarios worse than the best naive
    pct_beaten = np.mean(np.abs(o25 - scen25) > best_err) * 100
    rows.append(dict(var=d['short'], obs25=o25, ens=ens_med, ens_pe=100*ens_err/o25,
                     best_naive=best_k, naive_val=best_val, naive_pe=100*best_err/o25,
                     skill=skill, pct_beaten=pct_beaten, n=len(scen25), **{f'nv_{k}': val for k,val in nv.items()}))
R = pd.DataFrame(rows)

print("Naive benchmark test — forecast of 2025 from 2010+2015 (pre-COVID)\n")
print(f"{'var':<9}{'obs25':>9}{'ensemble':>10}{'best naive':>16}{'ens %err':>9}{'naive %err':>11}{'skill':>7}{'% scen worse':>13}")
print('-'*86)
for _, r in R.iterrows():
    print(f"{r['var']:<9}{r['obs25']:>9,.0f}{r['ens']:>10,.0f}{r['best_naive']+'='+format(r['naive_val'],',.0f'):>16}"
          f"{r['ens_pe']:>8.0f}%{r['naive_pe']:>10.0f}%{r['skill']:>7.1f}{r['pct_beaten']:>12.0f}%")
print("\nskill = |err ensemble| / |err best naive|.  >1 = the ruler beats the ensemble.")
print("full naive detail:")
print(R[['var','nv_RW','nv_linear','nv_log-trend']].round(0).to_string(index=False))

# ── figure ──
fig, ax = plt.subplots(figsize=(13, 6))
x = np.arange(len(R)); w = 0.38
b1 = ax.bar(x-w/2, R['ens_pe'], w, color='#534AB7', label='IAM ensemble (median)')
b2 = ax.bar(x+w/2, R['naive_pe'], w, color='#9aa0a6', label='best naive rule')
for i, r in R.iterrows():
    loses = r['skill'] > 1
    ax.text(i, max(r['ens_pe'], r['naive_pe'])+2,
            f"skill {r['skill']:.1f}\n{'ruler wins' if loses else 'ensemble wins'}",
            ha='center', fontsize=8, fontweight='bold', color='#C0392B' if loses else '#1D9E75')
ax.set_xticks(x); ax.set_xticklabels([f"{r['var']}\n(naive: {r['best_naive']})" for _,r in R.iterrows()], fontsize=9)
ax.set_ylabel('2025 forecast error  (% of observed)', fontsize=10)
ax.set_title('Does the IAM ensemble beat a trivial rule at predicting 2025?\n'
             'Forecast made with info 2010-2015 (pre-COVID). skill>1 = the rule wins.',
             fontsize=12, fontweight='bold')
ax.legend(fontsize=9); ax.spines[['top','right']].set_visible(False); ax.grid(axis='y', alpha=0.15)
plt.tight_layout(); plt.savefig('co2_benchmark.png', dpi=150, bbox_inches='tight')
print('\nSaved: co2_benchmark.png')
