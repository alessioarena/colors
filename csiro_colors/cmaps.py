from branca.colormap import _schemes as branca_registry
from matplotlib.cm import _cmap_registry as matplotlib_registry




csiro_main = ['#00A9CE', '#00313C']
csiro_cold = ['#9FAEE5', '#1E22AA', '#41B6E6', '#004B87', '#2DCCD3', '#007377', '#71CC98', '#007A53', '#78BE20', '#44693D']
csiro_warm = ['#6D2077', '#DF1995', '#E4002B', '#E87722', '#FFB81C']
csiro_blues = ['#9FAEE5', '#1E22AA', '#41B6E6', '#004B87', '#2DCCD3', '#007377']
csiro_greens = ['#71CC98', '#007A53', '#78BE20', '#44693D']
csiro_reds = ['#6D2077', '#DF1995', '#E4002B', '#E87722', '#FFB81C']
csiro_all = csiro_main + csiro_blues + csiro_greens + csiro_reds

csiro_registry = {
    'csiro_main' : csiro_main, 
    'csiro_cold' : csiro_cold, 
    'csiro_warm' : csiro_warm, 
    'csiro_blues' : csiro_blues, 
    'csiro_greens' : csiro_greens, 
    'csiro_reds' : csiro_reds, 
    'csiro_all' : csiro_all
}

for k, v in csiro_registry.copy().items():
    csiro_registry[k + '_r'] = v[::-1]


_branca_cmaps = set([s.split('_')[0] for s in branca_registry.keys()])
_csiro_cmaps = set(s.rstrip('_r') for s in csiro_registry.keys())
_matplotlib_cmaps = set([s.rstrip('_r') for s in  matplotlib_registry.keys()])