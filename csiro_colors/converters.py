import matplotlib.colors as col
import matplotlib.cm as cm
from IPython.core.display import HTML, display
import numpy as np
from itertools import cycle, islice
from branca.utilities import color_brewer

# for python 2 and python 3 compatibility
try:
    # python 2
    basestring # type: ignore
except NameError:
    # python 3
    basestring = (str, bytes)
number = (int, float, np.integer, np.floating)


def hex_to_rgb(hex_code, normalized=True):
    """Utility to convert HEX color codes to RGB
    
    Arguments:
    -----------
    color : str or list
        hex code(s) to be converted

    Returns:
    -----------
    out : tuple of floats
        RGB channel values
    """
    if isinstance(hex_code, basestring):
        hex_code = [hex_code]
    elif isinstance(hex_code, list):
        pass
    else:
        raise TypeError("hex code must be a str or list of str")
    hex_code = [h.lstrip('#') for h in hex_code]
    if normalized:
        den = 255
    else:
        den = 1
    out = [(int(h[0:2], 16)/den, int(h[2:4], 16)/den, int(h[4:6], 16)/den) for h in hex_code]
    if len(out) == 1:
        return out[0]
    return out

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

    if isinstance(rgb_tuple, tuple):
        rgb_tuple = [rgb_tuple]
    elif isinstance(rgb_tuple, list):
        pass

    if not all([isinstance(rgb, tuple) and (len(rgb) == 3 or len(rgb) == 4) for rgb in rgb_tuple ]):
        raise ValueError("you must provides tuples of 3 or 4 elements")

    if normalized:
        factor = 255
    else:
        factor = 1

    out = []
    for rgb in rgb_tuple:
        out.append('#%02x%02x%02x' % tuple((int(c * factor % 256) for c in rgb[:3])) )
    if len(out) == 1:
        return out[0]
    return out


def css_to_hex(color_name):
    """Utility to convert a CSS4 named color(s) to HEX code(s)

    Parameters
    ----------
    color_name : str or list
        color name to retrieve

    Returns
    -------
    str
        HEX string(s)
    """
    if isinstance(color_name, basestring):
        color_name = [color_name]
    elif isinstance(color_name, list):
        pass
    else:
        raise TypeError("color_name must be a string or list of strings")
    out = []
    for n in color_name:
        try:
            out.append(col.CSS4_COLORS[n.lower()])
        except KeyError:
            raise ValueError("Could not find CSS color '{0}'".format(n))
        
    if len(out) == 1:
        return out[0]
    return out


def css_to_rgb(color_name):
    """Utility to convert a CSS4 named color(s) to RGB value(s)

    Parameters
    ----------
    color_name : str or list
        color name to retrieve

    Returns
    -------
    tuple of floats
        RGB value(s)
    """
    if isinstance(color_name, basestring):
        color_name = [color_name]
    elif isinstance(color_name, list):
        pass
    else:
        raise TypeError("color_name must be a string or list of strings")
    out = []
    for n in color_name:
        try:
            out.append(col.CSS4_COLORS[n.lower()])
        except KeyError:
            raise ValueError("Could not find CSS color '{0}'".format(n))
    
    out = hex_to_rgb(out)

    if len(out) == 1:
        return out[0]
    return out


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
    # if isinstance(cmap, basestring):
    #     cmap = get_cmap(cmap)
    if isinstance(cmap, col.Colormap):
        pass
    else:
        raise TypeError("The argument 'cmap' must be a colormap or colormap name")

    try:
        return list(map(rgb_to_hex, cmap.colors))
    except AttributeError:
        return list(map(rgb_to_hex, cmap(np.linspace(0, 1, 256))))

def cmap_to_rgb(cmap, normalized=True):
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
    # if isinstance(cmap, basestring):
    #     cmap = get_cmap(cmap)
    if isinstance(cmap, col.Colormap):
        pass
    else:
        raise TypeError("The argument 'cmap' must be a colormap or colormap name")

    if normalized:
        n = 255
    else:
        n = 1
    try:
        return [c[:3]*n for c in cmap.colors]
    except AttributeError:
        return [c[:3]*n for c in cmap(np.linspace(0, 1, 256))]
