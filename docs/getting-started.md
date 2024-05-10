# Getting started

offlinedatasci comes with two interfaces, a command line interface and a Python interface.

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

Coming soon!
