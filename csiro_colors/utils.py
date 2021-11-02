import matplotlib.colors as col
import matplotlib.cm as cm
from IPython.core.display import HTML, display
import numpy as np
from itertools import cycle, islice
from branca.utilities import color_brewer, linear_gradient


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


def generate_discrete_cmap(color_list, name='CSIRO'):
    """Function to generate discrete colormaps
    
    Arguments:
    -----------
    color_list : list of str
        list of colors

    Returns:
    -----------
    out : ListedColormap
        colormap object
    """
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
    color_list : list of str
        list of HEX colors to use
    name : str, optional (default : CSIRO)\n
        name of the colormap
    
    Returns:
    -----------
    out : LinearSegmentedColormap
        linear colormap
    """
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
        cmap = cm.get_cmap(cmap)
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

def sample_cmap(cmap, n):
    """Utility to sample a Colormap

    Parameters
    ----------
    cmap : matplotlib.colors.Colormap
        Colormap to sample
    n : int
        number of colors to sample

    Returns
    -------
    matplotlib.colors.ListedColormap
        discrete colormap with sampled colors

    """
    if isinstance(cmap, str):
        cmap = cm.get_cmap(cmap)
    elif isinstance(cmap, col.Colormap):
        pass
    else:
        raise TypeError('The argument "cmap" must be a string or Colormap')
    vals = np.linspace(0,1,n)
    cmap = col.ListedColormap(cmap(vals))
    return cmap


def brew_colors(cmap, nbins=None):
    """Retrieve a matplotlib or colorbrewer colormap to generate a discrete or linear matplotlib colormap

    Parameters
    ----------
    cmap : str
        colormap name to retrieve
    nbins : int, optional
        number of discrete colors to have, by default None will generate a linear colormap

    Returns
    -------
    ListedColormap or LinearSegmentColormap
        output colormap
    """

    name = cmap
    # BUG there is a bug with branca https://github.com/python-visualization/branca/issues/104
    # to avoid that we need to iterate to find how many colors the colormap has, then retrieve all of them


    for i in range(12, 5, -1):
        try:
            cmap = color_brewer(cmap, n=i)
            if nbins is None:
                return generate_linear_cmap(cmap, name)
            hex_codes = linear_gradient(cmap, nbins)
            return generate_discrete_cmap(hex_codes, name)
        except KeyError:
            pass
        except ValueError:
            break
    else:
        raise RuntimeError('Could not interpret the colormap scheme')
    
    if isinstance(cmap, col.Colormap):
        pass
    else:
        try:
            cmap = cm.get_cmap(cmap)
        except ValueError:
            raise ValueError("The selected colormap is not a matplotlib or branca (colorbrewer) colormap. Please check https://rdrr.io/cran/RColorBrewer/man/ColorBrewer.html or https://matplotlib.org/stable/gallery/color/colormap_reference.html for options")
    
    if nbins is None:
        return cmap
    vals = np.linspace(0, 1, nbins)
    cmap = col.ListedColormap(cmap(vals), name)
    return cmap