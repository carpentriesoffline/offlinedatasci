# Contributing

## Table of Contents

1. [Contribute to the software](#contribute)
2. [Report issues of problems with the software](#reporting-issues)
3. [Seek support](#getting-help)
4. [Community guidelines](#community-guidelines)

## Contribute

### Getting Started

1. Start by forking the [main repository](https://github.com/carpentriesoffline/offlinedatasci)

2. Clone your copy of the repository.

   - **Using ssh**:

    ```bash
    git clone git@github.com:[your user name]/offlinedatasci.git
    ```

   - **Using https**:

    ```bash
    git clone https://github.com/[your user name]/offlinedatasci.git
    ```

3. Link or point your cloned copy to the main repository. (I always name it upstream)

    ```bash
    git remote add upstream https://github.com/carpentriesoffline/offlinedatasci.git
    ```

4. Check or confirm your settings using `git remote -v`

    ```bash
    origin git@github.com:[your user name]/offlinedatasci.git (fetch)
    origin git@github.com:[your user name]/offlinedatasci.git (push)
    upstream https://github.com/carpentriesoffline/offlinedatasci.git (fetch)
    upstream https://github.com/carpentriesoffline/offlinedatasci.git (push)
    ```

5. Install the package from the main directory.

offlinedatasci can be installed from source using including pip or uv.

**Install using Pip**

```bash
pip install .'[dev,docs]'
```

**Install using uv**

```bash
uv sync --all-extras --dev
```

### Installing R

Code of setting up the CRAN mirror (packages or R) requires requires that R be installed on the system.
If R is not already installed follow the [installation instructions for your operating system](https://cran.r-project.org/)

We use the `miniCRAN` package to handle mirroring CRAN.
It will be automatically installed if it is not already or if the minimum version is too low.

### Running tests locally

```bash
pytest -v
```

## Reporting Issues

* To report issues or problems with either the material or the operation of the site please [open an issue](https://github.com/weecology/forecasting-course/issues/new) and we'll be happy to address it.

## Getting Help

* [Open an issue](https://github.com/weecology/forecasting-course/issues/new) if there’s anything we can do to help!

## Community Guidelines

See our [Code of Conduct](https://github.com/weecology/forecasting-course/tree/main/CODE_OF_CONDUCT.md) for our community guidelines.
