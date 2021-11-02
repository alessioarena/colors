import matplotlib.colors as col
import matplotlib.cm as cm
from IPython.core.display import HTML, display
import numpy as np
from itertools import cycle, islice
from branca.utilities import color_brewer

from .cmaps import _csiro_cmaps, _branca_cmaps, _matplotlib_cmaps, csiro_registry


# for python 2 and python 3 compatibility
try:
    # python 2
    basestring # type: ignore
except NameError:
    # python 3
    basestring = (str, bytes)


def _smells_like_branca(cmap):
    if not isinstance(cmap, basestring):
        raise TypeError("the argument cmap must be a colormap name")
    return cmap.rstrip('_r') in _branca_cmaps

def _smells_like_csiro(cmap):
    if not isinstance(cmap, basestring):
        raise TypeError("the argument cmap must be a colormap name")
    return cmap.rstrip('_r') in _csiro_cmaps

def _smells_like_matplotlib(cmap):
    if not isinstance(cmap, basestring):
        raise TypeError("the argument cmap must be a colormap name")
    return cmap.rstrip('_r') in _matplotlib_cmaps

def print_color(color):
    """Utility to print hex color codes in your jupyter notebook
    
    Arguments:
    -----------
    color : str or list of str
        hex codes to be printed in your jupyter notebook
    """
    out = ""
    if isinstance(color, (list, np.ndarray)):
        for c in color:
            out += "<b style='color: {0}'>{0}</b>   ".format(c)
    else:
        out += "<b style='color: {0}'>{0}</b>   ".format(color)
    return display(HTML(out))


def hex_to_rgb(hex_code, normalized=True):
    """Utility to convert HEX color codes to RGB
    
    Arguments:
    -----------
    color : str
        hex code to be converted

    Returns:
    -----------
    out : tuple of floats
        RGB channel values
    """
    h = hex_code.lstrip('#')
    if normalized:
        return tuple(float(int(h[i:i+2], 16))/255 for i in (0, 2 ,4))
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

def rgb_to_hex(rgb_tuple, normalized=True):
    """Utility to convert RGB or RGBA tuples to HEX color strings

    Parameters
    ----------
    rgb_tuple : 3- or 4-items tuple
        RGB or RGBA code
    normalized : bool, optional
        Whether the RGB code is expressed as [0,1] or [0,255], by default True

    Returns
    -------
    str
        HEX string
    """

    if not isinstance(rgb_tuple, (tuple, list, np.ndarray)) or not (len(rgb_tuple) == 3 or len(rgb_tuple) == 4):
        raise ValueError("you must provide a tuple of 3 elements")
    r = []
    for channel in rgb_tuple[:3]:
        if normalized:
            r.append(int(channel * 255))
        else:
            if channel < 0 or channel > 255:
                raise ValueError('Invalid RGB value encountered. Make sure than this represents a 8bit code')
            r.append(channel)
    return '#%02x%02x%02x' % tuple(r)

def cmap_to_hex(cmap):
    """Utility to convert a matplotlib.colors.Colormap to a list of HEX strings

    Parameters
    ----------
    cmap : matplotlib.colors.Colormap
        Colormap object

    Returns
    -------
    list of str
        list of HEX strings
    """
    return list(map(rgb_to_hex, cmap.colors))

def cmap_to_rgb(cmap):
    """Utility to convert a matplotlib.colors.Colormap to a list of RGB codes

    Parameters
    ----------
    cmap : matplotlib.colors.Colormap
        Colormap object

    Returns
    -------
    list of lists of floats
        RGB tuples
    """
    return [c[:3] for c in cmap.colors]


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
    if isinstance(color_list, col.Colormap):
        sampling = np.linspace(0, 1, n_colors)
        return col.ListedColormap(color_list(sampling), name=name)
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

    if isinstance(color_list, col.ListedColormap):
        return generate_linear_cmap(cmap_to_hex(color_list))
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


def get_cmap(cmap, return_hex=False):
    if not isinstance(cmap, basestring):
        raise TypeError("The argument cmap must be a valid colormap name")
    name = cmap

    if _smells_like_branca(cmap):
        # BUG there is a bug with branca https://github.com/python-visualization/branca/issues/104
        # to avoid that we need to iterate to find how many colors the colormap has, then retrieve all of them
        for i in range(12, 5, -1):
            try:
                cmap = color_brewer(cmap, n=i)
                if return_hex:
                    return cmap
                else:
                    return generate_discrete_cmap(cmap, name=name)
            except KeyError:
                pass
            except ValueError:
                # BUG some cmaps appear on the branca registry but they are not there, like viridis
                # in that case we can try matplotlib
                break
        else:
            raise RuntimeError('Could not retrieve the branca colormap scheme')

    if _smells_like_csiro(cmap):
        cmap = csiro_registry[cmap]
        if return_hex:
            return cmap
        else:
            return generate_discrete_cmap(cmap, name=name)

    if _smells_like_matplotlib(cmap):
        cmap = cm.get_cmap(cmap)
        if return_hex:
            return cmap_to_hex(cmap)
        else:
            return cmap

    raise RuntimeError("Could not find the selected colormap. Please check available colormaps at https://rdrr.io/cran/RColorBrewer/man/ColorBrewer.html or https://matplotlib.org/stable/gallery/color/colormap_reference.html")


def brew_colors(cmap, nbins=None):
    """Retrieve a matplotlib or colorbrewer colormap to generate a discrete or linear matplotlib colormap

    Parameters
    ----------
    cmap : str
        colormap name to retrieve
    nbins : int, False or None, optional
        number of discrete colors to have, by default None
        passing None will return a discrete colormap with all available colors
        passing False will return a linear colormap

    Returns
    -------
    ListedColormap or LinearSegmentColormap
        output colormap
    """
    if not isinstance(cmap, basestring):
        raise TypeError("The argument cmap must be a valid colormap name")
    name = cmap

    if nbins is False:
        cmap = get_cmap(cmap, return_hex=True)
        return generate_linear_cmap(cmap, name)
    elif nbins == None:
        return get_cmap(cmap)
    elif isinstance(nbins, int):

        cmap = get_cmap(cmap)
        sampling = np.linspace(0,1,nbins)
        return col.ListedColormap(cmap(sampling))

        # return generate_discrete_cmap(hex_codes, name)
    else:
        raise TypeError('The argument nbins must be None, False or integer')
