#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE)
package_list = strsplit(args[2]," ")[[1]]
pth = file.path(args[1], "miniCRAN")
r_installer_version = args[3]

repo = c("https://cloud.r-project.org/")

install_minicran = FALSE
if (!require("miniCRAN")) {
    install_minicran = TRUE
} else if (packageVersion('miniCRAN') < "0.3.0") {
    install_minicran = TRUE
}

if (install_minicran) {
    if (!grepl("http", getOption("repos"))){
        #Lack of a default repo can cause the install to fail
        install.packages("miniCRAN", repos = "https://cloud.r-project.org" )
    } else {
        install.packages("miniCRAN") 
    }
}

library(miniCRAN)

types = c("source", "win.binary", "mac.binary.big-sur-x86_64", "mac.binary.big-sur-arm64")

for (type in types) {
    repo_bin_path <- miniCRAN:::repoBinPath(path = pth, type = type, Rversion = r_installer_version)
    if (!('PACKAGES' %in% list.files(repo_bin_path))) {
        if (!(file.exists(repo_bin_path))) {
            dir.create(repo_bin_path, recursive = TRUE)
        }
        file.create(file.path(repo_bin_path, 'PACKAGES'))
    }
    DC_pkg_tree = pkgDep(package_list, repos = repo, type = type, suggests = FALSE, Rversion = r_installer_version)
    local_cran_avail = pkgAvail(repos = pth, type = type, Rversion = r_installer_version)[, "Version"]
    pkgs_to_download = DC_pkg_tree[!DC_pkg_tree %in% names(local_cran_avail)]
    if (length(pkgs_to_download) == 0) {
        cat("Repository already exists, checking updates for", type, "\n")
        updatePackages(path = pth, repos = repo, type = type, ask = FALSE)
    } 
    else {
        # Get package dependency trees from list of wanted packages
        makeRepo(pkgs_to_download, path = pth, repos = repo, type = type, Rversion = r_installer_version)
    }
}
