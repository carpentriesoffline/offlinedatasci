#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE)

repo = c("https://cran.rstudio.com")
if (!require("miniCRAN")) {
  install.packages("miniCRAN")
  library("miniCRAN")
}
types = c("source", "win.binary", "mac.binary")
DC_pkgs = c("tidyverse", "RSQLite")
pth = file.path(getwd(), "miniCRAN")
for (type in types) {
    repo_bin_path <- miniCRAN:::repoBinPath(path = pth, type = type, Rversion = R.version)
    if (!('PACKAGES' %in% list.files(repo_bin_path))) {
        if (!(file.exists(repo_bin_path))) {
            dir.create(repo_bin_path, recursive = TRUE)
        }
        file.create(file.path(repo_bin_path, 'PACKAGES'))
    }
    DC_pkg_tree = pkgDep(DC_pkgs, repos = repo, type = type, suggests = FALSE, Rversion = R.version)
    local_cran_avail = pkgAvail(repos = pth, type = type, Rversion = R.version)[, "Version"]
    pkgs_to_download = DC_pkg_tree[!DC_pkg_tree %in% names(local_cran_avail)]
    if (length(pkgs_to_download) ==0) {
        cat("Repository already exists, checking updates for", type, "\n")
        updatePackages(path = pth, repos = repo, type = type, ask = FALSE)
    
    } 
    else {
        # Get package dependency trees from list of wanted packages
        makeRepo(pkgs_to_download, path = pth, repos = repo, type = type)
    }
}

