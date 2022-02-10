# csiro_colors: Matplotlib and ColorBrewer in one place
<!-- badges goes here -->

## What it is?
**csiro_colors** is a Python package developed to provide a common
interface to handle colormaps, supporting **matplotlib** (most popular
Python colormaps) and **colorbrewer** (through **branca**, most popular
JavaScript colormaps). In addition, you will be able to find **CSIRO** 
specific colormaps

## Main Features
  - Common interface for **matplotlib** and **colorbrewer** colormaps
  - Conversions from/to RGB, HEX or Colormap objects (**matplotlib**)
  - Conversions from/to linear, discrete colormap or colorpalette
  - Other utilities like **randomize_cmap** or **print_color** (as HTML)

## How to install
The current recommended method to install this package is from source.
To do that, after cloning this repository you can

```sh
pip install .
```

## How to use
For example usage please refer to [this short guide](Example_usage.md)

## How to build
To build a Pypi wheel file run the following command

```sh
python setup.py bdist_wheel --universal
```

This command will create a folder called **dist** where your *whl* file will be
stored

Currently there is no recipe to build a **conda** package

## License
[CSIRO Open Source Software Licence v1.0](LICENSE)

## Getting in contact
For information on this package please [contact us](mailto:BushfireAdaptation@csiro.au?subject=csiro_colors)