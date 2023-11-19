# Installation

## Basic installation

offlinedatasci is available for Python >=3.6 and can be installed using `pip`:

```
pip install DeepForest
```

## External dependencies

offlinedatasci relies on two external dependencies:

1. R - for for creating the partial CRAN mirror to deliver R packages
2. wget - for downloading lesson material

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

Download the appropriate wget executable from https://eternallybored.org/misc/wget/ and place it on your PATH.
