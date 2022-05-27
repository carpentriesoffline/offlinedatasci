import argparse
import sys
from offlinedatasci import *

def main():
    parser = argparse.ArgumentParser(prog='offlinedatasci')
    INSTALL_OPTIONS=["all", "custom","lessons","minicran","python", "python_libraries", "r","rstudio"]

    p=parser.add_argument("-i",
                        dest= "install",
                        nargs='?', 
                        const='all',
                        choices=INSTALL_OPTIONS)

    parser.add_argument("--python",
                        nargs='+', 
                        help="for setup")

    parser.add_argument("--r",
                        nargs='+', 
                        help="for setup")

    #parser.add_argument("-custom", 
    #                    dest="custom", 
    #                    help="Custom",
    #                    type=str, 
    #                    choices=["carpentries","data Science", "custom"])

    parser.add_argument('-path',
                        metavar='path',
                        type=str,
                        required=True,
                        help='path to setup offlinedatasci files in') 

    args, unknown = parser.parse_known_args()

    ods_dir = get_ods_dir(args.path)
    print(ods_dir)

    def get_installer_functions(selection,ods_dir):
        print(selection)
        if selection=="all":
            print("Doing all functions")
            download_r(ods_dir)
            download_software(ods_dir, "rstudio")
            download_minicran(ods_dir) 
            #download_lessons(ods_dir)
            download_software(ods_dir,"python")
            python_libraries(ods_dir)
        elif selection=="rstudio" or selection=="python":
            print( selection," downloading")
            download_software(ods_dir,selection)
        else:
            try:
                download_function = f"download_{selection}"
                getattr(sys.modules[__name__], download_function)(ods_dir)
            except Exception:
                print(f'method does not exist for selection {selection}')

    get_installer_functions(args.install,ods_dir)

   
if __name__ == '__main__':
                            
    main()
