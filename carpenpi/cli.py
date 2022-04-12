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
            pass
        elif args.selection == 'r':
            pass
        elif args.selection == 'rstudio':
            download_Rstudio(carpenpi_dir)
        elif args.selection == 'cran':
            pass
        elif args.selection == 'lessons':
            pass
        else:
            print("That option is not available. Choose from: all, r, rstudio, cran, lessons")

if __name__ == '__main__':
    main()
