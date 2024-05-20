[![Build Check](https://github.com/carpentriesoffline/offlinedatasci/actions/workflows/package-check.yml/badge.svg)](https://github.com/carpentriesoffline/offlinedatasci/actions/workflows/package-check.yml)
[![Documentation Status](https://readthedocs.org/projects/offlinedatasci/badge/?version=latest)](https://offlinedatasci.readthedocs.io/en/latest/?badge=latest)
![PyPI - Downloads](https://img.shields.io/pypi/dm/offlinedatasci)

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

```sh
pip install offlinedatasci
```

### Using pipx:

To install just the command line interface (CLI) we recommend [pipx](https://pipx.pypa.io/). [Install pipx](https://pipx.pypa.io/stable/installation/) and then run:

```sh
pipx install offlinedatasci
```

### Installing development versions

#### Directly From GitHub

```sh
pip install git+https://git@github.com/carpentriesoffline/offlinedatasci.git
```

#### Locally

Clone the repository and from the root directory run:

```sh
git clone https://github.com/carpentriesoffline/offlinedatasci.git
cd offlinedatasci
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

## Developer docs

### Creating a release

1. Increment the version numbers in `pyproject.toml`, `__init__.py`, and `docs/conf.py`
2. Commit and push the changes to GitHub
3. Create a tag for the new version
4. Push the tag to GitHub (`git push upstream <tag_name>`)
5. Make sure the `build` package is installed
6. Make sure your PyPI credentials are stored in `~/.pypirc`
7. Build the source distribution: `python -m build --sdist`
8. Build the universal wheel: `python -m build --wheel`
9. Upload the new release to PyPI: `twine upload dist/*`
