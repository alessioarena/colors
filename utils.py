import matplotlib.colors as col
from IPython.core.display import HTML, display
import numpy as np
from itertools import cycle, islice


def print_color(color):
    """Utility to print hex color codes in your jupyter notebook
    
    Arguments:
    -----------
    color : str or list of str
        hex codes to be printed in your jupyter notebook
    """
    out = ""
    if isinstance(color, list):
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


def generate_discrete_cmap(color_list):
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
    return col.ListedColormap(color_list)


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

