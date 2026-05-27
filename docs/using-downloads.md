# Using the Downloads

This page provides information how to use the software, packages, and lessons downloded by offlinedatasci.
`<path>` refers to the directory you provided when running offlinedatasci.

## Installing Python, R, and RStudio

Installers are stored in `<path>/python/`, `<path>/R/`, and `<path>/rstudio/` respectively.
Run the appropriate installer for your operating system as you normally would (e.g., double-clicking the file).

If using a server, direct users to the installer files at their location on the server.

## Installing Python Packages

offlinedatasci creates a local PyPI mirror at `<path>/pypi/`.
To use this mirror you change the way you call `pip install`.

### From a local directory

To install these packages on the same machine where you ran offlinedatasci:

```sh
pip install --index-url file:///<path>/pypi/ <package>
```

### From a served directory

To install these packages from a server where offlinedatasci was run (common for workshop environments):

```sh
pip install --index-url http://<server-ip>/pypi/ <package>
```

Where `<server-ip>` and instructions on how to connect to it will be provided by the instructor.

## Installing R Packages

offlinedatasci creates a local CRAN mirror at `<path>/miniCRAN/`.
To use this mirror you change the way you call `install.packages()`.

### From a local directory

To install these packages on the same machine where you ran offlinedatasci:

```r
install.packages("<package>", repos = "file:///<path>/miniCRAN")
```

### From a served directory

To install these packages from a server where offlinedatasci was run (common for workshop environments):

```r
install.packages("<package>", repos = "http://<server-ip>/miniCRAN")
```

Where `<server-ip>` and instructions on how to connect to it will be provided by the instructor.

## Browsing Lessons

### From a local directory

Open `<path>/lessons/index.html` in a web browser to see a list of available lessons and navigate to individual lesson pages.
You can do this on most system by either double clicking `<path>/lessons/index.html` or by opening your browser, typing `Ctrl-o` (Windows and Linux) or `Cmd-o` (macos), navigating to `<path>/lessons/` and selecting `index.html`.

### From a served directory

Your instructor should provide you with a url to the lesson material
