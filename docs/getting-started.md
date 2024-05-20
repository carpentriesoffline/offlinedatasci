# Getting started

offlinedatasci comes with two interfaces, a command line interface and a Python interface.

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

## Command line interface

### Installing everything

If you want to download and configure everything use `install all` and pass it the location store files:

```sh
offlinedatasci install all <path>
```

### Installing individual components

You can download and configure the different components separately:

* Python: `offlinedatasci install python <path>`
* Python packages: `offlinedatasci install python-packages <path>`
* R: `offlinedatasci install r <path>`
* RStudio: `offlinedatasci install rstudio <path>`
* R packages: `offlinedatasci install r-packages <path>`
* Lessons: `offlinedatasci install lessons <path>`

### Managing R and Python packages

By default offlinedatasci creates local package mirrors of the most common data science packages.
You can add additional packages yourself using `add-packages`, then language `r` or `python`, and the name of the packages to install:

```sh
offlinedatasci add r-packages package1 package2 ... <path>`
```

```sh
offlinedatasci add python-packages package1 package2 ... <path>`
```

## Python interface

The Python interface follows a similar structure but calling Python
functions directly rather than through the CLI.

### Import the package

```python
import offlinedatasci as ods
```

### Installing everything

```python
ods.download_all("<path>")
```

### Installing individual components

You can download and configure the different components separately:

- Python: `ods.download_python("<path>")`
- Python packages: `ods.download_python_packages("<path>")`
- R: `ods.download_r("<path>")`
- RStudio: `ods.download_rstudio("<path>")`
- R packages: `ods.download_r_packages("<path>")`
- Lessons: `ods.download_lessons("<path>")`

### Managing R and Python packages

By default offlinedatasci creates local package mirrors of the most common data science packages.
You can add additional packages yourself using the `download_*_packages` functions:

- Install custom R packages: `ods.download_r_packages("<path>", [<packagename>, <packagename>])`
- Install custom Python packages: `ods.download_python_packages("<path>", [<packagename>, <packagename>])`
