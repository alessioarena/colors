import numpy as np
import matplotlib.colors as col

from .converters import hex_to_rgb, rgb_to_hex, cmap_to_hex, cmap_to_rgb, css_to_rgb, css_to_hex
from .cmaps import matplotlib_registry, branca_registry, csiro_registry, get_cmap
from .generators import generate_discrete_cmap, generate_linear_cmap, generate_palette, randomize_cmap
from .utils import print_color


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
    name = cmap

    if nbins is False:
        cmap = get_cmap(cmap, return_hex=True)
        return generate_linear_cmap(cmap, name)
    elif nbins == None:
        return get_cmap(cmap)
    elif isinstance(nbins, int):

        cmap = get_cmap(cmap)
        if hasattr(cmap, 'colors') and nbins > len(cmap.colors):
            cmap = generate_linear_cmap(cmap)
        sampling = np.linspace(0,1,nbins)
        return col.ListedColormap(cmap(sampling), name=cmap.name)

    else:
        raise TypeError('The argument nbins must be None, False or integer')