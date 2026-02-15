import argparse
from secrets import choice
import sys
from offlinedatasci import *

def get_installer_function(selection, ods_dir):
    if selection == "all":
        download_all(ods_dir)
    elif selection == "rstudio":
        try_except_functions(ods_dir, download_rstudio)
    elif selection == "python":
        try_except_functions(ods_dir, download_python)
    elif selection == "r-packages":
        try_except_functions(ods_dir, download_r_packages)
    elif selection == "python-packages":
        try_except_functions(ods_dir, download_python_packages)
    elif selection == "lessons":
        try_except_functions(ods_dir, download_lessons)

def main():
    parser = argparse.ArgumentParser(prog = 'offlinedatasci')
    subparsers = parser.add_subparsers(help = 'sub-command help', dest='command')
    INSTALL_OPTIONS = ["all", "lessons", "r-packages", "python", "python-packages", "r", "rstudio"]

    install_parser = subparsers.add_parser('install')
    install_parser.add_argument('item',
                                default = 'all',
                                nargs = '+',
                                choices=INSTALL_OPTIONS)
    install_parser.add_argument('path',
                                 metavar = 'path',
                                 type = str,
                                 help = 'path to setup offlinedatasci files in')

    packages_parser = subparsers.add_parser('add')
    packages_parser.add_argument('package_type',
                                nargs = 1,
                                choices =['r-packages', 'python-packages'])
    packages_parser.add_argument('packages',
                                nargs = '+')
    packages_parser.add_argument('path',
                                 metavar = 'path',
                                 type = str,
                                 help = 'path to setup offlinedatasci files in')

    
    activate_parser = subparsers.add_parser('activate')
    activate_parser.add_argument('path',
                                metavar = 'path',
                                type = str,
                                help = 'path to offlinedatasci files directory')
    
    deactivate_parser = subparsers.add_parser('deactivate')

    args = parser.parse_args()

    if args.command == 'install':
        ods_dir = get_ods_dir(args.path)
        for i in args.item:
            get_installer_function(i, ods_dir)

<<<<<<< HEAD
    elif args.command == 'add':
        packages_to_install = package_selection(args.package_type[0], args.packages)
        if args.package_type[0] == "python-packages":
            download_python_packages(ods_dir, packages_to_install)
        elif args.package_type[0] == "r-packages":
            download_r_packages(ods_dir, packages_to_install)
=======
    elif args.command == 'add-packages':
        ods_dir = get_ods_dir(args.path)
        packages_to_install = package_selection(args.language[0], args.libraries)
        if args.language[0] == "python":
            download_python_libraries(ods_dir, packages_to_install)
        elif args.language[0] == "r":
            download_minicran(ods_dir, packages_to_install)
    elif args.command == "activate":
        ods_dir = get_ods_dir(args.path)
        activate(ods_dir)
    elif args.command == "deactivate":
        deactivate()
>>>>>>> de7d458 (Add (de)activate to CLI)
        
            
if __name__=='__main__':
              
    main()
