[![Build Check](https://github.com/carpentriesoffline/offlinedatasci/actions/workflows/package-check.yml/badge.svg)](https://github.com/carpentriesoffline/offlinedatasci/actions/workflows/package-check.yml)

# OfflineDataSci

This package helps you download and configure common tools for teaching and doing data science without an internet connection.
This includes:

* Installers for data science languages: Currently R and Python
* Installers for common data science IDEs: Currently RStudio
* Partial local mirrors of package repositories: Currently CRAN (for R) and PyPI (for Python)
* Locally browseable clones of data science teaching websites: Currently Data Carpentry and Software Carpentry

## Status

Early stage experiment

## Installation

### Using pip:

From PyPI

```sh
pip install offlinedatasci
```

From GitHub (latest development version)

```sh
pip install git+https://git@github.com/carpentriesoffline/offlinedatasci.git
```

### For local development:

Clone the repository and from the root directory run:

```sh
pip install .
```

On macOS make sure wheel package is installed first.

## Usage

### Download and setup everything

```sh
offlinedatasci install all /install/path
```

### Create just the local CRAN mirror with basic data science packages

```sh
offlinedatasci install minicran /install/path
```

### Add packages to repository mirrors:

To add packages beyond those included in the basic data science teaching focused mirrors use `add-packages`
The command structure is `offlinedatasci add-packages` followed by the language you want to add packages to, followed by the names of the packages, followed by the path of the mirror.
The path should be the same as where the mirror was originally setup, so the same install path you used for setup offlinedatasci.

For example, to add the `sf`, `terra`, and `stars` geospatial packages to the CRAN mirror: 

```sh
offlinedatasci add-packages r sf terra stars /install/path
```
