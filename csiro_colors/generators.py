import matplotlib.colors as col
import matplotlib.cm as cm
from IPython.core.display import HTML, display
import numpy as np
from itertools import cycle, islice
from branca.utilities import color_brewer

from .converters import *
from .cmaps import get_cmap

# for python 2 and python 3 compatibility
try:
    # python 2
    basestring # type: ignore
except NameError:
    # python 3
    basestring = (str, bytes)
number = (int, float, np.integer, np.floating)


def generate_discrete_cmap(color_list, name='CSIRO', n_colors=20):
    """Function to generate discrete colormaps
    
    Arguments:
    -----------
    color_list : list of str, str or Colormap
        list of colors
        if passing a str, this will be interpreted as a colormap to retrieve
        if passing a Colormap, this will be discretized

    Returns:
    -----------
    out : ListedColormap
        colormap object
    """
    if isinstance(color_list, basestring):
        color_list = get_cmap(color_list)
    elif isinstance(color_list, col.ListedColormap):
        return color_list

    if isinstance(color_list, col.Colormap):
        sampling = np.linspace(0, 1, n_colors)
        return col.ListedColormap(color_list(sampling), name=color_list.name)
    color_list = [hex_to_rgb(c) for c in color_list]
    return col.ListedColormap(color_list, name=name)


def generate_palette(color_list, n_colors):
    """Utility to generate a palette that you can use to manually iterate through colors
    
    Arguments:
    -----------
    color_list : list of str
        list of colors
    n_colors : int 
        number of colors required

    Returns:
    -----------
    out : np.array
        array of colors having length equal to n_colors
    """
    return np.array(list(islice(cycle(color_list), n_colors)))


def generate_linear_cmap(color_list, name='CSIRO'):
    """Function to generate a linear colormap given 2 or more colors
    
    Arguments:
    -----------
    color_list : list of str, str or ListedColormap
        list of HEX colors to use
        if passing a str, this will be interpreted as a colormap name to retrieve
        if passing a ListedColormap, this will be linearized
    name : str, optional (default : CSIRO)\n
        name of the colormap
    
    Returns:
    -----------
    out : LinearSegmentedColormap
        linear colormap
    """
    if isinstance(color_list, basestring):
        color_list = get_cmap(color_list)
    elif isinstance(color_list, col.LinearSegmentedColormap):
        return color_list

    if isinstance(color_list, col.ListedColormap):
        return generate_linear_cmap(cmap_to_hex(color_list), name=color_list.name)
    xs = np.linspace(0, 1, len(color_list))
    cdict = {}
    color_list = [hex_to_rgb(h) for h in color_list]
    for channel, idx in zip(['red', 'green', 'blue'], (0, 1, 2)):
        steps = []
        for c, x in zip(color_list, xs):
            steps.append((x, c[idx], c[idx]))
        cdict[channel] = tuple(steps)
    return col.LinearSegmentedColormap(name, cdict)


def randomize_cmap(cmap, n=None, seed=None):
    """Utility to randomize a Colormap

    Parameters
    ----------
    cmap : matplotlib.colors.Colormap
        Colormap to randomize
    n : int, optional
        number of colors to sample, by default None

    Returns
    -------
    matplotlib.colors.ListedColormap
        discrete colormap with random sampled colors

    """
    if isinstance(cmap, str):
        cmap = get_cmap(cmap)
    elif isinstance(cmap, col.Colormap):
        pass
    else:
        raise TypeError('The argument "cmap" must be a string or Colormap')
    if n is None:
        n = cmap.N
    vals = np.arange(0,cmap.N,1)
    if isinstance(seed, int):
        np.random.seed(seed)
    elif seed is None:
        pass
    else:
        raise TypeError('The argument "seed" must be a integer or None')
    np.random.shuffle(vals)
    cmap = col.ListedColormap(cmap(vals[:n]))
    return cmap

