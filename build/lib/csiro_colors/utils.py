import numpy as np
from IPython.display import HTML

from ._color_picker import colorPicker

# for python 2 and python 3 compatibility
try:
    # python 2
    basestring # type: ignore
except NameError:
    # python 3
    basestring = (str, bytes)
number = (int, float, np.integer, np.floating)


def print_color(color):
    """Utility to print hex color codes in your jupyter notebook
    
    Arguments:
    -----------
    color : str or list of str
        hex codes to be printed in your jupyter notebook
    """
    out = ""
    if not isinstance(color, (list, np.ndarray)) or all([isinstance(ci, number) for ci in color]):
        color = [color]

    for c in color:
        if isinstance(c, basestring):
            out += "<b style='color: {0}'>{0}</b>   ".format(c)
        elif isinstance(c, (list, np.ndarray)):
            if all([isinstance(ci, (int, np.integer)) for ci in c]) or any([ci > 1 for ci in c]):
                c_elements = np.asarray(c).astype(int)
            elif all([isinstance(ci, (float, np.floating)) for ci in c]):
                c_elements = (np.asarray(c)*255).astype(int)
            else:
                raise TypeError('RGB values can only be floating or integer')
            if len(c) == 3:
                out += "<b style='color: rgb({0:d}, {1:d}, {2:d})'>{3}</b>   ".format(*c_elements, c)
            elif len(c) == 4:
                out += "<b style='color: rgba({0:d}, {1:d}, {2:d}, {3:d})'>{4}</b>   ".format(*c_elements, c)
            else:
                raise ValueError("incorrect number of channels for RGB/RGBA value: {0}".format(c))
    return HTML(out)
