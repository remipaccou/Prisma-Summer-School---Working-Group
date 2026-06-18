"""
CO2 hindcast — global overview + selections
Fig 1: all scenario trajectories (2010-2100) + observed points
Fig 2: small-multiples by selection (all / NZ2070 / model-weighted / energy / CGE / hybrid)
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
VAR = 'Emissions|CO2|Energy and Industrial Processes'
OBS = {2010: 33400, 2015: 35400, 2020: 34800, 2025: 38100}     # Mt CO2, GCB 2025
YEARS = list(range(2010, 2101, 5)); YCOLS = [str(y) for y in YEARS]
HIND = [2010, 2015, 2020, 2025]
X = np.array(YEARS)

# ── families & 3-way economic class ─────────────────────────────────────
_FAMILIES = ['MESSAGE','REMIND','IMACLIM','IMAGE','WITCH','POLES','GCAM','AIM',
             'COFFEE','TIAM','GEM-E3','PROMETHEUS','EPPA','C-ROADS','MERGE','CGEM','MINES']
def to_family(m):
    up = str(m).upper()
    return next((f for f in _FAMILIES if f in up), str(m))
_CLASS = {'IMAGE':'energy','POLES':'energy','COFFEE':'energy','GCAM':'energy','TIAM':'energy','PROMETHEUS':'energy',
          'AIM':'CGE','GEM-E3':'CGE','IMACLIM':'CGE','EPPA':'CGE','CGEM':'CGE',
          'REMIND':'hybrid','WITCH':'hybrid','MESSAGE':'hybrid','MERGE':'hybrid',
          'C-ROADS':'other','MINES':'other'}

df = pd.read_excel(SCI, sheet_name='data')
meta = pd.read_excel(SCI, sheet_name='meta')
meta['nzy'] = pd.to_numeric(meta['Emissions Diagnostics|Year of Net Zero|CO2'], errors='coerce')
nz_keys = set((meta.loc[meta['nzy'] <= 2070, 'Model'] + '|||' + meta.loc[meta['nzy'] <= 2070, 'Scenario']))

s = df[df['Variable'] == VAR].copy()
s['Family'] = s['Model'].map(to_family)
s['Class']  = s['Family'].map(_CLASS).fillna('other')
s['nz2070'] = (s['Model'] + '|||' + s['Scenario']).isin(nz_keys)

# ── weighted hindcast metrics (family-balanced within the subset) ───────
def fam_w(sub): return (1.0 / sub.groupby('Family')['Family'].transform('size')).values
def metrics(sub, weighted=True):
    w = fam_w(sub) if weighted else np.ones(len(sub))
    E, W = [], []
    for y in HIND:
        e = OBS[y] - sub[str(y)].values; m = ~np.isnan(e)
        E.append(e[m]); W.append(w[m])
    e = np.concatenate(E); w = np.concatenate(W)
    return (np.sum(w*e)/w.sum(), np.sum(w*np.abs(e))/w.sum(), np.sqrt(np.sum(w*e**2)/w.sum()))

def obs_pts(ax):
    ax.scatter(list(OBS), [OBS[y] for y in OBS], c='#E63329', s=55, zorder=6,
               edgecolor='black', lw=0.8, label='Observed (GCB 2025)')

def spaghetti(ax, sub, color='0.5', alpha=0.05, lw=0.4):
    M = sub[YCOLS].values
    ax.plot(X, M.T, color=color, alpha=alpha, lw=lw, zorder=1)
    med = np.nanmedian(M, 0); p5 = np.nanpercentile(M, 5, 0); p95 = np.nanpercentile(M, 95, 0)
    ax.fill_between(X, p5, p95, color=color, alpha=0.18, zorder=2, lw=0)
    ax.plot(X, med, color='black', lw=1.4, zorder=3, label='Median')
    ax.axvline(2025, color='gray', ls=':', lw=1, zorder=1)
    ax.axhline(0, color='gray', lw=0.6, zorder=1)

# ════════════════════════ FIG 1 — global overview ══════════════════════
fig, (axL, axR) = plt.subplots(1, 2, figsize=(15, 5.6),
                               gridspec_kw={'width_ratios': [1.5, 1]})
fig.suptitle('CO₂ Emissions (Energy & Industrial Processes) — full SCI-2025 ensemble  '
             f'(n={len(s)} scenarios)', fontsize=13, fontweight='bold')

spaghetti(axL, s); obs_pts(axL)
axL.set_title('Full horizon 2010–2100', loc='left', fontsize=10, fontweight='bold')
axL.set_ylabel('Mt CO₂/yr'); axL.set_xlabel('Year')
axL.legend(loc='upper right', fontsize=9); axL.spines[['top','right']].set_visible(False)
axL.text(2026, axL.get_ylim()[1]*0.93, 'hindcast │ future', fontsize=8, color='gray')

# zoom on the hindcast window
spaghetti(axR, s); obs_pts(axR)
axR.set_xlim(2008, 2032); axR.set_ylim(15000, 55000)
axR.set_title('Zoom: hindcast window 2010–2030', loc='left', fontsize=10, fontweight='bold')
axR.set_xlabel('Year'); axR.legend(loc='lower left', fontsize=9)
axR.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('../figures/co2_overview.png', dpi=150, bbox_inches='tight')
print('Saved: co2_overview.png')

# ════════════════════════ FIG 2 — selections ═══════════════════════════
CCOL = {'energy':'#378ADD','CGE':'#D85A30','hybrid':'#7E57C2'}
panels = [
    ('All scenarios',        s,                       '0.5'),
    ('Net-Zero by 2070',     s[s['nz2070']],          '#1D9E75'),
    ('Model-weighted (family means)', None,           '0.4'),     # special
    ('Energy-system models', s[s['Class']=='energy'], CCOL['energy']),
    ('Economy / CGE models', s[s['Class']=='CGE'],    CCOL['CGE']),
    ('Hybrid models',        s[s['Class']=='hybrid'], CCOL['hybrid']),
]
fig, axes = plt.subplots(2, 3, figsize=(16, 9), sharex=True)
fig.suptitle('CO₂ hindcast — selections  |  lines = scenarios, dots = observed, '
             'band = 5–95%  |  metrics = family-weighted ME/MAE/RMSE on 2010–2025 (Mt CO₂)',
             fontsize=12, fontweight='bold')

for ax, (title, sub, color) in zip(axes.flat, panels):
    if title.startswith('Model-weighted'):
        # one mean trajectory per family
        fam_means = s.groupby('Family')[YCOLS].mean()
        ax.plot(X, fam_means.values.T, color=color, alpha=0.55, lw=1.0, zorder=1)
        med = np.nanmedian(fam_means.values, 0)
        ax.fill_between(X, np.nanpercentile(fam_means.values,5,0), np.nanpercentile(fam_means.values,95,0),
                        color=color, alpha=0.15, zorder=2, lw=0)
        ax.plot(X, med, color='black', lw=1.4, zorder=3)
        ax.axvline(2025, color='gray', ls=':', lw=1); ax.axhline(0, color='gray', lw=0.6)
        me, mae, rmse = metrics(s, weighted=True); n = f'{s["Family"].nunique()} families'
    else:
        spaghetti(ax, sub, color=color, alpha=min(0.5, 30/len(sub)))
        obs_pts(ax)
        me, mae, rmse = metrics(sub, weighted=True); n = f'n={len(sub)}'
    ax.set_title(f'{title}  ({n})', loc='left', fontsize=10, fontweight='bold')
    ax.set_xlim(2008, 2052); ax.set_ylim(-12000, 55000)
    ax.text(0.97, 0.04, f'ME {me:+,.0f}\nMAE {mae:,.0f}\nRMSE {rmse:,.0f}',
            transform=ax.transAxes, ha='right', va='bottom', fontsize=8.5,
            bbox=dict(boxstyle='round', fc='white', ec='0.7', alpha=0.9))
    ax.spines[['top','right']].set_visible(False)
for ax in axes[:,0]: ax.set_ylabel('Mt CO₂/yr')
for ax in axes[1,:]: ax.set_xlabel('Year')
plt.tight_layout(); plt.savefig('../figures/co2_views.png', dpi=150, bbox_inches='tight')
print('Saved: co2_views.png')

# ════════════════════════ metrics table ════════════════════════════════
print('\nHindcast metrics on 2010–2025 (Mt CO₂)')
print(f'{"selection":<26}{"n":>6} | {"ME(scen)":>9}{"ME(fam)":>9} | {"MAE(fam)":>9}{"RMSE(fam)":>10}')
print('-'*82)
rows = [('All', s), ('Net-Zero 2070', s[s['nz2070']]), ('Energy', s[s['Class']=='energy']),
        ('CGE / economy', s[s['Class']=='CGE']), ('Hybrid', s[s['Class']=='hybrid'])]
for name, sub in rows:
    me_s = metrics(sub, weighted=False)[0]; me_f, mae_f, rmse_f = metrics(sub, weighted=True)
    print(f'{name:<26}{len(sub):>6} | {me_s:>+9,.0f}{me_f:>+9,.0f} | {mae_f:>9,.0f}{rmse_f:>10,.0f}')
