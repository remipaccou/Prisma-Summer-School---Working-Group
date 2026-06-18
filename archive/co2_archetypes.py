"""
CO2 hindcast — focused test on a few archetype models (less dispersion than full pooling)
ENERGY archetypes : POLES, TIAM, COFFEE
ECONOMY archetypes: GEM-E3, IMACLIM, WITCH
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
VAR = 'Emissions|CO2|Energy and Industrial Processes'
OBS = {2010: 33400, 2015: 35400, 2020: 34800, 2025: 38100}
HIND = [2010, 2015, 2020, 2025]
YEARS = list(range(2010, 2051, 5)); YCOLS = [str(y) for y in YEARS]; X = np.array(YEARS)

ENERGY  = ['POLES', 'TIAM', 'COFFEE']
ECONOMY = ['GEM-E3', 'IMACLIM', 'WITCH']
GROUPS = {'energy': ENERGY, 'economy': ECONOMY}
_FAMILIES = ['MESSAGE','REMIND','IMACLIM','IMAGE','WITCH','POLES','GCAM','AIM',
             'COFFEE','TIAM','GEM-E3','PROMETHEUS','EPPA','C-ROADS','MERGE','CGEM','MINES']
def to_family(m):
    up = str(m).upper(); return next((f for f in _FAMILIES if f in up), str(m))

df = pd.read_excel(SCI, sheet_name='data')
s = df[df['Variable'] == VAR].copy()
s['Family'] = s['Model'].map(to_family)

def metrics(sub):
    E = []
    for y in HIND:
        e = OBS[y] - sub[str(y)].values; E.append(e[~np.isnan(e)])
    e = np.concatenate(E)
    return e.mean(), np.abs(e).mean(), np.sqrt((e**2).mean())

def me_by_year(fams):
    """family-weighted ME per hindcast year across the given families"""
    sub = s[s['Family'].isin(fams)]
    out = []
    for y in HIND:
        per = [ (OBS[y] - sub[sub.Family==f][str(y)]).mean() for f in fams ]
        out.append(np.nanmean(per))          # each model weighted equally
    return out

CE = {'energy': '#378ADD', 'economy': '#D85A30'}

# ── FIG 1: per-model panels ─────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(15, 8.5), sharex=True, sharey=True)
fig.suptitle('CO₂ hindcast — archetype models  (lines = scenarios, dots = observed GCB 2025)',
             fontsize=13, fontweight='bold')
for r, (g, fams) in enumerate(GROUPS.items()):
    for c, fam in enumerate(fams):
        ax = axes[r, c]; sub = s[s['Family'] == fam]
        ax.plot(X, sub[YCOLS].values.T, color=CE[g], alpha=min(0.6, 25/max(len(sub),1)), lw=0.6, zorder=1)
        ax.plot(X, np.nanmedian(sub[YCOLS].values, 0), color='black', lw=1.4, zorder=3)
        ax.scatter(list(OBS), [OBS[y] for y in OBS], c='#E63329', s=45, ec='black', lw=0.7, zorder=5)
        ax.axvline(2025, color='gray', ls=':', lw=1); ax.axhline(0, color='gray', lw=0.5)
        me, mae, rmse = metrics(sub)
        ax.set_title(f'{fam}  ({g}, n={len(sub)})', loc='left', fontsize=10, fontweight='bold')
        ax.text(0.97, 0.04, f'ME {me:+,.0f}\nMAE {mae:,.0f}\nRMSE {rmse:,.0f}', transform=ax.transAxes,
                ha='right', va='bottom', fontsize=8.5, bbox=dict(boxstyle='round', fc='white', ec='0.7', alpha=.9))
        ax.set_xlim(2008, 2042); ax.set_ylim(10000, 46000); ax.spines[['top','right']].set_visible(False)
for ax in axes[:, 0]: ax.set_ylabel('Mt CO₂/yr')
for ax in axes[1, :]: ax.set_xlabel('Year')
plt.tight_layout(); plt.savefig('co2_archetypes.png', dpi=150, bbox_inches='tight'); print('Saved: co2_archetypes.png')

# ── FIG 2: group summary ────────────────────────────────────────────────
fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4.5))
for g, fams in GROUPS.items():
    a1.plot(HIND, me_by_year(fams), 'o-', color=CE[g], lw=2, ms=7, label=f'{g} ({", ".join(fams)})')
a1.axhline(0, color='gray', lw=0.6); a1.set_title('ME per year — energy vs economy archetypes',
            loc='left', fontsize=11, fontweight='bold')
a1.set_xlabel('Year'); a1.set_ylabel('ME (Mt CO₂)  obs−proj'); a1.legend(fontsize=8); a1.set_xticks(HIND)
a1.spines[['top','right']].set_visible(False)

labels = ['ME', 'MAE', 'RMSE']; xb = np.arange(3); w = 0.38
for k, (g, fams) in enumerate(GROUPS.items()):
    vals = [np.nanmean([metrics(s[s.Family == f])[i] for f in fams]) for i in range(3)]
    a2.bar(xb + (k-0.5)*w, vals, w, color=CE[g], label=g)
a2.axhline(0, color='gray', lw=0.6); a2.set_xticks(xb); a2.set_xticklabels(labels)
a2.set_title('Group metrics (each model weighted equally)', loc='left', fontsize=11, fontweight='bold')
a2.set_ylabel('Mt CO₂'); a2.legend(fontsize=9); a2.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('co2_archetypes_summary.png', dpi=150, bbox_inches='tight'); print('Saved: co2_archetypes_summary.png')

# ── table ───────────────────────────────────────────────────────────────
print('\nPer-model hindcast metrics 2010–2025 (Mt CO₂)')
print(f'{"model":<12}{"group":<9}{"n":>5} | {"ME":>8}{"MAE":>8}{"RMSE":>8}')
print('-'*54)
for g, fams in GROUPS.items():
    for f in fams:
        sub = s[s.Family == f]; me, mae, rmse = metrics(sub)
        print(f'{f:<12}{g:<9}{len(sub):>5} | {me:>+8,.0f}{mae:>8,.0f}{rmse:>8,.0f}')
    gm = [np.nanmean([metrics(s[s.Family == f])[i] for f in fams]) for i in range(3)]
    print(f'{"→ "+g+" avg":<21} | {gm[0]:>+8,.0f}{gm[1]:>8,.0f}{gm[2]:>8,.0f}')
    print('-'*54)
