import argparse
from secrets import choice
import sys
from offlinedatasci import *

def get_installer_functions(selection,ods_dir):
    if selection=="all":
        download_r(ods_dir)
        download_software(ods_dir, "rstudio")
        download_minicran(ods_dir) 
        #download_lessons(ods_dir)
        download_software(ods_dir,"python")
        download_python_libraries(ods_dir)

    elif selection=="rstudio" or selection=="python":
        download_software(ods_dir, selection)
    else:
        try:
            download_function = f"download_{selection}"
            #getattr(sys.modules[__name__], download_function)(ods_dir)
        except Exception:
            print(f'method does not exist for selection: {selection}')
def main():
    parser = argparse.ArgumentParser(prog='offlinedatasci')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    INSTALL_OPTIONS=["all", "lessons", "minicran", "python", "python_libraries", "r", "rstudio"]

    install_parser = subparsers.add_parser('install')
    install_parser.add_argument('item',
                                default='all',
                                nargs='+',
                                choices=INSTALL_OPTIONS)

    packages_parser = subparsers.add_parser('add-packages')
    packages_parser.add_argument('language',
                                nargs=1,
                                choices=['r', 'python'])
    packages_parser.add_argument('libraries',
                                nargs='+')

    parser.add_argument('path',
                        metavar='path',
                        type=str,
                        help='path to setup offlinedatasci files in') 


    args = parser.parse_args()
    ods_dir = get_ods_dir(args.path)

    if args.command == 'install':
        for i in args.item:
            get_installer_functions(i,ods_dir)

    elif args.command == 'add-packages':
        packages_to_install = package_selection(args.language[0],args.libraries)
        if args.language[0] == "python":
            download_python_libraries(ods_dir,packages_to_install)
        elif args.language[0] == "r":
            print (packages_to_install)
            download_minicran(ods_dir,packages_to_install)
        
            
if __name__ == '__main__':
              
    main()
