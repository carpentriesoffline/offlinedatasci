#!/usr/bin/env Rscript
#Rscript miniCran.R
repo = c("https://cran.rstudio.com")
#Installing minicran
if (!require("miniCRAN")) {
  install.packages("miniCRAN")
  library("miniCRAN")
}

#Function to return desired local path and create if needed
  # Create temporary folder for miniCRAN
dir.create(pth <- file.path(getwd(), "miniCRAN"))
  
  #Open local file of wanted packages
wanted_pkgs = read.csv("required_packages/workshop_packages.csv")
DC_pkgs = wanted_pkgs$package_name
  
  # Get package dependency trees from list of wanted packages
DC_pkg_tree = pkgDep(DC_pkgs, repos = repo, type = "source", suggests = FALSE, Rversion = R.version);
  
makeRepo(DC_pkg_tree, path = pth, repos = repo, type = c("source", "win.binary","mac.binary"))





