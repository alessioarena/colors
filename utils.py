import matplotlib.colors as col
from IPython.core.display import HTML, display


def print_color(color):
    out = ""
    if isinstance(color, list):
        for c in color:
            out += "<b style='color: {0}'>{0}</b>   ".format(c)
    else:
        out += "<b style='color: {0}'>{0}</b>   ".format(color)
    return display(HTML(out))


def hex_to_rgb(hex_code):
    h = hex_code.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))


def generate_cmap(color_list):
    color_list = [hex_to_rgb(c) for c in color_list]
    return col.ListedColormap(color_list)


def generate_palette(color_list, n_colors):
    return np.array(list(islice(cycle(color_list), n_colors)))