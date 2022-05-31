from branca.colormap import _schemes as branca_registry
from matplotlib.cm import _cmap_registry as matplotlib_registry
from base64 import b64encode
from io import BytesIO
from matplotlib.colors import Colormap
import numpy as np
import matplotlib.pyplot as plt
from branca.utilities import color_brewer
import matplotlib.colors as col
# for python 2 and python 3 compatibility
try:
    # python 2
    basestring # type: ignore
except NameError:
    # python 3
    basestring = (str, bytes)
number = (int, float, np.integer, np.floating)

from .converters import hex_to_rgb, cmap_to_hex

class ColormapCatalog():
    __colormap_image_catalog = None
    
    @property
    def _colormap_image_catalog(self):
        if self.__colormap_image_catalog is None:
            plt.ioff()
            image_catalog= {}
            gradient = np.repeat(np.linspace(0, 1, 256)[None, :], 25,0)
            
            for cmap_name in sorted(self.colormap_registry.keys()):
                if cmap_name.endswith('_r'):
                    continue
                cmap = self.colormap_registry[cmap_name]
                fig = plt.figure(frameon=False, figsize=(10, 0.5))
                ax = fig.add_axes([0, 0, 1, 1])
                ax.imshow(gradient, aspect='auto', cmap=cmap)
                ax.set_axis_off()
                
                tmpfile = BytesIO()
                fig.savefig(tmpfile, format='png', bbox_inches='tight')
                image_catalog[cmap_name] = {'fig': tmpfile}
                plt.close()
            self.__colormap_image_catalog = image_catalog
            plt.ion()
        else:
            image_catalog = self.__colormap_image_catalog
        return image_catalog

    
    def __init__(self, name, cmap_registry):
        self.name = name
        
        cmap_registry = cmap_registry.copy()
        for k, v in cmap_registry.items():
            if isinstance(v, Colormap):
                pass
            elif isinstance(v, list):
                color_list = [hex_to_rgb(c) for c in v]
                cmap_registry[k] = col.ListedColormap(color_list, name=k)
            else:
                raise TypeError("Only Colormap or list are supported")
        self.colormap_registry = cmap_registry
        self.available_colormaps = list(cmap_registry.keys())
    
    def keys(self):
        return self.colormap_registry.keys()
    def items(self):
        return self.colormap_registry.items()
    def values(self):
        return self.colormap_registry.values()
    
    def __getitem__(self, key):
        return self.colormap_registry[key]
    
    def __contains__(self, key):
        return key in self.keys()
    
    @staticmethod
    def _repr_html_fig(figtmpfile, alt=None):
        return '<img src="data:image/png;base64,{0}" alt="{1}">'.format(b64encode(figtmpfile.getvalue()).decode('utf-8'), alt)

    def _repr_html_(self):
        
        # gradient = np.vstack((gradient, gradient))
        
        html = "<table><tbody>"
        
        image_catalog = self._colormap_image_catalog
        
        for cmap_name, cmap in sorted(image_catalog.items()):
            figtmpfile = cmap['fig'] 
            html += '<tr><td style="width:20%; padding:0">{0}</td><td style="width:80%; padding:0">{1}</td></tr>'.format(cmap_name, self._repr_html_fig(figtmpfile))
            
        
        html += "</tbody></table>"
        return html


def _brew_branca_cmap(cmap):
    # BUG there is a bug with branca https://github.com/python-visualization/branca/issues/104
    # to avoid that we need to iterate to find how many colors the colormap has, then retrieve all of them
    for i in range(12, 5, -1):
        try:
            cmap = color_brewer(cmap, n=i)
            return cmap
                
        except KeyError:
            pass
        except ValueError:
            # BUG some cmaps appear on the branca registry but they are not there, like viridis
            # in that case we can try matplotlib
            break
    else:
        raise RuntimeError('Could not retrieve the branca colormap scheme')


def _removesuffix(s, suf):
    if suf and s.endswith(suf):
        return s[:-len(suf)]
    return s


def _smells_like_branca(cmap):
    if not isinstance(cmap, basestring):
        raise TypeError("the argument cmap must be a colormap name")
    return _removesuffix(cmap, '_r') in branca_registry

def _smells_like_csiro(cmap):
    if not isinstance(cmap, basestring):
        raise TypeError("the argument cmap must be a colormap name")
    return _removesuffix(cmap, '_r') in csiro_registry

def _smells_like_matplotlib(cmap):
    if not isinstance(cmap, basestring):
        raise TypeError("the argument cmap must be a colormap name")
    return _removesuffix(cmap, '_r') in matplotlib_registry


def get_cmap(cmap, return_hex=False):

    if isinstance(cmap, basestring):
        if _smells_like_branca(cmap):
            cmap = branca_registry[cmap]
        elif _smells_like_csiro(cmap):
            cmap = csiro_registry[cmap]
        elif _smells_like_matplotlib(cmap):
            cmap = matplotlib_registry[cmap]
        else:
            raise RuntimeError("Could not find the selected colormap. Please check available colormaps at https://rdrr.io/cran/RColorBrewer/man/ColorBrewer.html or https://matplotlib.org/stable/gallery/color/colormap_reference.html")
    elif isinstance(cmap, col.Colormap):
        pass
    else:
        raise TypeError("The argument cmap must be a valid colormap name")

    if return_hex:
        return cmap_to_hex(cmap)
    else:
        return cmap


csiro_main = ['#00313C', '#00A9CE']
csiro_core = csiro_main + ['#000000', '#757579', '#dadbdc']
csiro_primary = ['#1E22AA', '#004B87', '#6D2077', '#007377', '#007A53']
csiro_secondary = ['#DF1995', '#E87722', '#FFB81C', '#9FAEE5', '#71CC98', '#78BE20', '#2DCCD3']
csiro_cold = ['#9FAEE5', '#1E22AA', '#41B6E6', '#004B87', '#2DCCD3', '#007377', '#71CC98', '#007A53', '#78BE20', '#44693D']
csiro_warm = ['#6D2077', '#DF1995', '#E4002B', '#E87722', '#FFB81C']
csiro_blues = ['#9FAEE5', '#1E22AA', '#41B6E6', '#004B87', '#2DCCD3', '#007377']
csiro_greens = ['#71CC98', '#007A53', '#78BE20', '#44693D']
csiro_reds = ['#6D2077', '#DF1995', '#E4002B', '#E87722', '#FFB81C']
csiro_all = csiro_main + csiro_blues + csiro_greens + csiro_reds

csiro_registry = {
    'csiro_main' : csiro_main, 
    'csiro_core': csiro_core,
    'csiro_primary': csiro_primary,
    'csiro_secondary': csiro_secondary,
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
# _csiro_cmaps = set(_removesuffix(s, '_r') for s in csiro_registry.keys())
# _matplotlib_cmaps = set([_removesuffix(s, '_r') for s in  matplotlib_registry.keys()])

branca_registry = {k: _brew_branca_cmap(k) for k in _branca_cmaps if _brew_branca_cmap(k)}
branca_registry = ColormapCatalog('Branca', branca_registry)
matplotlib_registry = ColormapCatalog('Matplotlib', matplotlib_registry)
csiro_registry = ColormapCatalog('CSIRO', csiro_registry)