## Retrieving a colormap
This can be done by simply calling the **get_cmap** function.
This function will always return a **matplotlib** colormap

```Python
import csiro_colors as ccol
cmap = ccol.get_cmap('inferno') # this is a matplotlib colormap
cmap
```
![Matplotlib colormap](media/Example1.png)

```Python
cmap = ccol.get_cmap('Accent') # this is a colorbrewer colormap
cmap
```
![Colorbrewer colormap](media/Example2.png)

```Python
cmap = ccol.get_cmap('csiro_reds') # this is a CSIRO specific colormap
cmap
```
![CSIRO colormap](media/Example3.png)


## Modify a colormap
```Python
ccol.randomize_cmap(cmap) #we are not storing this result
```
![CSIRO colormap with random color order](media/Example4.png)

```Python
cmap = ccol.generate_linear_cmap(cmap)
cmap
```
![CSIRO colormap as continuous](media/Example5.png)

```Python
cmap = ccol.generate_discrete_cmap(cmap, n_colors=12)
# NOTE if you need more colors than the original ones you will have to convert the colormap to linear first
cmap
```
![CSIRO colormap as discrete](media/Example6.png)


## One call to rule them all
```Python
cmap = ccol.brew_colors('csiro_reds', nbins=None) # retrieve it and return it untouched
cmap
```
![CSIRO colormap](media/Example3.png)

```Python
cmap = ccol.brew_colors('csiro_reds', nbins=False) # retrieve it and return it as linear
cmap
```
![CSIRO colormap as continuous](media/Example5.png)

```Python
cmap = ccol.brew_colors('csiro_reds', nbins=12) # retrieve it and return a specific number of colors
cmap
```
![CSIRO colormap as discrete](media/Example6.png)


## Conversion to basic types
```Python
hex_colors = ccol.cmap_to_hex(cmap) #supports conversions between Colormap, hex codes or RGB/RGBA tuple
ccol.print_color(hex_colors)
```
![HEX codes for the discrete CSIRO colormap](media/Example7.png)

```Python
rgb_colors = ccol.cmap_to_rgb(cmap, normalized=False)
ccol.print_color(rgb_colors)
```
![RGB codes for the discrete CSIRO colormap](media/Example8.png)


## References

For a full list of **matplotlib** colormaps, please refer to [matplotlib documentation](https://matplotlib.org/stable/gallery/color/colormap_reference.html)
or use:
```Python
list(ccol.csiro_registry)
```

For a full list of **colorbrewer** colormaps, please refer to this [R documentation](https://rdrr.io/cran/RColorBrewer/man/ColorBrewer.html)
or use:
```Python
list(ccol.branca_registry)
```

For available **CSIRO** colormaps please use:
```Python
list(ccol.csiro_registry)
```