# Installation

offlinedatasci is a Python package distributed with releases distributed via the Python Package Index (PyPI).

## Install the CLI (using pipx):

We recomend that most users install the command line interface (CLI) using [pipx](https://pipx.pypa.io/).
This will produce an isolated installation than can be run using the CLI.
First, [install pipx](https://pipx.pypa.io/stable/installation/) and then run:

```sh
pipx install offlinedatasci
```

## Using pip:

To install the package into the current Python environment using pip:

```sh
pip install offlinedatasci
```

## Installing development versions

If you need functionality that has been implemented but not released yet you can install the development version.

### Directly From GitHub

To install directly from GitHub without have a local copy of the code to edit:

```sh
pip install git+https://git@github.com/carpentriesoffline/offlinedatasci.git
```

### Locally

To download and then install the code (which provides a local copy of the code to edit), first clone the repository and then from the root directory run:

```sh
git clone https://github.com/carpentriesoffline/offlinedatasci.git
cd offlinedatasci
pip install .
```

On macOS make sure wheel package is installed first.

## External dependencies

offlinedatasci relies on two external dependencies:

1. R - for creating the partial CRAN mirror to deliver R packages
2. wget - for downloading lesson material

### R

R can be [downloaded and installed via CRAN](https://cran.r-project.org/).
The miniCRAN package that we use does not declare any R version dependency so anything vaguely newish should work. 

### wget

#### Linux

wget is available by default on almost all Linux distributions.

#### macOS

The easiest to install wget on macOS is using homebrew:

```
brew install wget
```

If you are using conda for Python environment management you can also install it using `conda`/`mamba`:

```
conda install wget
```

or

```
mamba install wget
```

#### Windows

Download the appropriate wget executable from <https://eternallybored.org/misc/wget/> and place it on your PATH.
