#python setup.py build_ext --inplace
#python setup.py bdist_wheel --universal
from setuptools import setup, find_packages

requires = [
    "matplotlib>=3.4.1",
    "ipython>=7.22",
    "numpy",
    "branca>=0.4.2",
]

setup(
    name="csiro_colors",
    version="0.1.0",
    description="CSIRO and generic colormap handler",
    author="Alessio Arena",
    author_email="alessio.arena@csiro.au",
    packages = find_packages(),
    install_requires=requires,
)