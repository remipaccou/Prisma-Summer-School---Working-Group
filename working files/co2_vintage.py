"""
What does 'vintage 2021' mean when every series starts in 2010?
-> a scenario published in year Y was calibrated to history up to ~Y; its values for
   years <= Y are (near-)known history, not forecasts. Test: does early-year error
   shrink for recent vintages? And are the energy/economy archetypes confounded by vintage?
"""
import warnings; warnings.filterwarnings('ignore')
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from pathlib import Path

SCI = Path.home()/'PhD'/'4. Modeling'/'Prisma School'/'Scenario_Compass_Initiative_Data'/'SCI-2025_v1.0_pathways_ensemble_global.xlsx'
VAR = 'Emissions|CO2|Energy and Industrial Processes'
OBS = {2010: 33400, 2015: 35400, 2020: 34800, 2025: 38100}
HIND = [2010, 2015, 2020, 2025]

df = pd.read_excel(SCI, sheet_name='data')
meta = pd.read_excel(SCI, sheet_name='meta')
meta['key'] = meta['Model'] + '|||' + meta['Scenario']
meta['pubyear'] = meta['Scientific Manuscript (Citation)'].astype(str).str.extract(r'((?:19|20)\d{2})')[0].astype(float)
yr = meta.set_index('key')['pubyear']

s = df[df['Variable'] == VAR].copy()
s['key'] = s['Model'] + '|||' + s['Scenario']
s['pubyear'] = s['key'].map(yr)
_FAM = ['MESSAGE','REMIND','IMACLIM','IMAGE','WITCH','POLES','GCAM','AIM','COFFEE','TIAM','GEM-E3','PROMETHEUS','EPPA','C-ROADS','MERGE','CGEM','MINES']
s['Family'] = s['Model'].map(lambda m: next((f for f in _FAM if f in str(m).upper()), str(m)))

# vintage bins
def vbin(y):
    if y <= 2019: return '≤2019'
    if y <= 2021: return '2020–2021'
    if y <= 2023: return '2022–2023'
    return '≥2024'
s['vintage'] = s['pubyear'].apply(lambda y: vbin(y) if pd.notna(y) else 'unknown')
ORDER = ['≤2019', '2020–2021', '2022–2023', '≥2024']

# ── 1) MAE & ME at each hindcast year, per vintage bin ──────────────────
print('Family-of-publication effect — error at each hindcast year by vintage')
print(f'{"vintage":<12}{"n":>5} |' + ''.join(f'  MAE{y}' for y in HIND))
print('-'*52)
rows = {}
for v in ORDER:
    sub = s[s['vintage'] == v]
    maes = []
    for y in HIND:
        e = (OBS[y] - sub[str(y)]).abs().dropna(); maes.append(e.mean())
    rows[v] = maes
    print(f'{v:<12}{len(sub):>5} |' + ''.join(f'{m:>7,.0f}' for m in maes))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Hindcast error vs scenario vintage (publication year)', fontsize=13, fontweight='bold')
cmap = plt.cm.viridis(np.linspace(0.15, 0.85, len(ORDER)))
for v, col in zip(ORDER, cmap):
    a1.plot(HIND, rows[v], 'o-', color=col, lw=2, ms=7, label=f'{v} (n={int((s.vintage==v).sum())})')
a1.set_title('MAE by year — recent vintages ≈ 0 early (they knew it)', loc='left', fontsize=10, fontweight='bold')
a1.set_xlabel('Year'); a1.set_ylabel('MAE (Mt CO₂)'); a1.set_xticks(HIND)
a1.legend(fontsize=8, title='vintage'); a1.spines[['top','right']].set_visible(False)
a1.grid(axis='y', alpha=0.15)

# ── 2) Is the energy/economy contrast confounded by vintage? ────────────
ARCH = {'POLES':'energy','TIAM':'energy','COFFEE':'energy','GEM-E3':'economy','IMACLIM':'economy','WITCH':'economy'}
arch = s[s['Family'].isin(ARCH)].copy(); arch['grp'] = arch['Family'].map(ARCH)
comp = (arch.groupby(['Family', 'vintage']).size().unstack(fill_value=0).reindex(columns=ORDER+['unknown'], fill_value=0))
comp = comp.reindex(['POLES','TIAM','COFFEE','GEM-E3','IMACLIM','WITCH'])
bottom = np.zeros(len(comp))
allcols = ORDER + ['unknown']
colmap = dict(zip(ORDER, cmap)); colmap['unknown'] = '0.8'
for c in allcols:
    a2.barh(comp.index, comp[c].values, left=bottom, color=colmap[c], label=c)
    bottom += comp[c].values
a2.set_title('Vintage mix of each archetype model\n(energy = POLES/TIAM/COFFEE, economy = GEM-E3/IMACLIM/WITCH)',
             loc='left', fontsize=10, fontweight='bold')
a2.set_xlabel('n scenarios'); a2.legend(fontsize=8, title='vintage', loc='lower right')
a2.spines[['top','right']].set_visible(False); a2.invert_yaxis()
plt.tight_layout(); plt.savefig('co2_vintage.png', dpi=150, bbox_inches='tight'); print('\nSaved: co2_vintage.png')

print('\nVintage composition of the 6 archetype models:')
print(comp.to_string())
