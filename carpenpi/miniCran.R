#Installing minicran
if (!require("miniCRAN")) {
  install.packages("miniCRAN")
  library("miniCRAN")
}


repo = c("https://cran.rstudio.com")

#Return desired local path and create if needed
new.local.dir = function(name,create = FALSE){
  local.dir=file.path(getwd(),name)
  if (create==TRUE)
  dir.create(local.dir, recursive = TRUE)
  return(local.dir)
};

#Open local file of wanted packages
wanted_pkgs = readLines(new.local.dir("required_packages/workshop_packages.csv",create = FALSE));

# Note: Later use regex for determining if first line is header or not
if ( wanted_pkgs[1]=="package_name") {DC_pkgs = wanted_pkgs[-1]
} else { 
  DC_pkgs = wanted_pkgs
};

# Get package dependency trees from list of wanted packages
DC_pkg_tree = pkgDep(DC_pkgs, repos = repo, type = "source", suggests = FALSE, Rversion = R.version);

#Create and export matrix of packages and their dependency trees 
wanted_pkg_tree = matrix(DC_pkg_tree);colnames(wanted_pkg_tree) = "Package";
write.csv(wanted_pkg_tree,file = new.local.dir("required_packages/package_tree_download.csv",create = FALSE));

#Verify available packages on CRAN for desired OS
avail_pkgs = pkgAvail(repos = repo, type = "mac.binary");

#Get info of wanted current available package versions
wanted_pkgs_info = merge(avail_pkgs,wanted_pkg_tree);

# Check for miniCRAN local versions of wanted OS
downloadpath = new.local.dir("downloads",create = TRUE);
local_pkg_versions = pkgAvail(downloadpath, type = "mac.binary");

local=local_pkg_versions[, "Version"][-1]

online=wanted_pkgs_info[, "Version"]

online %in% local


#Identify packages that need go be updated

makeRepo(pkgs=DC_pkg_tree, path = downloadpath, repos = repo, type = c("source", "mac.binary"))

#List packages
repos = getOption(repo)

pkgAvail(downloadpath, type = "mac.binary")[, "Version"]

pkgAvail(repos = repo, type = "mac.binary")

list.files(pth, recursive = TRUE, full.names = FALSE)

 (DC_pkg_tree, repos = repo, type = "mac.binary")

#Install packages
install.packages(DC_pkg_tree, 
                 repos = paste0("file:///", pth),
                 type = "binary")

#Windows need Rtools
#https://stackoverflow.com/questions/53279685/r-make-not-found-when-installing-a-r-package-from-local-tar-gz
availPkgs = pkgAvail(repos = repo, type = "mac.binary")

availPkgs = pkgAvail(repos = repo, type = "mac.binary")[, "Depends"]
oldPackages(
  repos = getOption(repo),
  availPkgs = pkgAvail(repos = repos, type = "mac.binary")[,Depends],
  method=NULL,
  availableLocal = pkgAvail(repos ="/Users/virnaliz/Desktop/DC_miniCRAN/downloads/" , type = "mac.binary", quiet =
                              quiet),
  type = "mac.binary",
  Rversion = R.version,
  quiet = FALSE
)
downloadpath