import argparse
from secrets import choice
import sys
from offlinedatasci import *

def get_installer_function(selection, ods_dir):
    if selection == "r-packages": selection = "r_packages"
    if selection == "python-packages": selection = "python_packages"
    if selection == "all":
        download_all(ods_dir)
    elif selection == "rstudio":
        try_except_functions(ods_dir, download_rstudio)
    elif selection == "python":
        try_except_functions(ods_dir, download_python)
    else:
        try:
            download_function = f"download_{selection}"
            getattr(sys.modules[__name__], download_function)(ods_dir)
        except Exception:
            print(f'method does not exist for selection: {selection}')

def main():
    parser = argparse.ArgumentParser(prog = 'offlinedatasci')
    subparsers = parser.add_subparsers(help = 'sub-command help', dest='command')
    INSTALL_OPTIONS = ["all", "lessons", "r-packages", "python", "python-packages", "r", "rstudio"]

    install_parser = subparsers.add_parser('install')
    install_parser.add_argument('item',
                                default = 'all',
                                nargs = '+',
                                choices=INSTALL_OPTIONS)

    packages_parser = subparsers.add_parser('add')
    packages_parser.add_argument('package_type',
                                nargs = 1,
                                choices =['r-packages', 'python-packages'])
    packages_parser.add_argument('packages',
                                nargs = '+')

    parser.add_argument('path',
                        metavar = 'path',
                        type = str,
                        help = 'path to setup offlinedatasci files in') 


    args = parser.parse_args()
    ods_dir = get_ods_dir(args.path)

    if args.command == 'install':
        for i in args.item:
            get_installer_function(i, ods_dir)

    elif args.command == 'add':
        packages_to_install = package_selection(args.package_type[0], args.packages)
        if args.package_type[0] == "python-packages":
            download_python_packages(ods_dir, packages_to_install)
        elif args.package_type[0] == "r-packages":
            download_r_packages(ods_dir, packages_to_install)
        
            
if __name__=='__main__':
              
    main()
