import argparse
from carpenpi import *

def get_parser():
    parser = argparse.ArgumentParser(prog='carpenpi')
    subparsers = parser.add_subparsers(dest='command')

    setup_parser = subparsers.add_parser('setup',
                                            help = 'Setup CarpenPi content')
    setup_parser.add_argument('selection',
                              metavar='selection',
                              type=str,
                              help="Selection of components to setup. Use 'all' to setup everything.",
                              default='all'
                              )
    setup_parser.add_argument('path',
                                metavar='path',
                                type=str,
                                help='path to setup carpenpi files in')
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    print(args)
    if args.command == 'setup':
        carpenpi_dir = create_carpenpi_dir(args.path)
        if args.selection == 'all':
            download_and_save_r_installer(carpenpi_dir)
            download_Rstudio(carpenpi_dir)
            download_lessons(carpenpi_dir)
        elif args.selection == 'r':
            download_and_save_r_installer(carpenpi_dir)
        elif args.selection == 'rstudio':
            download_Rstudio(carpenpi_dir)
        elif args.selection == 'cran':
            find_call_minicran() 
        elif args.selection == 'lessons':
            download_lessons(carpenpi_dir)
        else:
            print("That option is not available. Choose from: all, r, rstudio, cran, lessons")

if __name__ == '__main__':
    main()
