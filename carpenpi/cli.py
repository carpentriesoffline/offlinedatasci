import os
import sys

import argparse
from carpenpi import download, download_lessons, downloadfiles
from carpenpi import create_carpenpi_dir
import carpenpi

def get_parser():
    parser = argparse.ArgumentParser(prog='carpenpi')
    subparsers = parser.add_subparsers(dest='command')

    download_parser = subparsers.add_parser('download',
                                            help = 'Download CarpenPi content')
    download_parser.add_argument('path',
                                metavar='path',
                                type=str,
                                help='path to download carpenpi files to')
    download_parser = subparsers.add_parser('download-lessons',
                                            help = 'Download Carpentries lessons')
    download_parser.add_argument('path',
                                metavar='path',
                                type=str,
                                help='path to download carpenpi files to')
    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    print(args)
    if args.command == 'download':
        carpenpi_dir = create_carpenpi_dir(args.path)
        download(carpenpi_dir)
    if args.command == 'download-lessons':
        carpenpi_dir = create_carpenpi_dir(args.path)
        download_lessons.download_lessons(carpenpi_dir)


if __name__ == '__main__':
    main()
